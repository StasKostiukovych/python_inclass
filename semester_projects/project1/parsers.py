from urllib.request import urlopen
import requests
import re
from bs4 import BeautifulSoup
import bs4
from random import choice
import json
import unidecode


def get_html(url, proxy=None, ua=None):
    """
    Get html with proxy and User Agent using requests
    :param url: url
    :param proxy: proxy
    :param ua: User Agent
    :return: str html of page
    """
    r = requests.get(url, headers=ua, proxies=proxy)
    return r.text


def getencoding(http_file):

    P_ENC = r'\bcharset=(?P<ENC>.+)\b'
    headers = http_file.getheaders()
    dct = dict(headers)
    content = dct.get('Content-Type', '')
    mt = re.search(P_ENC, content)
    if mt:
        enc = mt.group('ENC').lower().strip()
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


# -----------------------------------------Asos---------------------------------------------------


def find_links_asos(html, num=5):
    """

    :param html: str, html of page
    :param num: quantity of links
    :return: links of first num item
    """
    links_and_about = {}
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('article', {"data-auto-id": "productTile"})
    for index, item in enumerate(items):

        if index == num:
            break

        item = item.find('a')
        prices = item.get('aria-label').split(",")

        try:
            if len(prices) == 3:
                descr, sale_price, original_price = prices
                original_price = original_price.split(" ")[-1].replace("Price:", "").strip()
                sale_price = sale_price.split(" ")[-1].replace("Price:", "").strip()

            elif len(prices) == 2:

                descr, original_price = prices
                original_price = original_price.replace("Price:", "").strip()
                sale_price = original_price
        except Exception as e:
            print("third", e)

        templ_dict = {"description" : descr, "price": original_price,
                      "sale price": sale_price}

        links_and_about[item.get('href')] = templ_dict

    return links_and_about


def return_link_with_choosen_characteristic_asos(url, request, type_sort=None,size=None, gender=None):
    """
    :param url:
    :param request: str, example "adidas yung"
    :param type_sort: cheap ,fresh or relevant
    :param size: EU size, example: EU 44, M ,etc
    :param gender: man or woman
    :return: link with characteristic from above
    """
    gender_opt = ""
    sort_opt = ""
    size_opt = ""

    if gender == "women":
        gender_opt = "&refine=floor:1000"
    elif gender == "man":
        gender_opt = "&refine=floor:1001"

    if type_sort == "cheap":
        sort_opt = "&sort=priceasc"
    elif type_sort == "fresh":
        sort_opt = "&sort=freshness"

    if size == "None":
        size = None

    request = request.replace(" ", "+")

    # sizes.json contain id of asos size to do request
    with open('sizes.json', 'r') as f:
        sizes_arr = json.load(f)

    for size_dict in sizes_arr:
        for key, value in size_dict.items():
            if value == size.upper():
                size_opt = "|size_eu:" + str(size_dict['id'])

    return url + request+ gender_opt  + size_opt + sort_opt


def Asos(request, type_sort=None,size=None, gender=None, num_pages=5):

    """
    Сonnects all asos function
    :param request: str, example "adidas yung"
    :param type_sort: cheap ,fresh or relevant
    :param size: EU size, example: EU 44, M ,etc
    :param gender: man or woman
    :return: dict of links and all information
    """
    url = "https://www.asos.com/search/?&q="
    useragents = open("useragents.txt").read().split("\n")
    proxies = open('proxy').read().split('\n')
    proxy = {'http': 'http://' + choice(proxies)}
    useragent = {'User-Agent': choice(useragents)}

    new_url = return_link_with_choosen_characteristic_asos(url, request, type_sort=type_sort, gender=gender, size=size)
    html = get_html(new_url, proxy, useragent)
    all_info = find_links_asos(html, num_pages)
    return all_info


# ----------------------------------------Amazon--------------------------------------------------


def find_links_amazon(html,num=5):

    namehost = "https://www.amazon.com"
    array_of_links = []

    soup = BeautifulSoup(html, "lxml")
    div = soup.find_all("div", {"class":"a-section a-spacing-none"})

    index = 0
    for span in div:
        if index == num:
            break
        new_span = span.find('span', {"class":"rush-component"})
        if new_span:
            index += 1
            array_of_links.append(namehost + new_span.find('a').get('href'))



    return array_of_links


