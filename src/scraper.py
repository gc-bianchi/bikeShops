import requests
from bs4 import BeautifulSoup
import re


def extract_emails(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    html_text = str(soup)

    # Find email addresses using regex
    emailPattern = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|<a.*?href=["\'](mailto:.*?)["\'].*?>.*?</a>',
        re.IGNORECASE,
    )
    emails = re.findall(emailPattern, html_text)

    return emails


def scrape_emails(url_list):
    all_emails = []

    for url in url_list:
        print(f"scraping {url}")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract email addresses from the current page
            emails = extract_emails(url)
            all_emails.extend(emails)

            pattern = re.compile(
                r'<a.*?href=["\'](.*?)["\'].*?>.*?contact.*?</a>', re.IGNORECASE
            )

            other_pages = soup.find_all(
                "a", href=True, text=re.compile(r"contact", re.IGNORECASE)
            )

            for page in other_pages:
                page_url = page.get("href")
                if not page_url.startswith("http://") and not page_url.startswith(
                    "https://"
                ):
                    page_url = url + page_url

                print(f"scraping {page_url}")
                emails = extract_emails(page_url)

                all_emails.extend(emails)
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")

    return all_emails


# Example usage
url_list = [
    "https://www.505cycles.com",
    "http://www.utahmountainbiking.com",
    "https://www.mendbicycles.com",
    "http://2riversbicycle.com",
    "http://2020cycle.com",
]


emails = scrape_emails(url_list)
print(emails)
