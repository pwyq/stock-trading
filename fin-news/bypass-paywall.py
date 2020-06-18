from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import shutil


def get_html(url):
    driver.get(url)
    return driver.page_source


def process_html_ft(output_path, html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("meta", {"property":"og:title"})['content']
    desc = soup.find("meta", {"property":"og:description"})['content']
    pub_time = soup.find("meta", {"property":"article:published_time"})['content']
    body = soup.find(class_="article__content-body")

    unwanted_tags = ['n-content-recommended--single-story', 'n-content-pullquote']
    for t in unwanted_tags:
        garbage = body.findAll(class_=t)
        for g in garbage:
            g.decompose()

    with open(output_path, 'w') as f:
        f.write(title)
        f.write("\n")
        f.write(desc)
        f.write("\n")
        f.write(pub_time)
        f.write("\n")
        f.write(url)
        f.write("\n")
        f.write(body.get_text())


if __name__ == '__main__':
    ext_path = '/home/pwyq/github/stock-trading/third-parties/'
    ext_dir = ext_path + 'bypass-paywalls-chrome'
    ext_file = ext_path + 'paywall' # it will auto add filetype

    shutil.make_archive(ext_file, 'zip', ext_dir) # requries zip as extention
    ext_file += '.zip'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension(ext_file)

    driver = webdriver.Chrome(executable_path=const.PATH_CHROMEDRIVER, options=chrome_options)

    # TODO: get urls from other files
    url = 'https://www.ft.com/content/2226adc7-f897-4fa3-abdc-ba2ca2183cfc'
    # url2 = 'https://www.ft.com/content/1ac26225-c5dc-48fa-84bd-b61e1f4a3d94'
    
    raw_html = get_html(url)

    output_file = "ft.txt" # TODO: consistent, manageble naming
    process_html_ft(output_file, raw_html)

    # TODO: modify bypass-paywall popup

# End of File