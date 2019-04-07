import cgi
import xml.etree.ElementTree as Et



HTML_PAGE = '''<html>
<title>Bookslibrary</title>
<body>
<h3>Books library</h3>
<br>
<br>
<form method=POST action=>
<table>
<tr>
<td align=right>


Name of book:
<input type=text name=n_val1 value="">
<br>
Author:
<input type=text name=n_val2 value="">
<br>
Year:
<input type=text name=n_val3 value="">
<br>

</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="submit">

<br>
RESULT: {}
</br>

</td>
<table>
</form>
</body>
</html>
'''



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

    #return "success" + name



def xml_parser(name=None, author=None, year=None,filename="books.xml"):

    flag1 = name and author and year
    flag2 = name and author
    flag3 = name
    flag4 = name and year
    flag5 = year
    flag6 = year and author
    flag7 = author

    e = Et.parse(filename)
    root = e.getroot()
    rez = []

    to_return = []


    for child in root:
        if flag1 or flag2 or flag3 or flag4:
            for book_name in child.iter("name"):
                if name == book_name.text:
                    rez.append(child.attrib['id'])


        elif flag1 or flag2 or flag6 or flag7:
            for book_author in child.iter("author"):
                if author == book_author.text:
                    rez.append(child.attrib['id'])

        elif flag1 or flag5 or flag6 or flag7 :
            for book_year in child.iter("year"):
                if year == book_year.text:
                    rez.append(child.attrib['id'])

        else:
            return ""


        for i in rez:
            if i == child.attrib['id']:
                templ_a = ''
                templ_n = ''
                templ_y = ''

                for book_name in child.iter("name"):
                    templ_n = book_name.text

                for book_author in child.iter("author"):
                    templ_a = book_author.text

                for book_year in child.iter("year"):
                    templ_y = book_year.text

                to_return.append("<br>" + templ_n + " " + templ_a + " "+  templ_y + "<br>")

    return "".join(to_return)




def application(environ, start_response):
    """Викликається WSGI-сервером.

       Отримує оточення environ та функцію,
       яку треба викликати у відповідь: start_response.
       Повертає відповідь, яка передається клієнту.
    """
    if environ.get('PATH_INFO', '').lstrip('/') == '':
        # отримати словник параметрів, переданих з HTTP-запиту
        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                        environ=environ)

        templ1 = None
        templ2 = None
        templ3 = None

        if 'n_val1' in form :
            templ1 = form["n_val1"].value

        if 'n_val2' in form :
            templ2 = form["n_val2"].value

        if 'n_val3' in form :
            templ3 = form["n_val3"].value

        result = xml_parser(templ1,templ2,templ3)

        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # якщо команда невідома, то виникла помилка
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8053, application)
    httpd.serve_forever()

