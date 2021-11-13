import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import requests
import time
import os
import sys
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)



dataz = {"CUSIP": [], "PRICE": [], "DATE":[]}
def get_data(cusip):
    driver.get("https://finra-markets.morningstar.com/MarketData/")                     
    dataz["CUSIP"].append(cusip)
    driver.find_element_by_css_selector("#ms-finra-autocomplete-box").send_keys(cusip)
    driver.find_element_by_css_selector("#ms-finra-quick-search > input.button_blue.autocomplete-go").click()

    try:
        time.sleep(2)
        timeStamp = time.time()
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.rtq-panel.rtq-msg.rtq-a-c-p > div.container > div.ctn > h5')))
        print("1 took:",time.time() - timeStamp)
        dataz["PRICE"].append(element.text)
        dataz["DATE"].append(element.text)
        
        
    except:
        time.sleep(3)
        timeStamp = time.time()
        frame = driver.find_element_by_css_selector('#ms-bond-detail-iframe')
        driver.switch_to.frame(frame)
        print("1 took:",time.time() - timeStamp)
        price = driver.find_element_by_css_selector("#price").text
        date = driver.find_element_by_css_selector("#msqt_summary > div:nth-child(3) > table > tbody > tr > td:nth-child(3) > span").text
        if price == "—":
            dataz["PRICE"].append("No data")
        else:
            dataz["PRICE"].append(price)
        if date == "—":
            dataz["DATE"].append("No data")
        else:
            dataz["DATE"].append(date)
        driver.switch_to.default_content()
        

    print(dataz)
    driver.switch_to.window(driver.window_handles[0])


vitus = open("cusip.txt").read().splitlines()

for vitu in vitus:
    get_data(vitu)

df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in dataz.items()]))
df.to_csv("cusipdatesss2.csv")
print(df)