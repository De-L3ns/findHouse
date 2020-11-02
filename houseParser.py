import time
import os
import smtplib
from bs4 import BeautifulSoup
from selenium import webdriver

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# functions


def immoWebParser():
    driver = webdriver.Chrome()
    driver.get(
        'https://www.immoweb.be/nl/zoeken/huis/te-koop/deinze/9850?countries=BE&orderBy=newest')
    html = driver.execute_script("return document.documentElement.outerHTML")

    web_soup = BeautifulSoup(html, 'html.parser')

    for house in web_soup.find_all('article'):

        link = house.find(
            'a', class_='card__title-link')['href']
        sep = '?'
        stripped_link = link.split(sep, 1)[0]
        immoweb_list.append(stripped_link)
        # print(stripped_link) #dev check
        # print() #dev check

    driver.close()


def zimmoParser():
    driver = webdriver.Chrome()
    driver.get(
        'https://www.zimmo.be/nl/panden/?status=1&type%5B0%5D=5&hash=0e75a1596dc2bfbaa69cd88cff30a474&priceIncludeUnknown=1&priceChangedOnly=0&bedroomsIncludeUnknown=1&bathroomsIncludeUnknown=1&constructionIncludeUnknown=1&livingAreaIncludeUnknown=1&landAreaIncludeUnknown=1&commercialAreaIncludeUnknown=1&yearOfConstructionIncludeUnknown=1&epcIncludeUnknown=1&queryCondition=and&includeNoPhotos=1&includeNoAddress=1&onlyRecent=0&onlyRecentlyUpdated=0&isPlus=0&region=list&city=7cExDQAADAMgS61%252Fc02mYgeQAADAJz0D&sort=recent&sort_order=desc#gallery')

    html = driver.execute_script("return document.documentElement.outerHTML")

    web_soup = BeautifulSoup(html, 'html.parser')

    for house in web_soup.find_all('div', class_='property-item'):
        link = house.find('a', class_='property-item_link')['href']
        sep = '?'
        stripped_link = 'www.zimmo.be' + link.split(sep, 1)[0]
        zimmo_list.append(stripped_link)

    driver.close()

def sendEmail(list_name):

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'New entries on ImmoWeb'
        body = "\r\n".join(list_name[:5])

        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, 'reciever e-mail', msg)


# Actual Script


immoweb_list = []
updated_immoweb_list = []
zimmo_list = []
updated_zimmo_list = []

timer_count = 20
while True:

    print('Checking new houses')

    """ Parser 1 for Immoweb """
    immoWebParser()

    """ If statement that checks if there are new entries by comparing two lists """
    if updated_immoweb_list == immoweb_list:
        print('There are no new entries')

    else:
        print('There are new entries on ImmoWeb')
        if updated_immoweb_list == []:
            print('First time the program ran, nothing to report')
        else:
            print('New entry on ImmoWeb, sending e-mail')
            sendEmail(updated_immoweb_list)
    updated_immoweb_list = immoweb_list
    immoweb_list = []

    """ Parser 2 for Zimmo """
    zimmoParser()

    """ If statement that checks if there are new entries by comparing two lists """
    if updated_zimmo_list == zimmo_list:
        print('There are no new entries on Zimmo')

    else:
        print('There are new entries')
        if updated_zimmo_list == []:
            print('First time the program ran, nothing to report')
        else:
            print('New entry on Zimmo, sending e-mail')
            sendEmail(updated_zimmo_list)
    updated_zimmo_list = zimmo_list
    zimmo_list = []

    print('website checked, time for a ' + str(timer_count) + ' second nap')
    time.sleep(timer_count)


# extra code for more details in immoWebParser()
    # name = house.h2.text.strip()
    # # print(name) #dev check

    # price = house.find(
    #     'span', class_='sr-only').text.strip()
    # # print(price) #dev check

    # location = house.find(
    #     'p', class_='card__information card--results__information--locality card__information--locality').text.strip()

    # # print(location) #dev check


# def newEntryCheck(old_list, new_list):

#     if new_list == old_list:
#         print('There are no new entries')
#         old_list = []
#     else:
#         print('There are new entries!')
#     new_list = old_list
