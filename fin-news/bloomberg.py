import requests
import json
from urllib.parse import quote


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


# Scraper
def scraper(object_id: str = None, object_type: str = None, timeout: int = 5) -> list:
    """
    Get the Bloomberg data for the given object.
    :param object_id: The Bloomberg identifier of the object.
    :param object_type: The type of the object. (Currency or Index)
    :param timeout: Maximal number of seconds to wait for a response.
    :return: The data formatted as dictionary.
    """
    object_type = object_type.lower()
    if object_type not in VALID_TYPE:
        return list()
    # Build headers and url
    object_append = '%s:%s' % (object_id, 'IND' if object_type == 'index' else 'CUR')
    headers = HEADERS
    headers['Referer'] += object_append
    url = '%s/%s?%s' % (URL_ROOT, quote(object_append), URL_PARAMS)
    # Make the request and check response status code
    response = requests.get(url=url, headers=headers)
    if response.status_code in range(200, 230):
        return response.json()
    return list()

# Index
object_id, object_type = 'IBVC', 'index'
data = scraper(object_id=object_id, object_type=object_type)
print('The open price for %s %s is: %d' % (object_type, object_id, data[0]['openPrice']))
# The open price for index IBVC is: 50094

# Exchange rate
object_id, object_type = 'EUR', 'currency'
data = scraper(object_id=object_id, object_type=object_type)
print('The open exchange rate for USD per {} is: {}'.format(object_id, data[0]['openPrice']))
# The open exchange rate for USD per EUR is: 1.0993