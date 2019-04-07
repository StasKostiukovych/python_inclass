from tkinter import *
from math import *
from time import *


def Clock0(w):
    ny = w.winfo_height()
    nx = w.winfo_width()

    x0 = nx / 2
    radiys_x = 9 * nx / 20
    y0 = ny / 2
    radiys_y = 9 * ny / 20
    radiys = min(radiys_x, radiys_y)
    r0 = 0.9 * radiys
    r1 = 0.6 * radiys
    r2 = 0.8 * radiys
    r3 = 0.85 * radiys

    w.create_oval(x0-radiys, y0-radiys, x0+radiys, y0+radiys, width=7, fill="white")

    for i in range(1, 13):
        phi = pi/ 6*i
        x_start = x0 + r0 * sin(phi)
        y_start = y0 - r0 * cos(phi)
        x_end = x0 + r2 * sin(phi)
        y_end = y0 - r2 * cos(phi)
        w.create_line(x_start, y_start,x_end,y_end,width=radiys*0.015)

    for i in range(1, 720):
        phi = pi / 30 * i
        if i % 60 != 0:
            x_start1 = x0 + r0 * sin(phi)
            y_start1 = y0 - r0 * cos(phi)
            x_end1 = x0 + r3 * sin(phi)
            y_end1 = y0 - r3 * cos(phi)
            w.create_line(x_start1, y_start1, x_end1, y_end1, width=radiys*0.005)


    t = localtime()
    time_seconds = t[5]
    time_minutes = t[4] + time_seconds / 60
    time_hours = t[3] % 12 + time_minutes / 60

    phi = pi / 6 * time_hours
    x = x0 + r1 * sin(phi)
    y = y0 - r1 * cos(phi)
    w.create_line(x0, y0, x, y, arrow=LAST, fill="red", width=4)

    phi = pi / 30 * time_minutes
    x = x0 + r2 * sin(phi)
    y = y0 - r2 * cos(phi)
    w.create_line(x0, y0, x, y, arrow=LAST, fill="blue", width=3)



    phi = pi / 30 * time_seconds
    x = x0 + r2 * sin(phi)
    y = y0 - r2 * cos(phi)
    w.create_line(x0, y0, x, y, arrow=LAST)


def Clock(w):
    w.delete(ALL)
    Clock0(w)
    w.after(10, Clock, w)


root = Tk()
root.title("Python clock")

nx = 500
ny = 500

frame = Frame(root)
frame.pack(fill="both", expand=True)
w = Canvas(frame, width=nx, height=ny, bg="grey")
w.pack(fill="both", expand=True)

print(w.winfo_reqheight())

Clock(w)

root.mainloop()
