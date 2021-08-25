
import json
import pandas as pd
from bs4 import BeautifulSoup
import csv
import sys
from os import path


class MenuMixScrape():
    """docstring for MenuMixScrape."""

    def __init__(self):
        super().__init__()
        self.data = []
        self.columns = []

    def scrape(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.data = []
        #results = soup.findAll("div", {"ces-selenium-id" : "component"})

        

if __name__ == "__main__":
    task = MenuMixScrape()
    f = open(fr'C:\Users\Hasin\Desktop\Projects\CrunchTimeRadiant\src\Scrapers\MenuMix\html_tests\MenuMix.html','rb') # 'rb' stands for read-binary, write-binary needs chmoding, this also needs to be changed for Selenium (needs to have date)
    content = f.read()
    task.scrape(content)
    f.close()
