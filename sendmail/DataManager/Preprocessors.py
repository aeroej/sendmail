from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from autocorrect import spell


class WordProcessor:
    stop_words = list(set(stopwords.words('english')))

    def __init__(self):
        pass

    def pre_process(self, data):
        tp = data[0]
        text = data[1:]
        if tp == 'issue':
            title, labels, content, _, num_comments = text.split('\n')
            lines = [title, content]
        else:
            lines = text.split('\n')

        processed_words = []
        for line in lines:
            words = line.split(' ')
            for word in words:
                word = word.lower()
                word = self._remove_non_alpha(word)
                if word == '':
                    continue
                else:
                    word = self._typos_correcting(word)
                    word = self._eliminate_stop_word(word)
                    if word == '':
                        continue
                    else:
                        word = self._stemming(word)
                        processed_words.append(word)
        return processed_words

    def _remove_non_alpha(self, word):
        if str.isalpha(word):
            return word
        else:
            return ''

    def _typos_correcting(self, word):
        word = spell(word)
        return word

    def _eliminate_stop_word(self, word):
        if not word in WordProcessor.stop_words:
            return word
        else:
            return ''

    def _stemming(self, word):
        return PorterStemmer().stem(word)

class Preprocessor:
    def __init__(self):
        pass
