import html_page
from time import sleep


def auto_monitoring(quantity, shops,request,type_sort,gender,size,num):


    auto = html_page.Server()
    sleeptime = 60
    if quantity == "hour":
        sleeptime = 3600

    elif quantity == "day":
        sleeptime = 86400

    elif quantity == "week":
        sleeptime = 86400*7

    while True:
        print("=== Monitoring client ===")
        try:
            auto.monitoring("auto",shops, request, type_sort, gender, size, num)
        except Exception as e:
            print(e)

        sleep(sleeptime)


auto_monitoring("default",["Asos", "Amazon", "Rozetka"], "adidas stan smith", "cheap", "any", "44", 3)
