import re
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Utils import utils
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        pass

    def parse(self, project, str_list, tp):
        if tp == 'html':
            parser = HtmlParser()
        elif tp == 'komodo':
            parser = KomodoParser()
        else:
            parser = MarkdownParser()
        return parser.parse(project, str_list)


class HtmlParser:
    def __init__(self):
        self.titleBlock = 'title'
        self.labelBlock = 'a.sidebar-labels-style,box-shadow-nonewidth-full,d-block,IssueLabel,v-align-text-top'
        self.contextBlock = 'div.edit-comment-hide > task-lists > table > tbody > tr > td'
        self.commentsBlock = 'div.js-discussion.js-socket-channel > div.js-timeline-item.js-timeline-progressive-focus-container > \
        div.timeline-comment-wrapper.js-comment-container > div.timeline-comment-group.js-minimizable-comment-group > \
        div.unminimized-comment.comment.previewable-edit.js-comment.js-task-list-container.timeline-comment > \
        div.edit-comment-hide > task-lists > table.d-block > tbody.d-block > tr.d-block > \
        td.d-block.comment-body.markdown-body.js-comment-body'

    def parse(self, project, line_list):
        title, labels, content, comments, number = None, None, None, None, None
        lines = line_list
        string = utils.make_string(lines)
        soup = BeautifulSoup(string, 'html.parser')

        def _get_content(ps):
            context = ''
            for p in ps:
                p = p.getText().strip(' ').strip('\n')
                p = p.split()
                for word in p:
                    try:
                        context += str(word) + ' '
                    except:
                        continue
                context = context.strip()
            return context[:-1]

        def _get_comment(pss):
            comments = []
            for ps in pss:
                ps = ps.select('p')
                context = _get_content(ps)
                comments.append(context)
            return comments

        try:
            temp = soup.find(self.titleBlock).string.split(' ')
            if project == 'vscode':
                title = utils.make_string(temp[:-7])
            else:
                title = utils.make_string(temp[:-10])
            number = temp[-5].strip('#')
        except:
            pass
        try:
            labels = [x.string for x in soup.select(self.labelBlock)]
        except:
            pass
        try:
            content = _get_content(soup.select_one(self.contextBlock).select('p'))
        except:
            pass
        try:
            comments = _get_comment(soup.select(self.commentsBlock))
        except:
            pass

        if None in [title, labels, content, comments, number]:
            return 'err'

        def _arrange(string):
            string = re.sub('(\(.*?\))', '', string)
            string = re.sub('(<.*?>)', '', string)
            string = string.replace('[', '').replace(']', '')
            string = string.replace('|', '').replace('-', '')
            string = string.replace('# ', '').replace('#', '').replace('* ', '')
            string = string.replace('`)', '').replace('*', ' ').replace(':', '')
            string = string.replace('`', '').replace("'", '').replace('"', '')
            string = string.replace('>', '').replace(',', '').replace('/', ' ')
            return string

        return _arrange(title), labels, _arrange(content), comments, number


class MarkdownParser:
    def __init__(self):
        pass

    def parse(self, project, line_list):
        lines = line_list[9:]
        lines = [line.strip() for line in lines if len(line.strip()) > 0]
        lines = [line for line in lines if not line.startswith('!')]

        string = ''
        for line in lines:
            string += line+' '
        string = re.sub('(\(.*?\))', '', string)
        string = re.sub('(<.*?>)', '', string)
        string = string.replace('[', '').replace(']', '')
        string = string.replace('|', '').replace('-', '')
        string = string.replace('# ', '').replace('#', '').replace('* ', '')
        string = string.replace('`)', '').replace('*', ' ').replace(':', '')
        string = string.replace('`', '').replace("'", '').replace('"', '')
        string = string.replace('>' ,'').replace(',', '').replace('/', ' ')

        text = ''
        for line in string.split('. ')[:-1]:
            text += line+'\n'
        return text


class KomodoParser:
    def __init__(self):
        pass

    def parse(self, project, line_list):
        string = utils.make_string(line_list)
        soup = BeautifulSoup(string, 'html.parser')
        soup = soup.find('body')
        soup = soup.find('main')
        soup = soup.find('article')
        soup = str(soup)

        string = soup.replace('\n', '!@#$')
        string = self._string_arrange(string)

        string = string.split('!@#$')
        string = utils.make_string(string, conj='\n')
        return string

    def _string_arrange(self, string):
        string = re.sub('<footer.*?</footer>', '', string)
        string = re.sub('<aside.*?</aside>', '', string)
        string = re.sub('<.*?>', '', string)
        string = string.strip()
        return string