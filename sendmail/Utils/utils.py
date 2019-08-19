import re


def read_file_lines(file):
    return open(file, 'r', encoding='utf-8').readlines()


def make_string(lines, conj=' '):
    string = ''
    for line in lines:
        if len(line.strip()) > 0:
            string += line.strip()+conj
    return string


def string_arrange(string):
    #    string = string.replace('\n', ' ')
    string = re.sub('(\(*https://[^ ]*\))', '\n', string)
    string = re.sub('(\([^ ]*.md\))', '\n', string)
    string = re.sub('<.*?>', '\n', string)
    string = string.replace('[','\n').replace(']', '\n')
    string = string.replace('|','\n').replace('-','\n')
    string = string.replace(':', '\n').replace('/', '\n')
    string = string.replace('*','\n').replace(',','').replace('#','\n')
    string = string.replace('(`', '\n').replace('`)', '\n').replace('`','\n')
    string = string.replace('"','\n').replace(')', '\n')
    string = string.strip()
    return string


def write_to_file(file, string, mode='a'):
    with open(file, mode, encoding='utf-8') as f:
        f.write(string)
