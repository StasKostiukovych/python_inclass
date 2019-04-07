#t27_31_wsgi_fib_web.py
#Обчислення чисел Фібоначчі через WSGI-сервер.

import cgi
import json

HTML_PAGE = """<html>
<title>Toys shop</title>
<body>
<h3>Toys shop</h3>
<br>
{}
<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>

Name of toy:
<input type=text name=n_val1 value="">
<br>
Price:
<input type=text name=n_val2 value="">
<br>
From (age):
<input type=text name=n_val3 value="">
<br>
To (age)
<input type=text name=n_val4 value="">
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

def to_json(toy_dict, name="toys.json"):
    try:
        data = json.load(open(name))
    except:
        data = []

    data.append(toy_dict)

    with open("toys.json", "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return "success  "+ " ".join(toy_dict)


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
        result = ''
        if 'n_val1' in form and  'n_val2'  in form and 'n_val3'  in form and 'n_val4' in form:
            result = to_json({form['n_val1'].value :
                                  {"price": int(form['n_val2'].value),
                              "age(from)":int(form['n_val3'].value),
                             "age(to)": int(form['n_val4'].value)}})

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
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()

