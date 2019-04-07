import sys
import re

from urllib.request import urlopen
from collections import OrderedDict
import pandas as pd


def getencoding(http_file):

    P_ENC = r'\bcharset=(?P<ENC>.+)\b'
    headers = http_file.getheaders()
    dct = dict(headers)
    content = dct.get('Content-Type','')
    mt = re.search(P_ENC, content)

    if mt:
        enc = mt.group('ENC').lower().strip() # РІРёРґС–Р»РёС‚Рё РєРѕРґСѓРІР°РЅРЅСЏ
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


def find_weather(html_text):

    date_arr = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", "Субота", "Неділя"]
    rez = re.findall('\>.*?\<', html_text)
    newRez = list(filter(lambda x: x != '><' and x != '> <', rez))
    dic = OrderedDict({"день": ["мін", "макс"]})

    for item in range(len(newRez)):
        for day in date_arr:
            if day in newRez[item]:

                dic_key = " ".join(newRez[item:item+3]).replace("<", "").replace(">", "")
                dic_value1 = newRez[item+4].replace("&deg;", "").replace("<", "").replace(">", "")
                dic_value2 = newRez[item + 6].replace("&deg;", "").replace("<", "").replace(">", "")

                dic[dic_key] = list((dic_value1, dic_value2))

    return dic


def write_via_xlsx(dict, directory):
    dict = pd.DataFrame(dict)
    writer = pd.ExcelWriter(directory, engine='xlsxwriter')
    dict.to_excel(writer, sheet_name='Sheet1')
    writer.save()


if __name__ == '__main__':
    city = input("city: ")

    if len(city) == 0:
        city = "київ"

    if len(sys.argv) == 1:
        url = "https://ua.sinoptik.ua/" + urllib.parse.quote_plus("погода-%s" % city)

    else:
        url = sys.argv[1]

    http_file = urlopen(url)
    enc = getencoding(http_file)

    if enc:
        for line in http_file:
            s = str(line, encoding=enc)

    weather = find_weather(s)
    dir = "/home/stas/Documents/1.xlsx"
    write_via_xlsx(weather, dir)

