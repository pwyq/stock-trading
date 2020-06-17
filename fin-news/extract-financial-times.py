import extractor as ext
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


if __name__ == "__main__":
    URL = 'https://www.ft.com'
    output_path = "../data"
    tag = 'js-teaser-heading-link'

    d = date.today().strftime("%y-%m-%d")
    output_path += "/" + "financial-times-" + d + ".csv"

    raw = extract_web(URL, tag)
    ext.write_to_csv(output_path, raw, 1, URL)

    # End of File