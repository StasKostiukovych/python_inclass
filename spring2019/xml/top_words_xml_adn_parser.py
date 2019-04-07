import html.parser
from urllib.request import urlopen
from urllib.error import HTTPError
from collections import defaultdict, OrderedDict
import re
import xml.etree.ElementTree as et



def getencoding(http_file):
    P_ENC = r'\bcharset=(?P<ENC>.+)\b'

    headers = http_file.getheaders()
    dct = dict(headers)
    content = dct.get('Content-Type','')
    mt = re.search(P_ENC, content)
    if mt:
        enc = mt.group('ENC').lower().strip()
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


class MyParser(html.parser.HTMLParser):

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = re.sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()



class Top_words:

    def __init__(self, url, filename='refs.xml'):

        self.filename = filename
        self.url = url
        self._def = ''
        self.rez = defaultdict(int)
        http_file = urlopen(self.url)
        enc = getencoding(http_file)

        request = urlopen(self.url)
        data = str(request.read(), encoding=enc, errors='ignore')
        parser = MyParser()
        parser.feed(data)

        self._def = parser.text()
        self.count_words(self._def)
        self.createrb()


    def count_words(self, data):
        data = re.sub('[!.,:;]', '', data)
        data = re.findall(r'(\w*) ', data)

        for word in data:
            self.rez[word] += 1

        self.rez = OrderedDict(sorted(self.rez.items(), key=lambda kv: kv[1], reverse=True))


    def createrb(self):
        xml_list = et.Element('list_of_words')
        # проходимо по всіх словах і створюємо відповідні вузли, як це робиться у програмі 28_21_refbook_xml.py
        for word, i in self.rez.items():
            tmp_word = et.Element('word')
            tmp_word.set("count", str(i))
            tmp_word.text = word
            xml_list.append(tmp_word)

        # створюємо об'єкт xml і записуємо його у файл
        e = et.ElementTree(xml_list)
        e.write("classwork.xml")


    @property
    def definition(self):
        return self._def


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        url = 'https://www.bbc.com/news/world-asia-47634132'
    else:
        url = sys.argv[1]
    wd = Top_words(url)

