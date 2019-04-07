import urllib.request
import json
import openpyxl
from openpyxl import load_workbook


import sqlite3


class CurencyConverter:

    def __init__(self, path_to_download):
        self.cur_array = []
        self.rez = 0
        self.path_to_download = path_to_download


        self.list_of_currency()
        self.final_write()


    #
    def rez_lst(self, key1, key2):
        url_prt1 = "https://free.currencyconverterapi.com/api/v6/convert?q="
        url_prt2 = "&compact=ultra&apiKey=782dddca2acbac7d3d84"
        key = key1 + "_" + key2
        url = url_prt1 + key + url_prt2
        req = urllib.request.Request(url)
        data = urllib.request.urlopen(req).read()
        data = json.loads(data.decode("utf-8"))
        return data[key]


    def list_of_currency(self):
        main_cur = ["USD", "UAH", "EUR", "RUB", "PLN", "CHF", "GBP"]
        lenth = len(main_cur)
        for i in range(lenth):
            for j in range(lenth):
                self.cur_array.append([main_cur[i], main_cur[j]])


    def final_write(self):
        for i in range(len(self.cur_array)):
            self.cur_array[i].append(self.rez_lst(self.cur_array[i][0], self.cur_array[i][1]))
        self.write_db(self.cur_array)


    def write_db(self, array):

        '''Створює довідник та записує у нього n записів.'''
        conn = sqlite3.connect("currency.db")  # зв'язатись з БД

        curs = conn.cursor()
        curs.execute('''CREATE TABLE currency (cur1, cur2, rate)''')

        for i in range(len(array)):

            curs.execute("INSERT INTO currency VALUES (?, ?, ?)",
                         (array[i][0], array[i][1], array[i][2]))

        conn.commit()
        conn.close()


CurencyConverter("currency.db")