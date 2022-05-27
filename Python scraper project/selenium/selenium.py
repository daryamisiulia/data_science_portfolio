from selenium import webdriver
import pandas as pd
import sys, traceback

"""
Initial script parameters
"""

# page parse limit
page_limit = True  # page limit use
page_limit_n = 3   # number of pages to parse

# start URL
given_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/mazowieckie/?search%5Bregion_id%5D=7'

# Selenium headless browser mode parameters
chromedriver = r'chromedriver.exe'   # chromedriver path
options = webdriver.ChromeOptions()  # load driver options
options.add_argument('headless')     # headless mode
driver = webdriver.Chrome(executable_path=chromedriver, options=options)  # driver object


def get_list(url):
    """
    Get list of item's URL to parse
    :param url: start URL
    :return: items URL list
    """
    next_page = url # page 
    counter = 0     # page counter
    res = []      # empty list for items URL
    while (next_page is not None) & ((not page_limit) | ((counter < page_limit_n) & page_limit)):
        print('Page {}'.format(counter + 1))# prins a number of page starting from 1
        driver.get(next_page)#finds all elements by using xpath
        #with data feature name  which are equal to 'listing_no_promo' and 'promo_top_ads'.
        content = driver.find_elements_by_xpath("//a[@data-featured-name='listing_no_promo']") + \
                  driver.find_elements_by_xpath("//a[@data-featured-name='promo_top_ads']")
        res.extend(list(set([item.get_attribute('href') for item in content]))) #Adds each element of lists to tag
        print('Links added')
        try:
            element = driver.find_element_by_xpath("//a[@data-dir='next']") #finds  elements by using xpath

            if element:
                next_page = element.get_attribute('href')
            else:
                print('No next page')
                return # return a result as a lists of links  URL
        except Exception as e:
            print(traceback.format_exception(None, e, e.__traceback__),
                  file=sys.stderr, flush=True)
            print('Exception with next page')
            next_page = None
        counter += 1

    return res # return a result


def get_item(url):
    """
    Get item's data on given URL
    :param url:
    :return: data as dictionary
    """
    driver.get(url)

    names = [item.get_attribute('title')
             for item in driver.find_elements_by_xpath("//div[@class='css-o4i8bk ev4i3ak2']")] #finds  elements by using xpath
    values = [item.get_attribute('title')
              for item in driver.find_elements_by_xpath("//div[@class='css-1ytkscc ev4i3ak0']")] #finds  elements by using xpath
    res = {n: v for n, v in zip(names, values)}
    for name, xpath in zip(['title', 'address', 'Cena', 'Cena za metr kwadratowy'], #creates a loop which adds price and price per square meter
                           ["//h1[@data-cy='adPageAdTitle']", "//a[@class='css-1qz7z11 e1nbpvi61']",
                            "//strong[@aria-label='Cena']", "//div[@aria-label='Cena za metr kwadratowy']"]):
        content = driver.find_elements_by_xpath(xpath)
        if content:
            res.update({name: content[0].text})

    return res # return the result with data as dictionary


if __name__ == '__main__':
    # get list of links
    lst = get_list(given_url)

    # get items' data
    res = [get_item(item) for item in lst]

    # save data to dataframe
    pd.DataFrame(res).to_excel('parsed_sl.xlsx') # save result as datatable in xlsx. format
