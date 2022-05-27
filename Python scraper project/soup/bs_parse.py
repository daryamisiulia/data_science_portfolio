# Parsing using Beautiful Soup

# import necessary libraries
from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd

"""
Initial script parameters
"""

# page parse limit
page_limit = True  # page limit use
page_limit_n = 3   # number of pages to parse

# start URL
given_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/mazowieckie/?search%5Bregion_id%5D=7'

#function for getting list of links URL
def get_list(url):
    """
    Get list of item's URL to parse
    :param url: start URL
    :return: items URL list
    """
    next_page = url   #url of the first page
    counter = 0       #page counter
    res = []          #empty list for item's URL
    #limite page while loop
    while (next_page is not None) & ((not page_limit) | ((counter < page_limit_n) & page_limit)):
        print('Page {}'.format(counter + 1))  #print the number of page starting at 1

        html = request.urlopen(url)           #fetching URL
        bs = BS(html.read(), 'html.parser')   #create bs object for navigation and searching through the HTML for data
        #find all the anchor tags with "data-featured-name" attribute which equal to "listing_no_promo" or "promo_top_ads"
        apt_list = bs.find_all('a', attrs={'data-featured-name': ["listing_no_promo", "promo_top_ads"]})
        res.extend(list(set([tag['href'] for tag in apt_list])))        #adds every element(url) of a list to a Tag

        next_page = bs.find('a', attrs={'data-dir': 'next'})['href']    #go to the next page
        counter += 1                                                    
    return res    #return the result as a list of links URL

#function for getting data from links as dictionary
def get_item(url):
    """
    Get item's data on given URL
    :param url:
    :return: data as dictionary
    """
    html = request.urlopen(url)          #fetching URL
    bs = BS(html.read(), 'html.parser')  #create bs object for navigation and searching through the HTML for data
    #find all names for offer details (exmpl."Powierzchnia", "Liczba pokoi")
    names = bs.find_all('div', attrs={'class': 'css-o4i8bk ev4i3ak2'})
    #find all values for each name(offer detail)
    values = bs.find_all('div', attrs={'class': 'css-1ytkscc ev4i3ak0'})
    #create a dictionary
    res = {n['title']: v['title'] for n, v in zip(names, values)}
    #loop which adds title and address for each offer
    for names, cond in zip(['title', 'address'], [{'class': 'css-46s0sq eu6swcv18'}, {'class': 'css-1qz7z11 e1nbpvi61'}]):
        res.update({names: bs.find(['a', 'h1', 'div', 'strong'], attrs=cond).string}) 
    #loop which adds price and price per metr for each offer
    for i in ['Cena', 'Cena za metr kwadratowy']:
        res.update({i: bs.find(['h1', 'div', 'strong'], attrs={'aria-label': i}).string})

    return res  #return the result with data as dictionary

#execute the functions
if __name__ == '__main__':
    lst = get_list(given_url)
    res = [get_item(item) for item in lst]
    pd.DataFrame(res).to_excel('parsed_bs.xlsx')   #saving result as datatable in .xlsx format






