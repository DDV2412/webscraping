import requests
from bs4 import BeautifulSoup
import re

class JournalScraper:
    def __init__(self, journal):
        self.journal = journal
        self.session = requests.Session()

    def login(self, login_url, payload):
        try:
            response = self.session.post(login_url, data=payload)
            return response.ok
        except requests.RequestException as e:
            print(f"Login error: {e}")
            return False

    def scrape_data(self, base_url, name_journal):
        scraped_data = []
        try:
            target_url = f"{base_url}/editor/submissions/submissionsInReview"
            response = self.session.get(target_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            pagination_td = soup.find("td", colspan="5", align="left")
            if not pagination_td:
                print("Pagination element not found")
                return scraped_data

            # Extract and match pagination text
            pagination = pagination_td.text.strip()
            pattern = r"(\d+)\s*-\s*(\d+)\s*of\s*(\d+)\s*Items"
            matches = re.match(pattern, pagination)
            if not matches:
                print(f"Pagination text '{pagination}' does not match expected pattern")
                return scraped_data

            per_page = int(matches.group(2))
            total_items = int(matches.group(3))
            total_pages = (total_items + per_page - 1) // per_page

            for current_page in range(1, total_pages + 1):
                target_url = f"{base_url}/editor/submissions/submissionsInReview?submissionsPage={current_page}"
                response = self.session.get(target_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")

                listing_table = soup.find("table", class_="listing")
                submission_rows = listing_table.find_all("tr", valign="top")

                for row in submission_rows:
                    review_link = row.find("a", class_="action")

                    if review_link:
                        url = review_link.get("href")
                        submission_id = re.search(r"/(\d+)$", url).group(1)
                        modified_url = url.replace("submissionReview", "submission")

                        review_response = self.session.get(modified_url)
                        review_response.raise_for_status()
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
        except requests.RequestException as e:
            print(f"Error while scraping data: {e}")
        return scraped_data

    def run(self):
        all_scraped_data = []
        login_url = f"{self.journal['url']}/login/signIn"
        payload = {
            "username": "iaesmedia", "password": "254#@#@778&%$"
        }
        if self.login(login_url, payload):
            scraped_data = self.scrape_data(self.journal['url'], self.journal["journal_name"])
            all_scraped_data.extend(scraped_data)
        else:
            print(f"Failed to log in to {self.journal['journal_name']}.")
        return all_scraped_data