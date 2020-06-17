import extractor as ext
import csv
from bs4 import BeautifulSoup
from datetime import date


def extract_web(url, class_tag):
    if url is None or class_tag is None:
        return None
    raw = ext.simple_get(url)
    res = str(raw, 'utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    list_links = soup.find_all(class_=class_tag)
    return list_links


def write_to_csv(list_links, output_path, weight, url_prefix=None):
    d = date.today().strftime("%y-%m-%d")

    file_name = output_path + "/" + "financial-times-" + d + ".csv"
    with open(file_name, 'w', newline='') as file:
        w = csv.writer(file, delimiter=',')
        w.writerow(['Title', 'Weight', 'Link'])
        for l in list_links:
            title = l.get_text()
            link = url_prefix + l.attrs["href"]
            w.writerow([title, weight, link])
    return

if __name__ == "__main__":
    URL = 'https://www.ft.com'
    output_path = "../data"
    tag = 'js-teaser-heading-link'

    raw = extract_web(URL, tag)
    write_to_csv(raw, output_path, 1, URL)

    # End of File