def find_description_amazon(link, proxy, useragent):

    description_dict = {}
    array_sizes = []

    html = get_html(link, proxy, useragent)

    soup = BeautifulSoup(html, "lxml")

    tr = soup.find("tr", {"id": "priceblock_ourprice_row"})
    if tr:
        price = tr.find("span").next
    else:
        price = "NaN"

    description_dict[link] = {"price": price}

    span = soup.find('span', {"class": "twister-dropdown-highlight transparentTwisterDropdownBorder"})

    if span:
        span = span.find('span')

        for option in span:
            opt = option.find_all('option')
            for size in opt:

                try:
                    array_sizes.append(size.next.strip())
                    description_dict[link].update({"size": array_sizes[1:]})

                except Exception as e:
                    print("key", e)


    else:
        description_dict[link].update({"size": []})


    div = soup.find("div", {"id":"productDescription"})
    if div:

        p = div.find("p")
        #print(p.next.strip())

        try:
            description_dict[link].update({"description": p.next.strip()})
        except Exception as e:
            print("four excep:", e)

    else:
        description_dict[link].update({"description": "NaN"})

    return description_dict


def Amazon(request, type_sort=None, gender=None,size=None, num_pages=5):

    all_info = {}
    if type_sort == "relevant":
        sort_opt = ""

    elif type_sort == "cheap":
        sort_opt = "&s=price-asc-rank"

    elif type_sort == "fresh":
        sort_opt = "&s=date-desc-rank"

    request = request.replace(" ", "+")
    if gender:
        if gender != "any":
            request += "+" + gender

        else:
            pass

    url = "https://www.amazon.com/s?k="
    new_url = url + request + sort_opt


    useragents = open("useragents.txt").read().split("\n")
    useragent = {'User-Agent': choice(useragents)}
    proxy = None # mine proxy
    html = get_html(new_url, proxy, useragent)
    array_links = find_links_amazon(html, num_pages)


    for link in array_links:
        all_info.update(find_description_amazon(link, proxy, useragent))

    return all_info


# ----------------------------------------Rozetka--------------------------------------------------


def find_links_rozetka(url, max_iter=5):
    """
    :param url: url to find those links
    :param max_iter: quantity of links
    :return: links of first max_iter item
    """
    links_and_avalible_opt = {}
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    iters = 1

    # if items with some characteristics by same price
    ul = soup.find_all('ul',{'class': "cat-variants-l clearfix"})
    for item in ul:
        # avalible option
        avalible = []
        avalible_items = item.find_all('a')
        for avalible_item in avalible_items:
            avalible .append(avalible_item.next)
        href = avalible_items[0].get('href')
        links_and_avalible_opt[href] = {"size": avalible}
        if iters >= max_iter:
            break
        iters += 1

    # if only one complection
    if len(links_and_avalible_opt) == 0:
        div = soup.find_all("div", {"class": "g-i-tile-i-title clearfix"})
        for link in div:
            links_and_avalible_opt[link.find('a').get("href")] = {}

            if iters >= max_iter:
                break
            iters += 1

    return links_and_avalible_opt


def find_description_rozetka(url):
    """
    :param url: str url
    :return: dict with urls and all characteristics
    """
    description_dict = {}
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    description_array_html = soup.find_all('tr', {"class": "ng-star-inserted"})

    price = soup.find("span", {"class":"detail-price-uah"})

    try:
        if price:
            description_dict["price"] = str(unidecode.unidecode(price.next.string))
    except Exception as e:
        print("first exept", e)

        description_dict["price"] = ""

    for descr in description_array_html:

        if len(descr.find_all('span', {'class':"ng-star-inserted"})) != 2:

            # if we have 2 args
            try:
                # form our dict
                key = descr.find('span')
                value = descr.find('a', {"class": "ng-star-inserted"})
                if key and value:
                    description_dict[str(key.next)] = str(value.next)


            except Exception as s:
                print("second exep",s)


        else:

            templ = descr.find_all('span', {'class': "ng-star-inserted"})[1].next

            # if it's string
            if type(templ) is bs4.element.NavigableString:
                description_dict[str(descr.find_all('span', {'class': "ng-star-inserted"})[0].next)] = \
                    str(descr.find_all('span', {'class': "ng-star-inserted"})[1].next)

            # if it's link
            elif type(templ) is not bs4.element.NavigableString:
                description_dict[str(descr.find_all('span', {'class': "ng-star-inserted"})[0].next)] = \
                    "https:" + str(templ.get("href"))

    return description_dict



