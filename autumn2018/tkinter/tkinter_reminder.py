from tkinter import *
from datetime import *
import time


root = Tk()


def close():
   root.destroy()


def show():
   top = Toplevel(root)
   top.overrideredirect(True)
   top.geometry("{0}x{1}+0+0".format(top.winfo_screenwidth(), top.winfo_screenheight()))
   top.configure(bg='black')
   Label(top, text=str(entry_event.get()), fg='white', bg='black', font=('Helvetica', 30)).place(anchor='center', relx=0.5, rely=0.5)
   close_button = Button(top, text='click to end', font='Helvetica', bg="white", fg="black",command=close)
   close_button.pack()



def hide():

   root.withdraw()
   time_to_sleep_time = set_time_to_sleep.get()
   time_to_sleep_data = set_data_to_sleep.get()

   data_now = datetime.now()

   data = datetime.strptime(time_to_sleep_data + " " + time_to_sleep_time, "%d-%m-%Y %H:%M:%S")
   time_to_sleep = data - data_now
   time.sleep(time_to_sleep.total_seconds())
   show()


label_time = Label(root, text="time")
label_time.grid(row=0, column=0)

label_data = Label(root, text="data")
label_data.grid(row=1, column=0)

label_reminder = Label(root, text="event")
label_reminder.grid(row=2, column=0)

entryText = StringVar()
set_time_to_sleep = Entry(root)
set_data_to_sleep = Entry(root, textvariable=entryText)
entryText.set("27-11-2018")

entry_event = Entry(root)
entry_event.grid(row=2, column=1)


set_time_to_sleep.grid(row=0, column=1)
set_data_to_sleep.grid(row=1, column=1)

button = Button(text='Set', command=hide)
button.grid(row=0, column=2)

root.mainloop()
