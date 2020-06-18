import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


chromedriver_path = '/usr/bin/chromedriver'
ext_path = '/home/pwyq/github/stock-trading/third-parties/'
ext_dir = ext_path + 'bypass-paywalls-chrome'
ext_file = ext_path + 'paywall' # it will auto add filetype

shutil.make_archive(ext_file, 'zip', ext_dir)

ext_file += '.zip'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(ext_file)


driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
url = 'https://www.ft.com/content/2226adc7-f897-4fa3-abdc-ba2ca2183cfc'
url2 = 'https://www.ft.com/content/1ac26225-c5dc-48fa-84bd-b61e1f4a3d94'
driver.get(url)

html = driver.page_source

# TODO: post-processed the html
soup = BeautifulSoup(html, 'html.parser')
# <meta property="og:title" content="Donald Trump asked Xi Jinping for election help, John Bolton claims">
# <meta property="og:description" content="Former adviser calls US president ‘stunningly uninformed’ and ‘erratic’ in excerpts from book">
# <meta property="article:published_time" content="2020-06-18T03:18:24.625Z">


# <div class="article__content-body n-content-body js-article__content-body">

title = soup.find("meta", {"property":"og:title"})['content']
desc = soup.find("meta", {"property":"og:description"})['content']
pub_time = soup.find("meta", {"property":"article:published_time"})['content']
print(type(title))
# print(desc)
# print(pub_time)


x = soup.find(class_="article__content-body")
# print(x.get_text())
# x.aside.decompose() # remove <aside> content

unwanted = ['n-content-recommended--single-story', 'n-content-pullquote']

for t in unwanted:
    garbage = x.findAll(class_=t)
    for g in garbage:
        g.decompose()



# x = [t.decompose() for t in x.findAll('aside')]

# print(x.get_text())

output_file = "ft.txt" # TODO: consistent, manageble naming

with open(output_file, 'w') as f:
    f.write(title)
    f.write("\n")
    f.write(desc)
    f.write("\n")
    f.write(pub_time)
    f.write("\n")
    f.write(url)
    f.write("\n")
    f.write(x.get_text())

# TODO: modify bypass-paywall popup
# End of File