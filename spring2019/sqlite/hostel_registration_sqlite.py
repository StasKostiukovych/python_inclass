import sqlite3
import cgi
import re



HTML_PAGE = """<html>
<title>registration</title>
<body>
<h3>Hotel registration</h3>
<br>
{}
<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>

Enter Your Name:
<input type=text name=n_val1 value="">
<br>

Days:
<input type=text name=n_val2 value="">
<br>

Type/number of room:
{}
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



class Guest:

    def __init__(self):
        self.name = None
        self.bayer = None
        self.room = None
        self.days = None


    def input(self):
        self.name = input("Enter surname: ")
        self.bayer = input("Enter year of birth: ")
        self.room = input("Enter room you wont: ")
        self.days = input("Enter days you wont to live there: ")

    def print(self):
        print(self.name, self.bayer, self.room, self.days, sep=", ")



class Hotel:

    def __init__(self, filename="registration.db"):

        self.filename = filename
        self.room_id = []
        self.func_room_id()

        self.type_rooms = {"Single": 99,
                           "Double": 149,
                           "Triple": 199,
                           "Quad": 249,
                           "Queen": 399,
                           "King": 499,
                           "Twin": 239}

        self.count_rooms = {"Single": 10,
                            "Double": 12,
                            "Triple": 4,
                            "Quad": 3,
                            "Queen": 2,
                            "King": 1,
                            "Twin": 4}


        self.descpiption = """Single: A room assigned to one person. May have one or more beds.
                            Double: A room assigned to two people. May have one or more beds.
                            Triple: A room assigned to three people. May have two or more beds.
                            Quad: A room assigned to four people. May have two or more beds.
                            Queen: A room with a queen-sized bed. May be occupied by one or more people.
                            King: A room with a king-sized bed. May be occupied by one or more people.
                            Twin: A room with two beds. May be occupied by one or more people."""



    def func_room_id(self):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        with conn:
            rez = cur.execute("SELECT * FROM hotel")
            for i in rez.fetchall():
                self.room_id.append(str(i[0]) + "-" + i[1])


    def rooms_to_sqlite(self):

        conn = sqlite3.connect(self.filename)  # зв'язатись з БД

        curs = conn.cursor()
        try:
            curs.execute('''CREATE TABLE hotel (id_room, type, guest_name, day_to_live, pay)''')
        except sqlite3.OperationalError:
            pass

        id_room = 1
        for key_type, value_type in self.type_rooms.items():
            for key_count, value_count in self.count_rooms.items():
                if key_type == key_count:
                    while value_count !=0:

                        # TODO write to sqlite
                        curs.execute("INSERT INTO hotel VALUES (?, ?, ?, ?, ?)",
                                     (id_room, key_type, "none", 0, 0))

                        id_room += 1
                        value_count-=1

        conn.commit()
        conn.close()
        return "success"

    def add(self, name, id, days, type_room):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        pay = int(days) * int(self.type_rooms[type_room])
        with conn:
            curs.execute("UPDATE hotel SET guest_name = (?) WHERE id_room = (?);",(name, id))
            curs.execute("UPDATE hotel SET day_to_live= (?) WHERE id_room = (?);",(days, id))
            curs.execute("UPDATE hotel SET pay= (?) WHERE id_room = (?);",(pay, id))


        return "success " + name + ", room # "+ str(id)


    def print_all(self):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        form = ""
        with conn:
            rez = cur.execute("SELECT * FROM hotel")
            for row in rez.fetchall():
                form += "\n<br>"
                for i in row:
                    form += str(i) + " "
        return form


    def mkslct(self, name, values):

        select_block = '<select name="{0}">\n{1}</select>\n'

        option_block = '<option value="{0}">{0}</option>\n'

        return select_block.format(name, ''.join(option_block.format(v) for v in values))


    def web_page(self, environ, start_response):


        if environ.get('PATH_INFO', '').lstrip('/') == '':

            form = cgi.FieldStorage(fp=environ['wsgi.input'],
                                environ=environ)

            if 'n_val1' in form and 'n_val2' in form:
                # TODO func that add to registration

                id_room, type_room = form.getvalue("list").split('-')
                result = self.add(form['n_val1'].value, int(id_room), int(form['n_val2'].value), type_room)

            else:
                result = "pls write smth in every block"
            body = HTML_PAGE.format(result, self.mkslct("list", self.room_id))
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        else:
            # якщо команда невідома, то виникла помилка
            start_response('404 NOT FOUND', [('Content-Type', 'text/plain; charset=utf-8')])
            body = 'Сторінку не знайдено'
        return [bytes(body, encoding='utf-8')]



    def connect(self):
        from wsgiref.simple_server import make_server
        print('=== Local WSGI webserver ===')
        httpd = make_server('localhost', 8047, self.web_page)
        httpd.serve_forever()





h = Hotel()
h.print_all()
