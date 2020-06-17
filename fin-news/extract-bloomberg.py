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


def write_to_csv(output_path, data, weight, url_prefix=None):
    with open(output_path, 'w', newline='') as file:
        w = csv.writer(file, delimiter=',')
        w.writerow(['Title', 'Weight', 'Link'])
        for l in data:
            title = l.get_text()
            link = url_prefix + l.attrs["href"]
            w.writerow([title, weight, link])
    return

def append_to_csv(output_path, data, weight, url_prefix=None):
    with open(output_path, 'a', newline='') as f:
        w = csv.writer(f)
        for l in data:
            title = l.get_text()
            link = url_prefix + l.attrs["href"]
            w.writerow([title, weight, link])
    return


if __name__ == "__main__":
    URL = 'https://www.bloomberg.com'
    output_path = "../data"

    d = date.today().strftime("%y-%m-%d")
    output_path += "/" + "bloomberg-" + d + ".csv"

    # header
    tag = 'single-story-module__headline-link'
    raw_1 = extract_web(URL, tag)
    write_to_csv(output_path, raw_1, 0.9, URL)

    # header related 
    tag = 'single-story-module__related-story-link'
    raw_2 = extract_web(URL, tag)
    append_to_csv(output_path, raw_2, 0.8, URL)

    # non-header
    tag = 'story-package-module__story__headline-link'
    raw_3 = extract_web(URL, tag)
    append_to_csv(output_path, raw_3, 0.5, URL)

    # End of File