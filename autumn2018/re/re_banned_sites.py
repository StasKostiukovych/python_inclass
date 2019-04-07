# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:11:50 2018

@author: Stas
"""

import re
import datetime
import pickle
import collections

P_IP = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'

#P_SITE = r'http?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

P_SITE = r"https://(?:[-\w.])+"

P_DATE = r"(\d{1,2}\.\d{1,2}\.\d{4}|\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4})"

P_TIME = r"(\d{1,2}\:\d{1,2})"

P_WORKER = r'\s'.join([P_IP, P_SITE, P_DATE, P_TIME])



def process_file(fname, errname):
    '''Обробляє файл fname з відомостями про робітників

    Очікуваний формат даних, наприклад:
    123.321.555.228 https://habr.com 18.01.2018 18:55
    Неправильні рядки записує у файл errname
    '''
    workers = {}                       # словник з даними студентів
    pat_worker = re.compile(P_WORKER, re.VERBOSE)
    g = open(errname, "w")
    f = open(fname,"r")
    errcount = 0
    i = 0
    for line in f:
        i+=1
        try:
            process_line(line, workers, pat_worker, i)    # обробити 1 рядок файлу
        except ValueError:
            errcount += 1
            g.write(line)
    if errcount != 0:
        print("Неправильних записів:", errcount)

    f.close()
    g.close()
    return workers



def process_line(line, workers, pat_work, iterat):
    '''Обробляє рядок line з відомостями про студентів та додає його
    до словника workers.

    Очікуваний формат даних, наприклад:
    123.321.555.228 https://habr.com 18.01.2018 18:55
    '''
    x = line.split()           
    line = ' '.join(x)  # залишити по 1 пропуску між словами
    #print("line: ",line)
    rez = re.search(pat_work, line)    # шукаємо у рядку відповідність шаблону
    if rez == None:
        raise ValueError("Неправильний формат даних '{}'".format(line))
    
    wk = rez.group().split()
    #print(wk)
    key = iterat
    bdate = getdate(wk[2], wk[3])
    # записати дані студента у словник
    workers[key] = (wk[0], wk[1], bdate)


def getdate(datestr,timestr):
    '''Повертає дату як об'єкт за рядком дати datestr у різних форматах.

    Можливі формати дати:
    dd.mm.yyyy
    yyyy-mm-dd
    mm/dd/yyyy
    '''
    if '.' in datestr:
        dateformat = "%d.%m.%Y %H:%M"
    elif '-' in datestr:
        dateformat = "%Y-%m-%d %H:%M"
    else:
        dateformat = "%m/%d/%Y %H:%M"
        
    return datetime.datetime.strptime(datestr + " " + timestr, dateformat)


def banned(dic, sites, names):
    array_of_ip = []    
    for key, value in workers.items():
        
        if value[0] not in array_of_ip:
            array_of_ip.append(value[0])
                              
    dic_of_ip = dict.fromkeys(array_of_ip, [])
    a = []
    
    for key, value in dic_of_ip.items():
        for key1, value1 in workers.items():
            if key == value1[0]:
                a.append(tuple((key,  value1[1])))
                
    dic_of_ip1 = {}
    for i in range(len(a)):
        
        if a[i][0] not in dic_of_ip1.keys():
            dic_of_ip1[a[i][0]] = [a[i][1]]
            
        else :
            dic_of_ip1[a[i][0]].append(a[i][1])
            
    for key, value in dic_of_ip1.items():
        
        if len(value) > 1:
            res = collections.Counter(value).most_common()
            print(names[key])
            for i in res:
                print(i)
        
        elif len(value) == 1:
            print(names[key],value[0])
        

if __name__ == '__main__':
    file_banned = open("banned_sites.txt", "r")
    banned_sites = file_banned.read().split(',')  
    
    filename = "workers.txt"
    errname = 'errdata.txt'
    
    workers = process_file(filename, errname)
    
    # збереженя оброблених даних у файлі
    archname = filename + '.dat'
    h = open(archname, "wb")
    pickle.dump(workers, h)
    h.close
    # читання збережених даних з файлу
    h = open(archname, "rb")
    workers = pickle.load(h)
    h.close
    
    name_workers = {'123.321.555.228': "worker0",
                    "321.421.521.121": "worker1",
                    "123.331.555.228": "worker2", 
                    "321.131.321.312": "worker3", 
                    "321.131.221.312": "worker4",
                    "111.111.111.444": "worker5",
                    "111.111.111.555": "worker6" }
        
    file_banned = open("banned_sites.txt", "r")
    file_banned.close
    result = banned(workers, banned_sites, name_workers)
    

#result ip site data