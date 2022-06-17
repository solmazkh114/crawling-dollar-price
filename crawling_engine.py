from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


class crawling_app:
    url = 'https://www.tgju.org/profile/price_dollar_rl/history'
    def __init__(self, no_page=10):
        self.no_page = no_page  #number of pages we want navigate for extracting data

    def __define_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver

    def __extract_desired_html(self, html_doc):
        soup = BeautifulSoup(html_doc, features="lxml")
        table = soup.find_all('tbody', {'id': 'table-list'})
        return table

    def __extracted_data_from_html(self, html_data):
        extracted_data_list = []
        start1 = "<tr"
        end1 = "</tr>"
        data = str(html_data).split(start1)
        start2 = '<td>'
        end2 = '</td>'
        for i in range(1, len(data)):
            tmp = [x.split(end2)[0] for x in str(data[i]).split(start2)]
            # print(len(tmp))
            try:
                tmp[5] = tmp[5].split(">")[1].split("<")[0]
                tmp[6] = tmp[6].split(">")[1].split("<")[0]
            except:
                tmp[5] = 0
                tmp[6] = 0
            tmp_clean = [re.sub(',', '', str(x)) for x in tmp]
            extracted_data_list.append(tmp_clean[1:])
        return extracted_data_list

    def extract_data(self):
        driver = self.__define_driver()
        driver.get(self.url)
        page_source = driver.page_source
        output = self.__extracted_data_from_html(self.__extract_desired_html(page_source))
        print(type(output))
        sleep(5)
        for i in range(1, self.no_page):
            link = driver.find_element(value="DataTables_Table_0_next")
            driver.implicitly_wait(10)
            link.click()
            sleep(5)
            page_source_next = driver.page_source
            tmp1 = self.__extracted_data_from_html(self.__extract_desired_html(page_source_next))
            output = output + tmp1
        df = pd.DataFrame(output, columns=["Open", "Low", "High", "Close", "Rate_change", "Percent_change", "Date",
                                           "Solar_date"])
        df = df[1:]
        df.to_csv("data/history_dollar_price.csv", index=False)


