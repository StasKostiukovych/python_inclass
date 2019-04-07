import cgi
import json


HTML_PAGE = """<html>
<title>Toys shop</title>
<body>
<h3>Toys shop</h3>
<br>
<br>
<form method=POST action=>
<table>
<tr>
<td align=right>


Price:
<input type=text name=n_val1 value="">
<br>
From (age):
<input type=text name=n_val2 value="">
<br>
To (age)
<input type=text name=n_val3 value="">
<br>

</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="submit">

<br>
RESULT_JSON: {}
</br>

</td>
<table>
</form>
</body>
</html>
"""


def find(agestart=None, ageend=None, price=None, name="toys.json"):
    rez = []
    with open(name) as file:
        inf = json.load(file)
    for templ_dict in inf:
        for key, value in templ_dict.items():
            if agestart and ageend and price:
                if value["price"] <= price and value["age(from)"] <= agestart and value["age(to)"] >= ageend:

                    rez.append(templ_dict)

            elif price and not agestart and not ageend:
                if value["price"] <= price:
                    rez.append(templ_dict)

            elif agestart and ageend and not price:
                if value["age(from)"] <= agestart and value["age(to)"] >= ageend:
                    rez.append(templ_dict)

            elif agestart and not ageend and not price:
                if value["age(from)"] >= agestart:
                    rez.append(templ_dict)

            elif ageend and not agestart and not price:
                if value["age(to)"] <= ageend:
                    rez.append(templ_dict)

    return json.dumps(rez)


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

        templ_price = None
        templ_age_s = None
        templ_age_e = None

        if 'n_val1' in form:
            templ_price = int(form["n_val1"].value)

        if 'n_val2' in form:
            templ_age_s = int(form["n_val2"].value)

        if 'n_val3' in form:
            templ_age_e = int(form["n_val3"].value)

        result = find(price=templ_price, agestart=templ_age_s, ageend=templ_age_e)

        body = HTML_PAGE.format(result) #application/json
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
    httpd = make_server('localhost', 8052, application)
    httpd.serve_forever()
