
import json
import pandas as pd
from bs4 import BeautifulSoup
import csv
import sys
from pathlib import Path


class MenuMixScrape():
    """docstring for MenuMixScrape."""

    def __init__(self):
        super().__init__()
        self.data = []
        self.columns = []

    def checkFolders(self):
        pass

    def scrapePC(self, html, PC):
        soup = BeautifulSoup(html, 'html.parser')
        self.data = []
        #results = soup.findAll("div", {"ces-selenium-id" : "component"})

        header = soup.findAll("span", {"class" : "x-column-header-text-inner"})
        header = list(map(lambda element: element.string.strip(), header))
        print(list(header))

        rows = soup.findAll("tr", {"role" : "row"})
        print(len(rows))




if __name__ == "__main__":
    task = MenuMixScrape()
    f = open(fr'C:\Users\Hasin\Desktop\Projects\CrunchTimeRadiant\src\Scrapers\MenuMix\html_tests\MenuMix.html','rb') # 'rb' stands for read-binary, write-binary needs chmoding, this also needs to be changed for Selenium (needs to have date)
    content = f.read()
    task.scrapePC(content,"9999")
    f.close()
