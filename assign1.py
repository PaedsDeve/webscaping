import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import sqlite3


def getData_Assign1():
    URL = "https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview"

    # driver = webdriver.Chrome(ChromeDriverManager().install())

    ser = Service("E:\\webscaping\chromedriver\chromedriver.exe")

    op = webdriver.ChromeOptions()
    op.headless
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)
    driver.get(URL)

    get_url = driver.current_url

    wait.until(EC.url_to_be(URL))

    if get_url == URL:
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        section = soup.find('section', attrs={"class", "col-sm-12"})
        rows_nme = section.find_all("td", attrs={"class", "variables-name"})
        rows_unit = section.find_all("td", attrs={"class", "variables-units"})
        rows_descr = section.find_all("td", attrs={"class", "variables-description"})

        a = 0

        if len(rows_nme) > 0:
            for row in rows_nme:
                if (rows_nme[a].text == "2m temperature"):

                    var_nme = rows_nme[a].text
                    var_unit = rows_unit[a].text
                    var_descrp = rows_descr[a].text

                    store_Assign1(var_nme, var_unit, var_descrp)

                elif (rows_nme[a].text == "Snowmelt"):

                    var_nme = rows_nme[a].text
                    var_unit = rows_unit[a].text
                    var_descrp = rows_descr[a].text

                    store_Assign1(var_nme, var_unit, var_descrp)

                a = a + 1
        else:
            print("No rows found")

    driver.close()


def getData_Assign2():
    URL = "https://grace.jpl.nasa.gov/data/get-data/monthly-mass-grids-land/"

    ser = Service("E:\\webscaping\chromedriver\chromedriver.exe")

    op = webdriver.ChromeOptions()
    op.headless
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)
    driver.get(URL)

    get_url = driver.current_url

    wait.until(EC.url_to_be(URL))

    if get_url == URL:
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        section = soup.find('section', attrs={"class", "content_page module content_page_template"})

        print(section)
        exit(0)

        rows_nme = section.find_all("td", attrs={"class", "variables-name"})
        rows_unit = section.find_all("td", attrs={"class", "variables-units"})
        rows_descr = section.find_all("td", attrs={"class", "variables-description"})

        a = 0

        if len(rows_nme) > 0:
            for row in rows_nme:
                if (rows_nme[a].text == "2m temperature"):

                    var_nme = rows_nme[a].text
                    var_unit = rows_unit[a].text
                    var_descrp = rows_descr[a].text

                    store_Assign1(var_nme, var_unit, var_descrp)

                elif (rows_nme[a].text == "Snowmelt"):

                    var_nme = rows_nme[a].text
                    var_unit = rows_unit[a].text
                    var_descrp = rows_descr[a].text

                    store_Assign1(var_nme, var_unit, var_descrp)

                    a = a + 1
                else:
                    print("No rows found")

    driver.close()



    # myhtml.find_element(By.XPATH, "/html/body")

    # r = requests.get(URL)
    # soup = BeautifulSoup(r.content, 'html.parser')

    # var_main = soup.find('div', attrs={"class", "main-container container-fluid js-quickedit-main-content"})
    # var_section = var_main.find('section', attrs={"class", "col-sm-12"})
    # test1 = var_section.find('div', attrs={"class", "region region-content container-fluid"})


def deleteOldRecords():
    conn = sqlite3.connect("articlesscrap.db")
    cursor = conn.cursor()
    cursor.execute("delete from assign1")
    cursor.close()
    conn.commit()

    ###########  Assign 2  ###########

    #cursor = conn.cursor()
    #cursor.execute("delete from assign2")
    #cursor.close()
    #conn.commit()

    ###########  Assign 3  ###########

    #cursor = conn.cursor()
    #cursor.execute("delete from assign3")
    #cursor.close()
    #conn.commit()

    conn.close()


def store_Assign1(var_nme, var_unit, var_descrp):
    conn = sqlite3.connect('articlesscrap.db')
    cursor = conn.cursor()

    data_tuple = (var_nme,
                  var_unit,
                  var_descrp)

    qry = '''insert into assign1(nme, unit, descrp) values(?, ?, ?)'''
    cursor.execute(qry, data_tuple)
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    deleteOldRecords()
    #getData_Assign1()
    getData_Assign2()