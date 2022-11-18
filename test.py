from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import sys

url = 'https://www.brainyquote.com/'
chrome_driver_path = 'E:\\webscaping\chromedriver\chromedriver.exe'
s = Service('E:\\webscaping\chromedriver\chromedriver.exe')

chrome_options = Options()
chrome_options.add_argument('--headless')

op = webdriver.ChromeOptions()
op.headless
webdriver = webdriver.Chrome(service=s, options=op)
webdriver.get(url)


# default search query
search_query = "life"

if (len(sys.argv) >= 2):
    search_query = sys.argv[1]
    print(search_query)

with webdriver as driver:
    # Set timeout time
    wait = WebDriverWait(driver, 10)

    # retrive url in headless browser
    driver.get(url)

    # find search box
    search = driver.find_element(By.ID, "hmSearch")
    search.send_keys(search_query + Keys.RETURN)


    wait.until(presence_of_element_located((By.ID, "quotesList")))
    # time.sleep(3)
    #results = driver.find_element('m-brick')

    print(search)

    exit(0)

    #for quote in results:
     #   quoteArr = quote.text.split('\n')
     #   print(quoteArr)
     #   print()

    # must close the driver after task finished
    driver.close()