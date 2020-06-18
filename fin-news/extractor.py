from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import csv
import constants as const

# ********************************
# Web extracting
# ********************************

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, headers=const.HEADERS)) as resp:
            if is_good_response(resp) is True:
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error(url, e)
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(url, e):
    print('[ERROR] Error during requests to {0}:\n{1}'.format(url, str(e)))
    return


def extract_web_with_class_tag(url, class_tag):
    if url is None or class_tag is None:
        return None
    raw = simple_get(url)
    res = str(raw, 'utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    list_links = soup.find_all(class_=class_tag)
    return list_links


def extract_web_with_attr(url, attr):
    if url is None or attr is None:
        return None
    raw = simple_get(url)
    res = str(raw, 'utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    list_links = soup.find_all(attr)
    return list_links


# ********************************
# Data output
# ********************************


def write_to_csv(output_path, data, weight, timestamp, url_prefix=None):
    with open(output_path, 'w', newline='') as file:
        w = csv.writer(file, delimiter=',')
        w.writerow(const.CSV_TITLE)
        for l in data:
            # message less than 5 words hardly contain useful info
            if len(l.get_text().split()) <= 5:
                continue
            # remove leading & trailing spaces
            title = l.get_text().strip()
            if "href" in l.attrs:
                link = url_prefix + l.attrs["href"] if url_prefix is not None else l.attrs["href"]
            else:
                link = ''
            w.writerow([title, weight, timestamp, link])
    return


def write_to_csv_marketwatch(output_path, data, weight, timestamp, url_prefix=None):
    with open(output_path, 'w', newline='') as file:
        w = csv.writer(file, delimiter=',')
        w.writerow(const.CSV_TITLE)
        for l in data:
            if len(l.get_text().split()) <= 5:
                continue
            title = l.get_text().strip()
            if "href" in l.attrs:
                link = url_prefix + l.attrs["href"] if url_prefix is not None else l.attrs["href"]
            else:
                link = ''
            w.writerow([title, weight, timestamp, link])
    return


def append_to_csv(output_path, data, weight, timestamp, url_prefix=None):
    with open(output_path, 'a', newline='') as f:
        w = csv.writer(f)
        for l in data:
            if len(l.get_text().split()) <= 5:
                continue
            title = l.get_text().strip()
            if "href" in l.attrs:
                link = url_prefix + l.attrs["href"] if url_prefix is not None else l.attrs["href"]
            else:
                link = ''
            w.writerow([title, weight, timestamp, link])
    return


# End of File