import csv
import random
import undetected_chromedriver as uc
from shutil import which
from selenium.common.exceptions import TimeoutException
from time import sleep
from webbrowser import Chrome
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
chrome_path = "D:/RentPredictor/AutoCrawlData/chromedriver.exe"

list_url = []
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="bds_data"
)
mycursor = mydb.cursor()
sql = "INSERT INTO infohouse (ward,district,city,price,square,year) VALUES (%s,%s,%s,%s,%s,%s)"
for x in range(71, 101):
    adr = f"https://batdongsan.com.vn/cho-thue-nha-tro-phong-tro/p{str(x)}"
    list_url.append(adr)
for urlitem in list_url:
    chrome_options = Options()
    chrome_options.page_load_strategy = 'eager'
    driver = uc.Chrome(executable_path=chrome_path, options=chrome_options)
    driver.set_window_size(1920, 840)
    driver.get(urlitem)
    price = driver.find_elements(
        By.XPATH, "//a[@class='js__product-link-for-product-id']")
    list_href = []
    for x in price:
        list_href.append('https://batdongsan.com.vn/'+x.get_attribute('href'))
    driver.close()

    for x in list_href:
        op = Options()
        op.add_argument("--blink-settings=imagesEnabled=false")
        driver2 = uc.Chrome(executable_path=chrome_path, options=op)
        driver2.set_window_size(400, 400)
        driver2.get(x)
        diachi = ""
        gia = 0
        dientich = 0
        ngaydang = ""
        try:
            diachi_ele = driver2.find_element(
                By.XPATH, '//*[@id="product-detail-web"]/span')
            diachi = diachi_ele.text
        except:
            diachi = ""
        try:
            gia_ele = driver2.find_element(
                By.XPATH, '//*[@id="product-detail-web"]/div[1]/div[1]/span[2]')
            gia = gia_ele.text
        except:
            gia = 0
        try:
            dientich_ele = driver2.find_element(
                By.XPATH, '//*[@id="product-detail-web"]/div[1]/div[2]/span[2]')
            dientich = dientich_ele.text
        except:
            dientich = 0
        try:
            ngaydang_ele = driver2.find_element(
                By.XPATH, "//div[@class='re__pr-info pr-info js__product-detail-web']/*[last()]/div[1]/*[last()]")
            ngaydang = ngaydang_ele.text
        except:
            ngaydang = ""
        list_diachi = diachi.split(',')
        list_diachi.reverse()
        price = ""
        try:
            price = gia.split()[0]
        except:
            price = "0"
        try:
            square = dientich.split()[0]
        except:
            square = "0"
        try:
            year = ngaydang.split('/')[2]
        except:
            year = 0
        if (len(list_diachi) < 3):
            list_diachi += ["None"]*(4-len(list_diachi))
        row = (list_diachi[2].strip(), list_diachi[1].strip(),
               list_diachi[0].strip(), price, square, year)
        mycursor.execute(sql, row)
        mydb.commit()
        driver2.close()
