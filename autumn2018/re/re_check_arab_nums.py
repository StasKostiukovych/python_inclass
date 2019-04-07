import docx
import re


CONV_TABLE = ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I'))


def roman_to_arab(txt):
    ret = 0
    for arab, roman in CONV_TABLE:
        while txt.startswith(roman):
            ret += arab
            txt = txt[ len(roman): ]
    return ret


def arab_to_roman(number):
   if number <= 0: 
       return False
   ret = str()
   for arab, roman in CONV_TABLE:
       while number >= arab:
           ret += roman
           number -= arab
   return ret


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


name = 'text.docx'
all_text = getText(name)
textlookfor = r"[IVXCDML]{1,10}"
allresult = re.findall(textlookfor, all_text)



result = True
for i in range(len(allresult)):
    print("text:",allresult[i])
    print("after:",arab_to_roman(roman_to_arab(allresult[i])))
    if allresult[i] != arab_to_roman(roman_to_arab(allresult[i])):
        result = False
        
print(result)
