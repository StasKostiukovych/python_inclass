import cgi
import my_parsers
import urllib.request
import json
import re
import sqlite3
import datetime

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EasyShop.com</title>
</head>
<body>
<form method=POST action="">
    <h1 style="text-align: center">Enter name of item to find</h1>

    <p style="text-align: center">
        <input size=50 type=text name=to_search value=""><br>

    <table align="center" style="text-align: center">
    <tr>
        <td>Type sort: </td>
        <td>
            <select name="type_sort">
                <option value="relevant">Relevant</option>
                <option value="cheap">Price low to high</option>
                <option value="fresh">What's new</option>
            </select>
        </td>
        <td>Gender: </td>
        <td>
            <select name="gender">
                <option value="any">any</option>
                <option value="man">man</option>
                <option value="woman">woman</option>
            </select>
        </td>

        <td>Size: </td>
        <td>
        {}
        </td>

        <td>Number of pages: </td>
        <td>
            <select name="num">
                <option value="3">3</option>
                <option value="5">5</option>
                <option value="7">7</option>
            </select>
        </td>
    </tr>
    </table>

    <table align="center" style="text-align: center">
        <tr>
        <td>Choose shops: </td>
        <td>
            <input type="checkbox" name="shops" value="Asos" checked>Asos.com
            <input type="checkbox" name="shops" value="Amazon" checked>Amazon.com
            <input type="checkbox" name="shops" value="Rozetka" checked>Rozetka.com
        </td>
        </tr>
    </table>
    
    <table>

        <tr>
            <td>Show event log by start - end time:<br></td>
            <td>From:</td>
            <td>
                {}
            </td>
    
            <td>
                {}
            </td>
            <td>To:</td>
            <td>
                {}
            </td>
    
            <td>
                {}
            </td>
        <tr>
        
    </table>

    <table align="center" style="text-align: center">
        <tr>
            <td>
                <button name="submit" value="Search">Search</button>
                <button name="submit" value="Show">Show</button>
            </td>
        </tr>

    </table>

    {}
</form>
</body>
</html>
"""


item_table_descr = """
<table>
    <tr>
    <td>
        <b><pre>Ціна                Посилання на товар</pre></b>
        <b><pre>Ціна зі знижкою     Опис</pre></b>
    </td>
</table>
"""

item_tables = """

<table>
    <tr>
    <td>
        <pre>{}               <a href="{}">{}</a></pre><br />
        <pre>{} {}</pre>
    </td>
</table>
"""

show_info_form = """

