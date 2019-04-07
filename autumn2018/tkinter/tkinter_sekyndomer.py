
from tkinter import *
from datetime import datetime

root = Tk()
root.title('Stopwatch')

sec = 0 
h = 0  
after_id = ''  


def start_sw():
    btn1.grid_forget()
    btn2.grid(row=1, columnspan=2, sticky='ew')
    tick()


def continue_sw():
    btn3.grid_forget()
    btn4.grid_forget()
    btn2.grid(row=1, columnspan=2, sticky='ew')
    tick()


def reset_sw():
    global sec
    sec=0
    btn3.grid_forget()
    btn4.grid_forget()
    btn1.grid(row=1, columnspan=2, sticky='ew')
    label1.configure(text='00:00')



def stop_sw():
    btn2.grid_forget()
    btn3.grid(row=1,column=0,sticky='ew')
    btn4.grid(row=1, column=1, sticky='ew')
    root.after_cancel(after_id)


def tick():
    global sec, after_id, h
    after_id = root.after(1000, tick)
    if sec < 60 and h < 60:
        f_sec='%02d:%02d' % (h, sec)
        label1.configure(text=str(f_sec))
    elif sec == 60 and h < 60:
        h += 1
        sec -= 60
        f_sec = '%02d:%02d' % (h,sec)
        label1.configure(text=str(f_sec))
    else:
        stop_sw()

    sec += 1





label1 = Label(width=5, font=('Ubuntu', 100),text='00:00')
label1.grid(row=0, columnspan=2)  # columnspam = кількість стовпчиків які займає стовпчик

btn1 = Button(root, text='start', font=('Ubuntu', 30), command=start_sw)
btn2 = Button(root, text='stop', font=('Ubuntu', 30), command=stop_sw)
btn3 = Button(root, text='continue', font=('Ubuntu', 30), command=continue_sw)
btn4 = Button(root, text='reset', font=('Ubuntu', 30), command=reset_sw)


btn1.grid(row=1, columnspan=2, sticky='we')

root.mainloop()


