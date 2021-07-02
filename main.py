from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from config import config
from ds import Node, LinkedList
import datetime
import time

class CrunchTime(config):

    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.driver.get('https://dbi1497.net-chef.com/ncext/index.ct')
        self._wait = WebDriverWait(self.driver,5)
        self._LL4PC = LinkedList() #PC linked list to count down arrows and reaching end

    def printCurrentPage(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        print(soup.prettify())

    def clickByText(self, text):
        element = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[text()='{text}']")))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def inputByText(self, text):
        element = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[text()='{text}']")))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).send_keys(text).perform()

    def login(self):
        time.sleep(2)
        #element = self.driver.find_element_by_xpath("//*[text()='Log in again']")
        self.clickByText("Log in again")
        time.sleep(2)

        self._wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.getCrunchUser())
        self._wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(self.getCrunchPass())

        self.clickByText("Sign In")

    def choosePC(self):
        element = self._wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(4)

class MenuMix(CrunchTime):
    def __init__(self, driver):
        super().__init__(driver)

    def gotoSales(self):
        self.driver.get("https://dbi1497.net-chef.com/ncext/next.ct#MenuMixSummary")

        self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[text()='Product Number']")))
        parent = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@ces-selenium-id='griddockpanel']")))
        input = parent.find_element_by_tag_name('input')
        input.clear()
        ActionChains(self.driver).move_to_element(input).click().perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

        btn = parent.find_element_by_tag_name('a')
        ActionChains(self.driver).move_to_element(btn).click().perform()

        time.sleep(4)
        #self.printCurrentPage()


if __name__=="__main__":
    root = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\chromedriver.exe")
    task = MenuMix(root)
    task.login()
    task.choosePC()
    task.gotoSales()
    task.driver.quit()
