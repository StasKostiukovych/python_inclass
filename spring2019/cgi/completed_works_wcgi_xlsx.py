import cgi


HTML_PAGE = """<html>
<title>registration</title>
<body>
<h3>Hotel registration</h3>
<br>

<br>
<br>
<form method=POST action={}>
<table>
<tr>
<td align=right>

Type of act:
{}
<br>


</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="select">
</td>
<table>
</form>
</body>
</html>
"""


GROUNDS_HTML = """
ID:
<input type=text name=n_val1 value="">
<br>

Name:
<input type=text name=n_val2 value="">
<br>

Adress:
<input type=text name=n_val3 value="">
<br>

Responsible:
<input type=text name=n_val4 value="">
<br>

Manager:
<input type=text name=n_val5 value="">
<br>

<tr>
<td colspan=2 align=center>
<input type="submit" value="Submit" name="Submit1" />
</td>
"""

WORKS_HTML = """
ID:
<input type=text name=n_val1 value="">
<br>

Name:
<input type=text name=n_val2 value="">
<br>

<tr>
<td colspan=2 align=center>
<input type="submit" value="Submit" name="Submit2" />
</td>
"""


ACTS_HTML = """
ID:
<input type=text name=n_val1 value="">
<br>

No:
<input type=text name=n_val2 value="">
<br>

Date:
<input type=text name=n_val3 value="">
<br>

Sum:
<input type=text name=n_val4 value="">
<br>

S_id:
<input type=text name=n_val5 value="">
<br>

<tr>
<td colspan=2 align=center>
<input type="submit" value="Submit" name="Submit3" />
</td>
"""

POINTS_HTML = """
W_id:
<input type=text name=n_val1 value="">
<br>

A_id:
<input type=text name=n_val2 value="">
<br>

<tr>
<td colspan=2 align=center>
<input type="submit" value="Submit" name="Submit4" />
</td>
"""


class Works:

    def __init__(self, ground_xlsx="ground.xlsx", works_xlsx="works.xlsx",
                 acts_xlsx="acts.xlsx", points_xlsx="points.xlsx"):

        self.ground_xlsx = ground_xlsx
        self.works_xlsx = works_xlsx
        self.acts_xlsx = acts_xlsx
        self.points_xlsx =points_xlsx
        self.info_list = ["Майданчики", "Роботи", "Акти", "Пункти"]


    def mkslct(self, name, values):

        select_block = '<select name="{0}">\n{1}</select>\n'

        option_block = '<option value="{0}">{0}</option>\n'

        return select_block.format(name, ''.join(option_block.format(v) for v in values))


    def one_of_four(self, option):
        if option == "Майданчики":
            return GROUNDS_HTML

        elif option == "Роботи":
            return WORKS_HTML

        elif option == "Акти":
            return ACTS_HTML

        elif option == "Пункти":
            return POINTS_HTML

    def web_page(self, environ, start_response):

        if environ.get('PATH_INFO', '').lstrip('/') == '':

            form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)


            result = form.getvalue("list")

            if "Submit1" in form:
                templ = 1

            elif "Submit2" in form:
                templ = 2

            elif "Submit1" in form:
                templ = 3

            elif "Submit4" in form:
                templ = 4
            else:
                templ = "Couldn't determine which button was pressed."

            body = HTML_PAGE.format(self.one_of_four(result) ,self.mkslct("list", self.info_list) )

            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        else:

            start_response('404 NOT FOUND', [('Content-Type', 'text/plain; charset=utf-8')])
            body = 'Сторінку не знайдено'

        return [bytes(body, encoding='utf-8')]



    def connect(self):
        from wsgiref.simple_server import make_server
        print('=== Local WSGI webserver ===')
        httpd = make_server('localhost', 8046, self.web_page)
        httpd.serve_forever()

w = Works()
w.connect()
