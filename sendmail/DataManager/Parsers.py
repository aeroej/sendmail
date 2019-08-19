import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Utils import utils
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        pass

    def parse(self, project_name, data):
        if data[0] == 'issue':
            parser = IssueParser()
        elif data[0] == 'manual':
            parser = ManualParser()
        parsed = parser.parse(project_name, data[1:])
        parsed.insert(0, data[0])
        return parsed


class IssueParser:
    def __init__(self):
        pass

    def parse(self, project_name, data):
        parsed = data
        print('NOT YET IMPLEMENTED')
        return parsed


class ManualParser:
    def __init__(self):
        pass

    def parse(self, project_name, data):
        if project_name == 'atom':

        parsed = data
        print('NOT YET IMPLEMENTED')
        return parsed


class HtmlParser:
    def __init__(self):
        pass

    def parse(self, project_name, data):
        parsed = data
        print('NOT YET IMPLEMENTED')
        return parsed


class MarkdownParser:
    def __init__(self):
        pass

    def parse(self, project_name, data):
        if project_name == 'atom':
            lines = data[3:]
        lines = [line.strip() for line in lines if len(line.strip()) > 0]
        lines = [line for line in lines if not line.startswith('!')]

        string = ''
        for line in lines:
            string += line + ' '
        string = re.sub('(\(.*?\))', '', string)
        string = re.sub('(<.*?>)', '', string)
        string = string.replace('[', '').replace(']', '')
        string = string.replace('|', '').replace('-', '')
        string = string.replace('# ', '').replace('#', '').replace('* ', '')
        string = string.replace('`)', '').replace('*', ' ').replace(':', '')
        string = string.replace('`', '').replace("'", '').replace('"', '')
        string = string.replace('>', '').replace(',', '').replace('/', ' ')

        parsed = ''
        for line in string.split('. ')[:-1]:
            parsed += line + '\n'

        return parsed