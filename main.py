from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from config import config
from ds import Node, LinkedList

from dateutil.relativedelta import relativedelta
import datetime
import time

class CrunchTime(config):

    def __init__(self,driver):
        super().__init__()
        self.driver = driver
        self.driver.get('https://dbi1497.net-chef.com/ncext/index.ct')
        self._wait = WebDriverWait(self.driver,10)
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
        element = self._wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
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

        time.sleep(1)
        #self.printCurrentPage()


def get_past_date(str_days_ago,end=None):
    if end: TODAY = end
    else: TODAY = datetime.date.today()

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
	dates["days"]=0
	hour = int(datetime.datetime.now().strftime('%H'))

	if hour >= 23: #the half of the day
		dates["start"] = get_past_date('today').strftime("%m/%d/%Y")
		print(f"Auto date: use today's date\n{dates['start']}")

	elif hour < 23: #the other half of the day
		dates["start"] = get_past_date('yesterday').strftime("%m/%d/%Y")
		print(f"Auto date: use yesterday's date\n{dates['start']}")

	return dates


def handleDates(dates):

	if dates["start"]==dates["end"] and (dates["start"]==None or dates["start"]==datetime.datetime.now().strftime('%x')): dates=today(dates)

	elif (dates["start"]==None and dates["end"]!=None) or (dates["start"]!=None and dates["end"]==None):
		raise ValueError('Both dates need to be filled out, to choose one day:  dates = {"start": "7/28/2021", "end": "7/28/2021"}', dates["start"], dates["end"])

	else:
		print(f"Custom dates:\nFrom: {dates['start']} To: {dates['end']}")
		start = datetime.datetime.strptime(dates["start"], '%m/%d/%Y')
		end = datetime.datetime.strptime(dates["end"], '%m/%d/%Y')

		if not "days" in dates:
			dates["days"] = int(end.strftime("%j")) - int(start.strftime("%j"))
			dates["start"] = start.strftime("%m/%d/%Y")
			dates["end"] = end.strftime("%m/%d/%Y")
		else:
			dates["start"] = get_past_date(f'{dates["days"]} days ago', end).strftime("%m/%d/%Y")




if __name__=="__main__":

	## ALL DATES INCLUSIVE
	## get the amount of digits for month, day, and year correct (2 for month and day, 4 for year, probably)
	## one year at a time
	##
	## examples:
	## to choose one day:        dates = {"start": "07/28/2021", "end": "07/28/2021"}
	## to choose multiple days:  dates = {"start": "07/01/2021", "end": "07/31/2021"} (chooses all 31 days)
	## for normal runs:			 dates = {"start": None, "end": None}

	dates = {"start": None, "end": None}
	try: handleDates(dates)
	except ValueError as err:
		print(err.args)
		exit()


	while dates["days"] >= 0:
		print(dates,"\n")

		root = webdriver.Chrome(executable_path=r".\chromedriver.exe")
		task = MenuMix(root)
		task.login()
		task.choosePC()
		task.gotoSales()
		task.driver.quit()


		dates["days"]-=1
		if dates["days"] >= 0: handleDates(dates)
