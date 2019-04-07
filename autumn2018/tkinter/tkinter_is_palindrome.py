from tkinter import *


def palindrome(n):
    if str(n) == str(n)[::-1]:
        return "yes"
    else:
        return "no"


def output(event):
    txt = entry1.get()
    try:
        label1["text"] = palindrome(txt)
    except ValueError:
        label1["text"] = "enter str"


root = Tk()
root.title("palindrome?")

entry1 = Entry(root, width=50, font=15)
button1 = Button(root, text="check")
label1 = Label(root, width=10, font=15)

entry1.grid(row=0, column=0)
button1.grid(row=0, column=1)
label1.grid(row=0, column=2)

button1.bind("<Button-1>", output)

root.mainloop()