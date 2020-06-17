from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# Constants
HEADERS = {
    'Host': 'www.bloomberg.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': '*/*',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.bloomberg.com/quote/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'TE': 'Trailers'
}
URL_ROOT = 'https://www.bloomberg.com/markets2/api/datastrip'
URL_PARAMS = 'locale=en&customTickerList=true'
VALID_TYPE = {'currency', 'index'}


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, headers=HEADERS)) as resp:
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

# End of File
