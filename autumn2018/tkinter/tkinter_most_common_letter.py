from tkinter import *


class Question:

    def __init__(self, main):

        self.entry1 = Entry(main, width=50, font=15)
        self.entry2 = Entry(main, width=50, font=15)
        self.button1 = Button(main, text="compare",width=10)
        self.button2 = Button(main, text="close",command=main.quit ,width=10)
        self.label1 = Label(main, width=0, font=20)

        self.entry1.grid(row=0, column=0)
        self.entry2.grid(row=1, column=0)
        self.button1.grid(row=0, column=1)
        self.button2.grid(row=1,column=1)
        self.label1.grid(row=3, column=0)

        self.button1.bind("<Button-1>", self.answer)

    def answer(self, event):

        txt1 = self.entry1.get()
        txt2 = self.entry2.get()
        try:
            self.label1["text"] = self.compare(txt1,txt2)
        except ValueError:
            self.label1["text"] = "type someting"

    def compare(self, a,b):
        end_str = str()
        for i in range(len(a)):
            if a[i] not in b:
                end_str += a[i]
        return end_str


root = Tk()
root.title("most common letter")

q = Question(root)

root.mainloop()
