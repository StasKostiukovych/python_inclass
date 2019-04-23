import urllib.request
import json

class CurencyConverter:

    def __init__(self):
        self.cur_array = []
        self.rez = 0
        self.list_of_currency()
        self.final_write()

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
        main_cur = ["USD", "UAH", "EUR", "GBP"]
        lenth = len(main_cur)
        for i in range(lenth):
            for j in range(lenth):
                if i !=j:
                    self.cur_array.append([main_cur[i], main_cur[j]])

    def final_write(self):
        dic = {}
        for i in range(len(self.cur_array)):
            dic[self.cur_array[i][0] + "_" + self.cur_array[i][1]] = self.rez_lst(self.cur_array[i][0], self.cur_array[i][1])
        self.to_json(dic)

    def to_json(self, dict, name = "currency.json"):

        try:
            data = json.load(open(name))
        except:
            data = []

        data.append(dict)

        with open(name, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return "success"

c = CurencyConverter()