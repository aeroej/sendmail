import argparse
from sendmail.DataManager.DataManager import DataManager
#from DatabaseManager.DatabaseManager import DatabaseManager
#from Classifier.Classifier import Classifier
#from ResultManager.ResultManager import ResultManager


class Core():
    def __init__(self):
        self.project_name = None
        self.user_manual_url = None
        self.issues_url = None
        self.start_num = None
        self.end_num = None

    def set_params(self, project_name, user_manual_url, issues_url, start_num=1, end_num=2):
        self.project_name = project_name
        self.user_manual_url = user_manual_url
        self.issues_url = issues_url
        self.start_num = start_num
        self.end_num = end_num

    def data_manage(self, zip_path=None, issue_num=None):
        dm = DataManager()
        htmls = {}
        for issue_num in range(self.start_num, self.end_num+1):
            crawled = dm.crawl(self.issues_url, issue_num)

            if zip_path is not None:
                dm.compress_to_zip(crawled, './'+self.project_name+'_'+str(issue_num)+'.html', zip_path)

            if 'doc' in htmls.keys():
                htmls['doc'].append('./'+self.project_name+'_'+str(issue_num)+'.html')
            else:
                htmls['doc'] = [ './'+self.project_name+'_'+str(issue_num)+'.html' ]

        return htmls


#python main.py --project_name vscode --user_manual https://github.com/microsoft/vscode-docs/ --issues https://github.com/microsoft/vscode/issues/
