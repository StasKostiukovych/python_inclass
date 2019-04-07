import cgi
import json


HTML_PAGE = """<html>
<title>longest substring</title>
<body>
<h3>longest substring</h3>
<br>
{}
<br>
<br>
<form method=POST action="classwork_action.py">
<table>
<tr>
<td align=right>
<font size="5" color="blue" face="Arial">
Enter str:
</font>
</td>
<td>
<input type=text name=n_val value="">
</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="tap">
</td>
<table>
</form>
</body>
</html>
"""


def longest_sym(strng):
    len_substring = 0
    longest = 0

    rez_dic = {}
    for i in range(len(strng)):
        if i > 1:
            if strng[i] != strng[i - 1]:
                len_substring = 0
        len_substring += 1
        if len_substring > longest:
            longest = len_substring
            char = strng[i]

    return json.dumps({"symbol": char, "number": longest})


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
        if 'n_val' in form:
            n = str(form['n_val'].value)
            result = 'longest({}) = {}'.format(n, longest_sym(n))
        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/application/json; charset=utf-8')])
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

