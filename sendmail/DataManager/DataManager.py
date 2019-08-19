from sendmail.DataManager.Crawlers import AbsCrawler, Crawler
from sendmail.DataManager.Parsers_local import Parser
from sendmail.DataManager.Preprocessors import WordProcessor, Preprocessor
import zipfile

class DataManager:
    def __init__(self):
        pass

    def crawl(self, url, issue_number):
        crawler = Crawler()
        html = crawler.crawl(url, issue_number)
        return html

    def parse(self, project_name, data):
        parser = Parser()
        args = parser.parse(project_name, data)
        return args

    def compress_to_zip(self, data, data_path, zip_path):
        open(data_path, 'w', encoding='utf-8').write(data)
        try:
            issue_zip = zipfile.ZipFile(zip_path, 'x')
            issue_zip = zipfile.ZipFile(zip_path, 'w')
        except:
            issue_zip = zipfile.ZipFile(zip_path, 'a')
        
        issue_zip.write(data_path, data_path, compress_type=zipfile.ZIP_DEFLATED)

    def word_process(self, data):
        preprocessor = WordProcessor()
        words = preprocessor.pre_process(data)
        return words
