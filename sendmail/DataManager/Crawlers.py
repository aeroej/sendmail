import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import requests
from bs4 import BeautifulSoup
from Utils import utils


class AbsCrawler:
    def __init__(self):
        self._lines = None

    def crawl(self, url, issue_number):
        if issue_number is not None:
            self._lines = utils.read_file_lines(url+issue_number)
            self._lines.insert(0, 'issue')
        else:
            self._lines = utils.read_file_lines(url)
            self._lines.insert(0, 'manual')
        return self._lines


class Crawler:
    def __init__(self):
        self._html = []

    def crawl(self, url, issue_number):
        if issue_number is not None:
            try:
                expected_url = url+str(issue_number)
                req = requests.get(expected_url)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')
            except:
                print('URL'+str(issue_number)+' error')
        return str(soup)
