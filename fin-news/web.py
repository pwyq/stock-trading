# import os, zipfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#you have to download the chromedriver from selenium hq homepage
# chromedriver_path = '/usr/lib/chromium-browser/chromedriver'
chromedriver_path = '/usr/bin/chromedriver'
ext_dir = '/home/pwyq/github/stock-trading/third-parties/bypass-paywalls-chrome'



# ext_dir = 'extension'
ext_file = '/home/pwyq/github/stock-trading/third-parties/extension' # it auto add filetype

# Create zipped extension
# ## Read in your extension files
# file_names = os.listdir(ext_dir)
# file_dict = {}

# for fn in file_names:
#     if fn == ".github": # don't use `is` operator here
#         continue
#     else:
#         print(fn)
#         with open(os.path.join(ext_dir, fn), 'r') as infile:
#             file_dict[fn] = infile.read()

# ## Save files to zipped archive
# with zipfile.ZipFile(ext_file, 'w') as zf:
#     for fn, content in file_dict.items():
#         zf.writestr(fn, content)

# for root, dirs, files in os.walk(ext_dir):
#     for file in files
#         ziph.write(os.path.join(root, file))

shutil.make_archive(ext_file, 'zip', ext_dir)

# Add extension
chrome_options = webdriver.ChromeOptions()
ext_file += '.zip'
chrome_options.add_extension(ext_file)


driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
url = 'https://www.ft.com/content/2226adc7-f897-4fa3-abdc-ba2ca2183cfc'
# print(url)
# driver.implicitly_wait(1)
driver.get(url)



#login
#driver.find_element_by_css_selector('#Email').send_keys('email@gmail.com')
#driver.find_element_by_css_selector('#next').click()
#driver.find_element_by_css_selector('#Passwd').send_keys('1234')
#driver.find_element_by_css_selector('#signIn').click()


#get html
html = driver.page_source
print(html)
