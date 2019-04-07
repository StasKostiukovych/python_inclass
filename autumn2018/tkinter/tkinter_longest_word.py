from tkinter import *


class Question:

    def __init__(self, main):

        self.entry1 = Entry(main, width=50, font=15)
        self.button1 = Button(main, text="Enter n")
        self.label1 = Label(main, width=0, font=20)
        self.label2 = Label(main, width=0, font=20,bg="red")
        self.label3 = Label(main, width=0, font=20)

        self.entry1.pack(fill=X)
        self.button1.pack(fill=X)
        self.label1.pack(side=LEFT)
        self.label2.pack(side=LEFT)
        self.label3.pack(side=LEFT)

        self.button1.bind("<Button-1>", self.answer)


    def answer(self, event):

        txt1 = self.entry1.get()
        answer1, start, end = self.find_the_longest(txt1)
        try:
            self.label1["text"] = txt1[:start]
            self.label2["text"] = answer1
            self.label3["text"] = txt1[end:]

        except ValueError:
            self.label1["text"] = "type someting"


    def find_the_longest(self, txt):

        longest = 1
        temp_longest = 1
        last_char = str()
        name_str = str()

        for char in txt:
            if char == last_char:
                temp_longest += 1
                if temp_longest > longest:
                    longest = temp_longest
                    name_str = char

            else:
                temp_longest = 1
            last_char = char

        rez = longest * str(name_str)

        return rez, txt.find(rez), txt.find(rez) + longest


root = Tk()
root.title("find the longest")

q = Question(root)

root.mainloop()
