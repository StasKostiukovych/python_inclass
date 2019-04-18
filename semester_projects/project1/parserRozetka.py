from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import bs4
import unidecode


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


def return_data(url):
    http_file = urlopen(url)
    enc = getencoding(http_file)
    request = urlopen(url)
    data = str(request.read(), encoding=enc, errors='ignore')
    return data


def find_links_rozetka(url, max_iter=5):
    links_and_avalible_opt = {}
    html = return_data(url)
    soup = BeautifulSoup(html, 'lxml')
    iters = 1

    # if items with some characteristics by same price
    ul = soup.find_all('ul',{'class': "cat-variants-l clearfix"})
    for item in ul:
        # avalible option
        avalible = ""
        avalible_items = item.find_all('a')
        for avalible_item in avalible_items:
            avalible += str(avalible_item.next) + ", "
        href = avalible_items[0].get('href')
        links_and_avalible_opt[href] = {"avalible": avalible}
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
    this func find and return description of item

    get: link to item
    return: dict {name of characteristic: characteristic}

    """
    description_dict = {}
    html = return_data(url)
    soup = BeautifulSoup(html, 'lxml')
    description_array_html = soup.find_all('tr', {"class": "ng-star-inserted"})

    price = soup.find("span", {"class":"detail-price-uah"})

    try:
        description_dict["price"] = str(unidecode.unidecode(price.next.string))
    except AttributeError:
        description_dict["price"] = ""


    for descr in description_array_html:

        if len(descr.find_all('span', {'class':"ng-star-inserted"})) != 2:

            # if we have 2 args
            try:
                # form our dict
                description_dict[str(descr.find('span').next)] = str(descr.find('a', {"class": "ng-star-inserted"}).next)

            except AttributeError:
                pass

        else:

            templ = descr.find_all('span', {'class': "ng-star-inserted"})[1].next

            # if it's string
            if type(templ) is bs4.element.NavigableString:
                description_dict[str(descr.find_all('span', {'class': "ng-star-inserted"})[0].next)] = str(descr.find_all('span', {'class': "ng-star-inserted"})[1].next)

            # if it's link
            elif type(templ) is not bs4.element.NavigableString:
                description_dict[str(descr.find_all('span', {'class': "ng-star-inserted"})[0].next)] = str(templ.get("href"))

    return description_dict


def Rozetka(request, type_sort="", num_of_pages=5):

    url = "https://rozetka.com.ua/ua/search/?text={}".format(request)
    if type_sort == "cheap":
        url += "sort=cheap"

    all_info = find_links_rozetka(url,num_of_pages)

    for key, value in all_info.items():
        all_info[key].update(find_description_rozetka(key))

    for key,value in all_info.items():
        print(key, value)



if __name__ == '__main__':
    Rozetka("adidas stan smith")
