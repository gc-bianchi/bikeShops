import requests
from bs4 import BeautifulSoup

# URL of the directory page
data = []
justUrls = []
stillActiveSites = []
for i in range(21):
    url = "https://www.pinkbike.com/directory/list/united-states/?country=194&category=2&page="
    urlFinal = url + str(i + 1)
    response = requests.get(urlFinal)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select('td > a[href^="https://www.pinkbike.com/directory/"]')
    for link in links:
        href = link.get("href")
        start_index = href.find("=") + 1
        extracted_value = href[start_index:]
        data.append(extracted_value)
        # print(extracted_value)
for url in data:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a_tag = soup.select_one("li.nowrap.ellipoverflow > a")
    if a_tag is not None:
        href_value = a_tag["href"]
        justUrls.append(href_value)
        print(href_value)

print(justUrls)
