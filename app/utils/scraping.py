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

           
                    authors_div = review_soup.find("div", id="authors")

                    author_entries = authors_div.find_all("tr", valign="top")

         
                    authors_set = set()

                    author_lists = []
                
                    for author_entry in author_entries:
                        author_name_element = author_entry.find("td", class_="label", string="Name")
                        
                        if author_name_element:
                            author_value = author_name_element.find_next("td", class_="value")
                            name = author_value.text.strip() if author_value else None
                        else:
                            name = None

                        affiliate_element = author_entry.find("td", class_="label", string="Affiliation")
                        
                        if affiliate_element:
                            affiliate_value = affiliate_element.find_next("td", class_="value")
                            affiliation = affiliate_value.text.strip() if affiliate_value else None
                        else:
                            affiliation = None


                        authors_set.add((name, affiliation))


                    authors_list = list(authors_set)

                    filtered_data = [(name, affiliation) for name, affiliation in authors_list if name is not None]

                    for name, affiliation in filtered_data:
                        data = {
                            "name" : name,
                            "affiliation": affiliation
                        }

                        author_lists.append(data)


                    title_element = review_soup.find(
                        "td", class_="label", string="Title"
                    )
                    title = title_element.find_next("td", class_="value").text.strip()

                    abstract_element = review_soup.find(
                        "td", class_="label", string="Abstract"
                    )
                    abstract = abstract_element.find_next(
                        "td", class_="value"
                    ).text.strip()

                    submission_data = {
                        "submission_id": submission_id,
                        "authors": author_lists,
                        "title": title,
                        "abstract": abstract,
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
