#t27_31_wsgi_fib_web.py
#Обчислення чисел Фібоначчі через WSGI-сервер.

import cgi
import xml.etree.ElementTree as Et

HTML_PAGE = """<html>
<title>Books library</title>
<body>
<h3>Books library</h3>
<br>
{}
<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>

Author's surname:
<input type=text name=n_val1 value="">
<br>
Name of book:
<input type=text name=n_val2 value="">
<br>
Year:
<input type=text name=n_val3 value="">
<br>


</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="add">
</td>
<table>
</form>
</body>
</html>
"""


def to_xml(data, filename="books.xml"):
    name, author, year = data

    ID = 1
    inf = {"name": name,
           "author": author,
           "year": str(year)}

    try:
        e = Et.parse(filename)
        books = e.getroot()
        ID += int(books[-1].attrib["id"])

    except:
        books = Et.Element('Books')


    information = Et.Element('book')
    information.set("id", str(ID))

    name_book = Et.Element("name")
    name_book.text = inf["name"]

    author_book = Et.Element("author")
    author_book.text = inf["author"]

    year_book = Et.Element('year')
    year_book.text = inf["year"]

    information.append(name_book)
    information.append(author_book)
    information.append(year_book)

    books.append(information)

    e = Et.ElementTree(books)
    e.write(filename)

    return "success " + name


def application(environ, start_response):

    if environ.get('PATH_INFO', '').lstrip('/') == '':

        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                        environ=environ)
        result = ''
        if 'n_val1' in form and  'n_val2'  in form and 'n_val3'  in form:

            result = to_xml([form['n_val1'].value, form['n_val2'].value, form['n_val3'].value])

        else:
            result = "pls write smth in every block"

        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # якщо команда невідома, то виникла помилка
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8056, application)
    httpd.serve_forever()

