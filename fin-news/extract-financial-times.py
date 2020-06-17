import extractor as ext
import csv
from bs4 import BeautifulSoup
from datetime import date


def extract_web(url):
    raw = ext.simple_get(url)
    res = str(raw, 'utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    list_links = soup.find_all(class_='js-teaser-heading-link')
    return list_links


def write_to_csv(list_links, output_path, url_prefix=None):
    d = date.today().strftime("%y-%m-%d")

    file_name = output_path + "/" + "financial-times-" + d + ".csv"
    with open(file_name, 'w', newline='') as file:
        w = csv.writer(file, delimiter=',')
        w.writerow(['Title', 'Link'])
        for l in list_links:
            title = l.get_text()
            link = url_prefix + l.attrs["href"]
            w.writerow([title, link])
    return

if __name__ == "__main__":
    URL = 'https://www.ft.com'
    output_path = "../data"

    raw = extract_web(URL)
    write_to_csv(raw, output_path, URL)

    # End of File