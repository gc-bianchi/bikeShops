import requests
from bs4 import BeautifulSoup
import re
import csv


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


url_list = []
with open("justUrls.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        url_list.extend(row)

batch_size = 10
num_batches = len(url_list) // batch_size + 1

for batch_num in range(num_batches):
    start_index = batch_num * batch_size
    end_index = (batch_num + 1) * batch_size
    batch_urls = url_list[start_index:end_index]
    emails = scrape_emails(batch_urls)

    filename = f"email_batch_{batch_num + 1}.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["email"])
        writer.writerows([[url] for url in emails])

    print(f"Batch {batch_num + 1} completed. CSV file saved successfully.")

print("All batches processed.")