"""


def make_listbox(name, values):
    select_block = '<select name="{0}">\n{1}</select>\n'

    option_block = '<option value="{0}">{0}</option>\n'

    return select_block.format(name, ''.join(option_block.format(v) for v in values))

def convert(val_str, to_valuta="UAH"):

    with open("currency.json") as file:
        inf = json.load(file)

    val_arr = val_str.split("-")

    if len(val_arr) > 1:

        if val_arr[0].startswith("$"):
            req = "USD_" + to_valuta
            coef = inf[-1][req]

            return str(round(coef * float(val_arr[0].strip()[1:]))) + " - " \
                   + str(round(coef * float(val_arr[-1].strip()[1:])))

    else:
        if val_str.startswith("£"):
            req = "GBP_" + to_valuta
            coef = inf[-1][req]
            return str(round(coef * float(val_str[1:])))

        elif val_str.startswith("$"):
            req = "USD_" + to_valuta
            coef = inf[-1][req]
            return str(round(coef * float(val_str[1:])))

        else:
            return val_str.strip()


class AllInfoBd:
    def __init__(self, filename="info.db"):
        self.filename = filename

        try:
            self.create()
        except sqlite3.OperationalError:
            pass

    def create(self):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute("""
        CREATE TABLE all_info
        (id integer primary key autoincrement, 
        time timestamp,
        type_request,
        request, 
        type_sort, 
        gender, 
        size, 
        num);
        """)

        curs.execute("""
        CREATE TABLE sites 
        (id integer primary key autoincrement,
         name_site,
         href,
         price,
         sale_price,
         descr,
         other_info,
         sites_id integer not null,
         foreign key(sites_id) references objects(id));
         """)

        conn.commit()
        conn.close()

    def add_all_info(self, type_request, request, type_sort, gender, size, num):

        time = datetime.datetime.now() #.strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

        curs = conn.cursor()

        curs.execute("INSERT INTO all_info (time, type_request, request, type_sort, gender, size, num) VALUES (?, ?, ? ,? ,? , ?, ?)", (time, type_request, request,
                                                                            type_sort, gender, size, num))

        ID = curs.execute("SELECT MAX(id) FROM all_info")
        ID = ID.fetchone()[0]
        conn.commit()
        conn.close()
        return ID

    def add_sites(self, name_site, href, price, sale_price, descr, other_info, sites_id):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("insert into sites (name_site ,href , price, sale_price, descr, other_info, sites_id) "
                     "values (?, ?, ? ,? ,? , ?, ?)", (name_site, href, price, sale_price, descr, other_info, sites_id))
        conn.commit()
        conn.close()


    def return_info(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        rez = curs.execute("SELECT * FROM all_info")
        info = rez.fetchall()
        conn.close()
        return info

    def return_sites(self, ID):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        select_id = "SELECT * FROM sites Where sites.sites_id={}".format(str(ID))
        rez = curs.execute(select_id)

        sites = rez.fetchall()
        conn.close()
        return sites

    def print_all(self):
        info_array = self.return_info()
        to_print = ""

        for info in info_array:
            to_print += "<b>"
            for something in info:
                to_print += str(something) + " "

            to_print += "</b><br>\n"

            for site_descr in self.return_sites(info[0]):
                to_print += str(site_descr) + "<br><br>\n"

            to_print += "<br>\n"
        return to_print

    def info_with_time(self, start_time, end_time):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        rez = curs.execute("SELECT * FROM all_info WHERE strftime('%Y-%m-%d', time) BETWEEN (?) AND (?);",(start_time, end_time))
        info_array = rez.fetchall()
        conn.close()
        to_print = ""

        for info in info_array:
            to_print += "<b>"
            for something in info:
                to_print += str(something) + " "

            to_print += "</b><br>\n"

            for site_descr in self.return_sites(info[0]):
                to_print += str(site_descr) + "<br><br>\n"

            to_print += "<br>\n"
        return to_print


class Server(AllInfoBd):
    def __init__(self):

        AllInfoBd.__init__(self)
        self.list_sizes = ["None"] + [str(i) for i in range(35, 49)] + ["XXS", "XS", "S", "M", "L", "XL", "XXL"]
        self.days = ["0" + str(i) for i in range(1, 10)] + [str(i) for i in range(10, 32)]
        self.month = ["0" + str(i) for i in range(1, 10)] + ["10", "11", "12"]



    def combine_shops(self, shops, request, type_sort, gender, size, num):

        ID = self.add_all_info("request", request, type_sort, gender, size, num)
        all_info = []

        if type(shops) == str:
            shops = [shops]

        if len(shops) == 0:
            return "", ID

        for shop in shops:

            if shop == "Asos":
                all_info.append(my_parsers.Asos(request, type_sort, gender, size, num))

            elif shop == "Amazon":
                all_info.append(my_parsers.Amazon(request, type_sort, gender, size, num))

            elif shop == "Rozetka":
                all_info.append(my_parsers.Rozetka(request, type_sort, gender, size, num))

        return all_info, ID

    def info_to_form(self, info, sites_id):
        full_info = ""

        if len(info) == 0:
            return ""

        for shop in info:

            price = ""
            sale_price = ""

            if len(list(shop.keys())) !=0:
                site = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', list(shop.keys())[0])[0]
                site = str(site).replace("https://", "")
            else:
                site = ""
            full_info += '<h1 style="text-align: center">{}</h1>'.format(site)

            for link, information in shop.items():

                href = link
                descr = ""
                descr_bd = ""
                other_info = ""

                if information["price"] != "NaN":

                    for name, value in information.items():

                        if name == "price":

                            price = convert(value)

                        elif name == "sale price":
                            sale_price = convert(value)

                        elif name == "size":
                            sizes = "<b>Також доступні опції(розмри): </b>" + ", ".join(value) + "<br>\n"
                            sizes = "<br>".join([sizes[i:i+150] for i in range(0, len(sizes), 150)])
                            descr += sizes
                            descr_bd += str(value) + "\n"

                        elif name == "description":

                            d = "<br>".join([value[i:i+150] for i in range(0, len(value), 150)])
                            descr += "<b>Про товар: </b>" + d
                            descr_bd += str(value)

                        else:
                            descr += "<b>" + name + "</b> : " + value + "<br>\n"
                            other_info += str(name) + " : " + str(value) + "\n"

                full_info += item_tables.format(price, href, site, sale_price, descr)
                self.add_sites(site, href, price, sale_price, descr_bd, other_info, sites_id)

            full_info += "<br>\n"

        return item_table_descr +"<br>" + full_info

    def application(self, environ, start_response):
        request = ""
        type_sort = "relevant"
        gender = "any"
        size = "None"
        num = 3
        shops = []

        if environ.get('PATH_INFO', '').lstrip('/') == '':
            result = ""
            form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

            if form["submit"].value == "Search":
                if 'to_search' in form:

                    request = form['to_search'].value

                    type_sort = form.getvalue("type_sort")
                    gender = form.getvalue("gender")
                    size = form.getvalue("size")
                    num = form.getvalue("num")
                    shops = form.getvalue("shops")  # array

                info, ID = self.combine_shops(shops, request, type_sort, gender, size, int(num))
                result = self.info_to_form(info, ID)

            elif form["submit"].value  == "Show":

                start_time = str(2019) + "-" + str(form.getvalue("month_from")) + "-" + str(form.getvalue("day_from"))
                end_time = str(2019) + "-" + str(form.getvalue("month_to")) + "-" + str(form.getvalue("day_to"))
                result = self.info_with_time(start_time, end_time)

            body = HTML_PAGE.format(make_listbox("size", self.list_sizes),
                                    make_listbox("day_from", self.days),
                                    make_listbox("month_from", self.month),
                                    make_listbox("day_to", self.days),
                                    make_listbox("month_to", self.month), result)

            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        else:

            start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
            body = 'Сторінку не знайдено'

        return [bytes(body, encoding='utf-8')]

    def start_server(self):
        from wsgiref.simple_server import make_server
        print('=== Local WSGI webserver ===')
        httpd = make_server('localhost', 8051, self.application)
        httpd.serve_forever()


if __name__ == '__main__':
    s = Server()
    s.start_server()
