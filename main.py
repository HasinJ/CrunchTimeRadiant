from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import shutil

from config import config
from ds import Node, LinkedList
from src.Scrapers.MenuMix import MenuMixScraper

from dateutil.relativedelta import relativedelta
import datetime
import time


class CrunchTime(config):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.driver.get('https://dbi1497.net-chef.com/ncext/index.ct')
        self._wait = WebDriverWait(self.driver, 10)
        self.LL4PC = LinkedList()  # PC linked list to count down arrows and reaching end

    def checkFolders(self, date):
        date = date.replace("/",".") # for folder use
        filepaths = [
            Path(f'./data'),
            Path(f'./data/MenuMix'),
            Path(f'./data/{self.LL4PC.head.PC}'),
            Path(f'./data/{self.LL4PC.head.PC}/{date}'),
        ]

        for dir in filepaths:
            if not (dir.exists()): dir.mkdir(parents=True, exist_ok=False)

        self.filepath = filepaths[-1] / f"MenuMix-{date}" # folder for downlaoding (for now)

    def printCurrentPage(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        print(soup.prettify())

    def clickByText(self, text):
        element = self._wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//*[text()='{text}']")))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def inputByText(self, text):
        element = self._wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//*[text()='{text}']")))
        actions = ActionChains(self.driver)
        actions.move_to_element(element).send_keys(text).perform()

    def login(self):
        time.sleep(2)
        #element = self.driver.find_element_by_xpath("//*[text()='Log in again']")
        self.clickByText("Log in again")
        time.sleep(2)

        self._wait.until(EC.presence_of_element_located(
            (By.NAME, "username"))).send_keys(self.getCrunchUser())
        self._wait.until(EC.presence_of_element_located(
            (By.NAME, "password"))).send_keys(self.getCrunchPass())

        self.clickByText("Sign In")

    def choosePC(self):
        element = self._wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "input")))
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        element = self._wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "input")))
        self.LL4PC.insertBeginning(Node(element.get_property("value")))
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(4)


class MenuMix(CrunchTime):
    def __init__(self, driver, dates):
        super().__init__(driver)
        self.dates = dates

    def download(self):
        printbtn = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@ces-selenium-id='gridexport_print']")))
        printbtn.click()
        time.sleep(2)

        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(2)

        counter = 0
        while not len(list(downloadPath.glob("MenuMix_*.csv"))):
            time.sleep(1)
            if counter==10:
                print("ERRORRRRRR")
                break #throw error
            counter+=1

        self.tempFile = list(downloadPath.glob("MenuMix_*.csv"))[0]

        if self.filepath.exists(): self.filepath.unlink()
        shutil.move(self.tempFile, self.filepath)

    def gotoSales(self):
        self.driver.get(
            "https://dbi1497.net-chef.com/ncext/next.ct#MenuMixSummary")

        self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[text()='Product Number']")))
        input = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@ces-selenium-id='cesdatefield_beginDate']")))
        input = input.find_element_by_tag_name('input')
        input.clear()
        input.send_keys(self.dates["start"])
        time.sleep(1)
        input = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@ces-selenium-id='cesdatefield_endDate']")))
        input = input.find_element_by_tag_name('input')
        input.clear()
        input.send_keys(self.dates["start"])

        btn = self._wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@ces-selenium-id='button_retrieveButton']")))
        ActionChains(self.driver).move_to_element(btn).click().perform()

        time.sleep(5)
        print("",self.LL4PC)


def get_past_date(str_days_ago, end=None):
    if end:
        TODAY = end
    else:
        TODAY = datetime.date.today()

    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return TODAY
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return date
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return date
    else:
        return "Wrong Argument format"


def today(dates):
    dates["days"] = 0
    hour = int(datetime.datetime.now().strftime('%H'))

    if hour >= 23:  # the half of the day
        dates["start"] = get_past_date('today').strftime("%m/%d/%Y")
        print(f"Auto date: use today's date\n{dates['start']}")

    elif hour < 23:  # the other half of the day
        dates["start"] = get_past_date('yesterday').strftime("%m/%d/%Y")
        print(f"Auto date: use yesterday's date\n{dates['start']}")

    return dates


def handleDates(dates):
    if dates["start"] == dates["end"] and (dates["start"] == None or dates["start"] == datetime.datetime.now().strftime('%x')):
        dates = today(dates)

    elif (dates["start"] == None and dates["end"] != None) or (dates["start"] != None and dates["end"] == None):
        raise ValueError(
            'Both dates need to be filled out, to choose one day:  dates = {"start": "7/28/2021", "end": "7/28/2021"}', dates["start"], dates["end"])

    else:
        print(f"Custom dates:\nFrom: {dates['start']} To: {dates['end']}")
        start = datetime.datetime.strptime(dates["start"], '%m/%d/%Y')
        end = datetime.datetime.strptime(dates["end"], '%m/%d/%Y')

        if not "days" in dates:
            dates["days"] = int(end.strftime("%j")) - int(start.strftime("%j"))
            dates["start"] = start.strftime("%m/%d/%Y")
            dates["end"] = end.strftime("%m/%d/%Y")
        else:
            dates["start"] = get_past_date(
                f'{dates["days"]} days ago', end).strftime("%m/%d/%Y")


if __name__ == "__main__":

    # ALL DATES INCLUSIVE
    # autopep8 -i my_file.py in case tabs are inconsistent in command prompt
    # get the amount of digits for month, day, and year correct (2 for month and day, 4 for year, probably)
    # ONE YEAR at a time
    ##
    # examples:
    # to choose one day:        dates = {"start": "07/28/2021", "end": "07/28/2021"}
    # to choose multiple days:  dates = {"start": "07/01/2021", "end": "07/31/2021"} (chooses all 31 days)
    # for normal runs:			dates = {"start": None, "end": None}

    dates = {"start": None, "end": None}
    try:
        handleDates(dates)
    except ValueError as err:
        print(err.args)
        exit()

    # download path
    downloadPath = Path.cwd() / ".temp"
    if not downloadPath.exists(): downloadPath.mkdir(parents=True, exist_ok=False)
    newOptions = webdriver.ChromeOptions()
    newOptions.add_experimental_option("prefs", {"download.default_directory" : (downloadPath).__str__() } );

    while dates["days"] >= 0:
        print(dates, "\n")

        root = webdriver.Chrome(executable_path = r".\chromedriver.exe", options = newOptions)

        selenium = MenuMix(root, dates)
        selenium.login()
        selenium.choosePC()
        selenium.gotoSales()
        selenium.checkFolders(dates["start"])
        selenium.download()

        # scrape

        # selenium.printCurrentPage()
        selenium.driver.quit()
        #selenium.deleteTemp()

        dates["days"] -= 1
        if dates["days"] >= 0:
            handleDates(dates)
