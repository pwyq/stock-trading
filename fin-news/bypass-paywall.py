import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chromedriver_path = '/usr/bin/chromedriver'
ext_path = '/home/pwyq/github/stock-trading/third-parties/'
ext_dir = ext_path + 'bypass-paywalls-chrome'
ext_file = ext_path + 'paywall' # it will auto add filetype

shutil.make_archive(ext_file, 'zip', ext_dir)

ext_file += '.zip'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(ext_file)


driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
url = 'https://www.ft.com/content/2226adc7-f897-4fa3-abdc-ba2ca2183cfc'
driver.get(url)

html = driver.page_source
print(html)

# TODO: post-processed the html

# End of File