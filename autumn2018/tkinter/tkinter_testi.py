from tkinter import *
import collections
import re


class Tests:

    def __init__(self, master, dic, answer_dict):
        self.dic = dic
        self.buttonDic = {}
        self.answer_dict = answer_dict

        for key, values in self.dic.items():
            self.label = Label(master, text=key)
            self.label.grid(sticky='w')
            for value in values:
                self.buttonDic[value] = 0

                self.buttonDic[value] = IntVar()
                self.aCheckButton = Checkbutton(master, text=value, variable=self.buttonDic[value])
                self.aCheckButton.grid(sticky='w')

        self.submitButton = Button(master, text="Submit", command=self.query_checkbuttons)
        self.submitButton.grid()


    def query_checkbuttons(self):

        output_dict = collections.defaultdict(list)
        true_answer = collections.defaultdict(list)
        false_answer = collections.defaultdict(list)
        quantity_true = 0

        for key, value in self.buttonDic.items():
            state = value.get()
            for questions, answers in self.dic.items():
                for answer in answers:
                    if answer == key and state != 0:
                        output_dict[questions].append(key)

        for keys1, values1 in self.answer_dict.items():
            for keys2, values2 in output_dict.items():

                for i in values1:
                    for j in values2:
                        if i == j:
                            true_answer[keys1].append(i)
                            quantity_true += 1
                        else:
                            false_answer[keys1].append(i)

        print(true_answer)

        top = Toplevel()
        f = Frame(top)
        f.pack(side=LEFT)
        Label(f, text="Your answer: ").pack()
        for key, values in output_dict.items():
             Label(f, text=key).pack()
             Label(f, text=values).pack()

        Label(f, text="True answer: "+str(quantity_true)).pack()


        f1 = Frame(top)
        f1.pack(side=LEFT)
        Label(f1, text="True answer: ").pack()
        for key, values in true_answer.items():
            Label(f1, text=key).pack()
            Label(f1, text=values).pack()

"""
my_dic = {"question1": ("a)lol", "b)kek", "c)sadq", "d)dadqw"),
          "question2": ("a)qwdxd", "b)sdfwec", "c)wcsqasq", "d)qqfcww"),
          "question3": ("a)qwe1das", "b)qwdqwas", "c)qdwd", "d)dqdw")}

answer_dic = {"question1": ["a)lol"],
              "question2": ["b)sdfwec"],
              "question3": ["c)qdwd"]}
"""

my_path = r"C:\Users\Stas\Documents\Test_z_informatiki.txt"
my_path1 = r"C:\Users\Stas\Documents\true_answer.txt"

def return_dict_of_question(path, path1):
    f = open(path, 'r')
    text = f.read()
    f1 = open(path1, "r")
    text1 = f1.read()

    question = re.findall('^[0-9].*', text, re.MULTILINE)
    answers = re.findall('^[a-г].*', text, re.MULTILINE)
    question1 = re.findall('^[0-9].*', text1, re.MULTILINE)
    answers1 = re.findall('^[a-г].*', text1, re.MULTILINE)

    c = []
    temporary = []
    for i in range(len(answers)):
        temporary.append(answers[i])
        if i < len(answers) - 1:
            if answers[i + 1][0] == 'а':
                c.append(temporary)
                temporary = []
        else:
            c.append(temporary)

    dict_with_questions_answers = {}

    for i in range(len(question)):
        dict_with_questions_answers[question[i]] = c[i]

    dict_with_true_answers = {}
    for i in range(len(question1)):
        dict_with_true_answers[question1[i]] = [answers1[i]]

    return dict_with_questions_answers, dict_with_true_answers


my_dic, answer_dic = return_dict_of_question(my_path, my_path1)
#print(my_dic)
#print(answer_dic)
root = Tk()
Tests(root, my_dic, answer_dic)
root.mainloop()