# T26_31 Отримання означення з вікіпедії за запитом.

import html.parser
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import datetime
import subprocess
import shlex

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

    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.pieces = []  # список частин тексту означення
        self.in_tag = False  # чи знаходимось ми усередині тегу <p>
        # self.in_p дорівнює
        # False до першого тегу <p>,
        # True всередині першого тегу <p>,
        # None після першого тегу <p>

    def handle_starttag(self, tag, attrs):
        '''Обробляє початковий тег tag (<p>).'''
        if tag == 'script' and self.in_tag != None:
            self.in_tag = True

    def handle_endtag(self, tag):
        '''Обробляє кінцевий тег tag (<p>).'''
        if tag == '/script':
            self.in_tag = None

    def handle_data(self, data):
        '''Обробляє дані data.'''
        if self.in_tag and "draw_clock" in data:
            self.pieces.append(data)

    @property
    def getdef(self):
        '''Повертає рядок означення.'''
        return ' '.join(self.pieces)


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
            rez = re.findall(r'(\d+,\d+,\d+,\d+,\d+,\d+)',self._def)[0]
            self._linux_set_time(rez)
        except HTTPError as e:
            print(e)


    @property
    def definition(self):
        return self._def


    def change_time(self, server_time):
        now = datetime.datetime.now()
        dt = datetime.datetime.strptime(server_time, '%Y,%m,%d,%H,%M,%S')
        print(now)
        print(dt)

        if now != dt:
            subprocess.call(['sudo', 'date', '-s', '{:}'.format(dt.strftime('%Y-%m-%d %H:%M:%S'))], shell=True)
            #print("success!!!")


    def _linux_set_time(self,  server_time):
        dt = datetime.datetime.strptime(server_time, '%Y,%m,%d,%H,%M,%S')
        time_string = dt.strftime('%Y-%m-%d %H:%M:%S')

        #subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
        subprocess.call(shlex.split("sudo date -s '%s'" % time_string), stdin=open("/home/stas/Downloads/1.txt"))
        subprocess.call(shlex.split("sudo hwclock -w"), stdin=open("/home/stas/Downloads/1.txt"))



if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        url = 'https://time.online.ua/in/kyiv/'
    else:
        url = sys.argv[1]
    wd = WikiDef(url)
    #print('Definition:', wd.definition)



