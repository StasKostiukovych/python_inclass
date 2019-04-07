# t29_01_refbook_db.py
# Телефонний довідник (db)
import sqlite3
import cgi
import datetime as dt
import html.parser
import os
from urllib.error import HTTPError
import openpyxl
import sys


HTML_PAGE = """
<html>
<title>Currency Converter</title>
<body>
<h3>Currency Converter</h3>
<br>

{}

<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>


From: 
</font>
{}

To:
</font>
{}
</br>

Cash:
</font>
<input type=text name=cash value="">
<input type=submit value="Convert">
</br>

</td>
<table>
</form>
</body>
</html>

"""



def convert(curr1, curr2, cash):

    try:
        conn = sqlite3.connect("currency.db")
        curs = conn.cursor()
        curs.execute("SELECT rate FROM currency WHERE cur1=? AND cur2=?", (curr1, curr2,))
        rate = curs.fetchone()
        conn.close()
        return '{} {} to {}\n<br>\nRate: {}<br>Converted cash: {}'.format(cash, curr1, curr2, round(rate[0], 3) ,round(cash * rate[0],3))

    except Exception as e:
        print(e)
        sys.exit(1)


def mkslct(name, values):

    select_block = '<select name="{0}">\n{1}</select>\n'

    option_block = '<option value="{0}">{0}</option>\n'

    return select_block.format(name, ''.join(option_block.format(v) for v in values))


def application(environ, start_response):
    """Викликається WSGI-сервером.
       Отримує оточення environ та функцію,
       яку треба викликати у відповідь: start_response.
       Повертає відповідь, яка передається клієнту.
    """
    if environ.get('PATH_INFO', '').lstrip('/') == '':

        # отримати словник параметрів, переданих з HTTP-запиту
        currency_list = ["USD", "UAH", "EUR", "RUB", "PLN", "CHF", "GBP"]
        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                        environ=environ)

        result = ''

        if 'cash' in form:
            cash = float(form['cash'].value)
            result = '{}'.format(convert(form.getvalue('list_currencies_0'), form.getvalue('list_currencies_1'), cash))
        body = HTML_PAGE.format(result, mkslct('list_currencies_0', currency_list), mkslct('list_currencies_1', currency_list))
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # якщо команда невідома, то виникла помилка
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain; charset=utf-8')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8047, application)
    httpd.serve_forever()