def Rozetka(request, type_sort="",gender=None, size=None, num_of_pages=5):
    """
    :param request: str, example "adidas yung"
    :param type_sort: str, sheap or relevant
    :param num_of_pages:
    :return:
    """
    if size == "None":
        size = None

    gender_opt = ""
    if gender == "man":
        gender_opt = "чоловічі"
    elif gender == "woman":
        gender_opt = "жіночі"

    request = gender_opt + "+" + request
    request = request.replace(" ", "+")
    url = "https://rozetka.com.ua/ua/search/?text={}".format(request)
    new_url = url

    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    li = soup.find_all("li", {"class": "filter-parametrs-tile-l-i"})

    if li:

        for tag_li in li:
            a = tag_li.find('a')
            if str(a.next)[0:2] == size:
                new_url = a.get('href')

    if type_sort == "cheap":
        new_url += "sort=cheap"

    all_info = find_links_rozetka(new_url, num_of_pages)

    for key, value in all_info.items():
        all_info[key].update(find_description_rozetka(key))

    return all_info


# ----------------------------------------Lamoda--------------------------------------------------


def find_links_lamoda(html, max_iter=5):

    links_and_avalible_opt = {}
    soup = BeautifulSoup(html, "lxml")

    divs = soup.find_all("div", {"class":"products-list-item"})

    for index, div in enumerate(divs):

        if index == max_iter:
            break

        price = div.get("data-price")
        href = div.find('a').get('href')
        href = "https://www.lamoda.ua" + href

        links_and_avalible_opt[href] = {"price": price}

        sale_price_templ = div.find("div",{"class":"products-list-item__cd js-cd-timer hidden"})

        if sale_price_templ:

            try:
                sale_price_templ = sale_price_templ.get('data-countdown')
                json_sale_price = json.loads(str(sale_price_templ))
                sale_price = json_sale_price[0]["action_price"]
                links_and_avalible_opt[href].update({"sale price": sale_price})

            except Exception as e:
                print("fivs except:", e)

        sizes_tags = div.find_all("div", {"class":"products-list-item__sizes"})
        if sizes_tags:
            for sizes_tag in sizes_tags:
                sizes = [size.next for size in sizes_tag.find_all('a')]
                links_and_avalible_opt[href].update({"size": sizes})

    return links_and_avalible_opt


def find_description_lamoda(link):
    descr = {}
    html = get_html(link)
    soup = BeautifulSoup(html, "lxml")

    div = soup.find('div', {'class':'ii-product__description-text'})

    descr_labels = [d.next for d in div.find_all('span', {'class':'ii-product__attribute-label'})]
    descr_values = [d.next for d in div.find_all('span', {'class':'ii-product__attribute-value'})]

    for i in range(len(descr_values)):
        descr[descr_labels[i]] = descr_values[i]

    return descr



def Lamoda(request, type_sort="", size=None,gender=None, num_of_pages=5):

    sort_opt = ""
    size_opt = ""


    if request == None:
        return ""

    if size.isalpha():
        size = size.upper()

    request = request.replace(" ", "+")

    if type_sort == "cheap":
        sort_opt = "&sort=price_asc"

    elif type_sort =="fresh":
        sort_opt = "&sort=new"


    if size:
        size_opt = "&size_values=" + str(size)

    url = "https://www.lamoda.ua/catalogsearch/result/?q=" + request + sort_opt + size_opt

    if gender:

        if gender == "woman":
            url = "https://www.lamoda.ua/c/4153/default-women/?q=" + request + sort_opt + size_opt

        elif gender == "men":
            url = "https://www.lamoda.ua/c/4152/default-men/?q=" + request + sort_opt + size_opt
    #print(url)


    html = get_html(url)

    all_info = find_links_lamoda(html)

    for key, values in all_info.items():
        values.update(find_description_lamoda(key))

    return all_info




if __name__ == "__main__":
    pass
    #print(Lamoda("adidas stan smith","cheap", '44', "man"))
    #print(Asos("adidas stan smith","cheap", 'eu 43', "man"))
    #print(Amazon("adidas yung 1", "cheap", "man"))
    #print(Rozetka("adidas stan smith", "cheap", "man", "43"))








