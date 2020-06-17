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
    URL = 'https://www.bloomberg.com'
    output_path = "../data"

    d = date.today().strftime("%y-%m-%d")
    output_path += "/" + "bloomberg-" + d + ".csv"

    # header
    tag = 'single-story-module__headline-link'
    raw_1 = extract_web(URL, tag)
    ext.write_to_csv(output_path, raw_1, 0.9, URL)

    # header related 
    tag = 'single-story-module__related-story-link'
    raw_2 = extract_web(URL, tag)
    ext.append_to_csv(output_path, raw_2, 0.8, URL)

    # non-header
    tag = 'story-package-module__story__headline-link'
    raw_3 = extract_web(URL, tag)
    ext.append_to_csv(output_path, raw_3, 0.5, URL)

    # End of File