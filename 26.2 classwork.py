from urllib.request import urlopen, urlretrieve
from urllib.request import urlopen
from urllib.error import HTTPError
import sys
import html.parser
import re


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


def download(links):
    url_to_download = "http://www.matfiz.univ.kiev.ua"
    for link in links:
        page_url = url_to_download + link
        link2 = link.replace("userfiles/files/", "")
        result = urlretrieve(page_url, "/home/stas/Documents/testing26{}".format(link2))  # завантажуємо файл
    print(result[0], result[1], sep='\n')


class MyParser(html.parser.HTMLParser):

    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.pieces = []  #
        self.in_tag = False



    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self.in_tag != None:
            self.in_tag = True
            for name, value in attrs:
                if name == 'href' :
                    if ".py" in value or ".pyw" in value:
                        self.pieces.append(value)

    @property
    def getdef(self):
        return self.pieces


class WikiDef:

    def __init__(self, url):
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


    @property
    def definition(self):
        return self._def


if __name__ == '__main__':

    try:
        page = int(input("write_page_to_download:")) + 16
    except ValueError:
        page = 26

    if len(sys.argv) == 1:
        url = 'http://www.matfiz.univ.kiev.ua/pages/{}'.format(page)
    else:
        url = sys.argv[1]
    wd = WikiDef(url)
    download(wd.definition)

