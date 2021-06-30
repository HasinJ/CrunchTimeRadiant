from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time

class CrunchTime():

    def __init__(self,driver):
        self.driver = driver
        self.driver.get('https://dbi1497.net-chef.com/ncext/index.ct')

    def login(self):
        time.sleep(2)



if __name__=="__main__":
    root = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\chromedriver.exe")
    task = CrunchTime(root)
    task.login()
    task.driver.quit()
