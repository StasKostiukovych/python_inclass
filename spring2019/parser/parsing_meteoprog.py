import html.parser
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import pandas as pd


def getencoding(http_file):
    P_ENC = r'\bcharset=(?P<ENC>.+)\b'

    headers = http_file.getheaders()
    dct = dict(headers)
    content = dct.get('Content-Type', '')
    mt = re.search(P_ENC, content)
    if mt:
        enc = mt.group('ENC').lower().strip()
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


class MyParser(html.parser.HTMLParser):

    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.pieces = {}  # список частин тексту означення
        self.in_tag = False  # чи знаходимось ми усередині тегу <p>
        self.i = 0
        # self.in_p дорівнює
        # False до першого тегу <p>,
        # True всередині першого тегу <p>,
        # None після першого тегу <p>

    def handle_starttag(self, tag, attrs):
        if tag == 'li' and self.in_tag != None:
            self.in_tag = True

            for name, value in attrs:
                templ_temper = ""


                if name == "title":
                    temperature = value.split(",")[0]
                    min = temperature.split(".")[0]
                    max = temperature.split(".")[-1]
                    templ_temper = (min, max)
                    self.pieces[self.i] = templ_temper
                    self.i += 1

    @property
    def getdef(self):
        '''Повертає рядок означення.'''
        return self.pieces


class Parser:

    def __init__(self, url, city):
        self.city = city
        self.url = url
        self._def = ''
        http_file = urlopen(self.url)
        enc = getencoding(http_file)

        try:
            request = urlopen(self.url)
            data = str(request.read(), encoding=enc, errors='ignore')
            parser = MyParser()
            parser.feed(data)
            self._def = parser.getdef

        except HTTPError as e:
            print(e)

        self.write_via_xlsx(self._def, "prognoz.xlsx")


    def write_via_xlsx(self, dic, directory):
        dic = pd.DataFrame(dic)
        writer = pd.ExcelWriter(directory, engine='xlsxwriter')
        dic.to_excel(writer, sheet_name=self.city)
        writer.save()

    @property
    def definition(self):
        return self._def



if __name__ == '__main__':
    import sys
    city = input("Enter city:")
    if city == "":
        city = "Kyiv"

    if len(sys.argv) == 1:
        url = 'https://www.meteoprog.ua/ua/weather/{}/'.format(city)
    else:
        url = sys.argv[1]
    a = Parser(url, city)

    #print(a.definition)


