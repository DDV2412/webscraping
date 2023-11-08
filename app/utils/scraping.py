import requests
from bs4 import BeautifulSoup
import re


class JournalScraper:
    def __init__(self, journal):
        self.journal = journal
        self.session = requests.Session()

    def login(self, login_url, payload):
        response = self.session.post(login_url, data=payload)
        return response.ok

    def scrape_data(self, base_url, name_journal):
        scraped_data = []
        cookies = self.session.cookies.get_dict()

        target_url = f"{base_url}/editor/submissions/submissionsInReview"
        response = self.session.get(target_url)
        soup = BeautifulSoup(response.content, "html.parser")

        pagination = soup.find("td", colspan="5", align="left").text.strip()
        pattern = r"(\d+)\s*-\s*(\d+)\s*of\s*(\d+)\s*Items"
        matches = re.match(pattern, pagination)

        per_page = int(matches.group(2))
        total_items = int(matches.group(3))
        total_pages = (total_items + per_page - 1) // per_page

        for current_page in range(1, total_pages + 1):
            target_url = f"{base_url}/editor/submissions/submissionsInReview?submissionsPage={current_page}"
            response = self.session.get(target_url)
            soup = BeautifulSoup(response.content, "html.parser")

            listing_table = soup.find("table", class_="listing")
            submission_rows = listing_table.find_all("tr", valign="top")

            for row in submission_rows:
                review_link = row.find("a", class_="action")

                if review_link:
                    url = review_link.get("href")
                    submission_id = re.search(r"/(\d+)$", url).group(1)
                    modified_url = url.replace("submissionReview", "submission")

                    review_response = requests.get(modified_url, cookies=cookies)
                    review_soup = BeautifulSoup(review_response.content, "html.parser")

                    submission_element = review_soup.find("div", id="submission")

                    if submission_element:
                        title_element = submission_element.find(
                            "td", class_="label", string="Title"
                        )
                        title = (
                            title_element.find_next("td", class_="value").text.strip()
                            if title_element
                            else None
                        )

                        authors_element = submission_element.find(
                            "td", class_="label", string="Authors"
                        )
                        authors = (
                            authors_element.find_next("td", class_="value").text.strip()
                            if authors_element
                            else None
                        )

                        date_submitted_element = submission_element.find(
                            "td", class_="label", string="Date submitted"
                        )
                        date_submitted = (
                            date_submitted_element.find_next("td").text.strip()
                            if date_submitted_element
                            else None
                        )

                        submission_data = {
                            "submission_id": submission_id,
                            "title": title,
                            "authors": authors,
                            "date_submitted": date_submitted,
                            "journal_name": name_journal,
                        }

                        scraped_data.append(submission_data)

        return scraped_data

    def run(self):
        all_scraped_data = []
        login_url = f"{self.journal['url']}/login/signIn"
        payload = self.journal.get("payload", {})
        if self.login(login_url, payload):
            target_url = f"{self.journal['url']}"
            scraped_data = self.scrape_data(target_url, self.journal["journal_name"])
            all_scraped_data.extend(scraped_data)
        else:
            print(f"Failed to log in to {self.journal['journal_name']}.")

        return all_scraped_data
