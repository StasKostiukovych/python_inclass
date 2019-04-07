import sqlite3
import cgi

HTML_PAGE = """<html>
<title>registration</title>
<body>
<h3>Hotel info</h3>
{}
</body>
</html>
"""


def print_all(filename="registration.db"):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    form = ""
    with conn:
        rez = cur.execute("SELECT * FROM hotel")
        for row in rez.fetchall():
            form += "\n<br>"
            for i in row:
                form += str(i) + " "
    return form



def application(environ, start_response):

    if environ.get('PATH_INFO', '').lstrip('/') == '':
        result = print_all()
        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:

        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()