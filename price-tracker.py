import random
import smtplib
import sqlite3
import sys

import requests
from bs4 import BeautifulSoup

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
conn = sqlite3.connect('price.db')


def create_db_table():
    # DROP TABLE IF EXISTS LINKS;
    # DROP TABLE IF EXISTS ITEMS;
    conn.executescript("""
    CREATE TABLE LINKS
             (
             LINK           CHAR(100)    NOT NULL
             );
    CREATE TABLE ITEMS
            (
            NAME           CHAR(100)    NOT NULL,
            PRICE            DOUBLE     NOT NULL
            );""")
    print("Table created successfully")

    conn.close()


# Run it only one time#
# create_db_table()

# set the headers and user string

link_list = 'https://www.amazon.in/Bose-SoundLink-Wireless-Around-Ear-Headphones/dp/B0117RGG8E/ref=sr_1_11?qid=1562395272&refinements=p_89%3ABose&s=electronics&sr=1-11'


def send_request(link):
    # send a request to fetch HTML of the page
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    response = requests.get(link, headers={'User-Agent': user_agent})
    print(str(user_agent))
    # create the soup object
    soupf = BeautifulSoup(response.content, 'html.parser')
    soupf.encode('utf-8')
    return soupf


# function to check if the price has dropped below 20,000
def check_price(link):
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
    # print(price)
    # converting the string amount to float
    converted_price = float(price[0:5])
    print(converted_price)
    if converted_price < 20000:
        # send_mail(link, converted_price)
        pass
    # using strip to remove extra spaces in the title
    print(title.strip())


# function that sends an email if the prices fell down
def send_mail(link, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('zazob55@gmail.com', 'mufabiyllybpgsll')

    subject = 'Price Fell Down'
    body = "Check the HB price: " + str(price) + "  link " + str(link)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'zazob55@gmail.com',
        'bugrahan.tabak@hotmail.com',
        msg
    )
    # print a message to check if the email has been sent
    print('Hey Email has been sent')
    # quit the server
    server.quit()


# loop that allows the program to regularly check for prices
while True:
    soup = send_request(link_list)
    check_price(link_list)
    sys.exit(666)
    time.sleep(60 * 60)
