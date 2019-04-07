# t29_01_refbook_db.py
# Телефонний довідник (db)
import sqlite3


class Objects:

    def __init__(self, filename="objects.db"):
        self.filename = filename

    def create(self):


        conn = sqlite3.connect(self.filename)

        curs = conn.cursor()

        curs.execute("""
        CREATE TABLE objects
        (id integer primary key autoincrement, 
        type_of_bulding, 
        address, 
        area, 
        num_rooms);
        """)

        curs.execute("""
        CREATE TABLE rooms 
        (id integer primary key autoincrement,
         appointment ,
         area,
         objects_id integer not null,
         foreign key(objects_id) references objects(id));
         """)

        conn.commit()
        conn.close()


    def add_object(self, type_of_bulding, address,area, num_rooms):
        try:
            ID = self.get_id() + 1
        except:
            ID = 1

        conn = sqlite3.connect(self.filename)

        curs = conn.cursor()

        curs.execute("INSERT INTO objects VALUES (? ,?, ?, ?, ?)",(ID ,type_of_bulding, address, area, num_rooms))

        conn.commit()
        conn.close()
        return ID



    def add_rooms(self, appointment, area , objects_id):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("insert into rooms (appointment, area, objects_id) values (?, ?, ?)", (appointment, area, objects_id))
        conn.commit()
        conn.close()


    def print_rooms(self, ID):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        rez = curs.execute("select * from rooms where objects_id = (?);", (str(ID)))
        rooms_str = ""
        for row in rez.fetchall():
            smth = ""
            for i in range(1, len(row)-1):
                smth += str(row[i]) + " "
            rooms_str += smth+ "\n"


        conn.close()

        return rooms_str


    def return_objects(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        rez = curs.execute("SELECT * FROM objects")

        objects_dict = {}
        for row in rez.fetchall():
            form = ""

            for i in row:

                form += str(i) + " "
            objects_dict[row[0]] = form


        conn.close()
        return objects_dict


    def print_all(self):
        objects_dict = self.return_objects()
        all = ""
        for key_o , value_o in objects_dict.items():
            all += value_o
            all += "\nrooms: \n" + self.print_rooms(key_o) + "\n"

        print(all)


    def get_id(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        ID = curs.execute("SELECT MAX(id) FROM objects")
        ID = ID.fetchone()

        conn.close()

        return ID[0]

    def all_objects_with_type_and_area(self, type_b, area):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("SELECT id FROM objects WHERE type_of_bulding=? AND area=?", (type_b, area))
        arrayID = curs.fetchone()
        conn.close()

        objects_dict = self.return_objects()
        all = ""
        for key_o, value_o in objects_dict.items():
            if key_o in arrayID:
                all += value_o
                all += "\nrooms: \n" + self.print_rooms(key_o) + "\n"

            else:
                pass
                #all = "there are no buldings with type: {} and area {}".format(type_b, area)

        print(all)

o = Objects()

print("""
Operation modes:
1 - Create bd
2 - Add Objects and/or rooms
3 - Add room via ID of bulding
4 - Print All
5 - Print room via ID
6 - Find buldings by type and area
0 - Exit
""")



while True:
    k = int(input("enter operation mode: "))
    if k==1:
        try:
            o.create()
            print("Success")
        except:
            print("Already created!")

    elif k == 2:

        type_of_bulding = input("Enter type of bulding: ")
        address = input("Enter address: ")
        area = int(input("Enter area of object: "))
        num_rooms = int(input("Number of roooms: "))
        print("Would you like to add rooms? ")
        option = input("Enter (y) or (n) ")
        ID = o.add_object(type_of_bulding, address, area, num_rooms)
        if option == 'y':
            for i in range(num_rooms):
                room_info = input("Enter some information about room: ")
                room_area = int(input("Enter the area of the room: "))
                o.add_rooms(room_info, room_area, ID)
        print("Success!!!")

    elif k ==3 :
        ID = input("Enter num of object: ")
        room_info = input("Enter some information about room: ")
        room_area = int(input("Enter the area of the room: "))
        o.add_rooms(room_info, room_area, ID)
        print("Success!!!")

    elif k == 4:
        print("all objects: \n")
        o.print_all()

    elif k == 5:
        ID = int(input("Enter ID of Object: "))
        print(o.print_rooms(ID))

    elif k == 6:

        type_of_bulding = input("Enter type of bulding: ")
        area = int(input("Enter area of object: "))
        o.all_objects_with_type_and_area(type_of_bulding, area)

    elif k == 0:
        print("Thanks for working with me")
        break
