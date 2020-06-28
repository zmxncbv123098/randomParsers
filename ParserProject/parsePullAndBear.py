from bs4 import BeautifulSoup
import requests
import sqlite3
import time
import json


class UsersDB:
    name = 'pullAndBear.db'

    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = sqlite3.connect(self.name)
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        self._db_cur.execute(query)
        self._db_connection.commit()
        return

    def fetch(self, query):
        return self._db_cur.execute(query).fetchall()

    def save(self):
        self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()


def createProducts():
    db = UsersDB()
    db.query(
        'CREATE TABLE Products(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToProduct TEXT, price TEXT, title TEXT, article TEXT);')


def createImages():
    db = UsersDB()
    db.query(
        'CREATE TABLE Images(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToImage TEXT, productId INTEGER);')


def addProduct(linkToProduct, price, title, article, images):
    db = UsersDB()
    db.query('INSERT INTO Products(linkToProduct, price, title, article) values(\'%s\', \'%s\', \'%s\', \'%s\')' % (
       linkToProduct, price, title, article))
    prId = db.fetch("Select id from products order by id DESC limit 1")
    for img in images:
        db.query('INSERTS INTO Images(linkToImage, productId) values(\'%s\', %d)' % (img, prId[0][0]))



url = "https://www.pullandbear.com/m/ru/%D0%B4%D0%BB%D1%8F-%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%BC%D0%B0%D0%B9%D0%BA%D0%B8-c29070.html?isMobile=True"

headers = {
    'User-Agent': "User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"}

html = requests.get(url, headers=headers).text
time.sleep(2)
soup = BeautifulSoup(html, "lxml")  # html5lib
noscript = soup.find_all('noscript')
for url in noscript[-1].find_all('a'):
    ps = url.find_all('p')
    if ps[0].text != '' and not (64 < ord(ps[0].text[0]) < 123):
        href = url.get('href')
        cur_html_obj = requests.get(href, headers=headers).text
        time.sleep(2)
        obj_soup = BeautifulSoup(cur_html_obj, "lxml")
        info = obj_soup.find("script", {"type": "application/ld+json"}).text
        left = info.find("{")
        right = info.rfind("}")
        info = info[left:right + 1]
        info = json.loads(info)
        title = info["name"]
        price = info["offers"]["price"] + " " + info["offers"]["priceCurrency"]
        images = []
        img = info["image"]
        img = img[:img.rfind('?')]
        for i in range(1, 11):
            img = img.split("_")
            img[1] = '2'
            img[2] = str(i)
            img = "_".join(img)
            if str(requests.get(img, headers=headers)) == '<Response [200]>':
                time.sleep(1)
                images.append(img)
            else:
                break
        article = info["mpn"]
        time.sleep(1)
        # print(href, title, price, images, article)
        addProduct(href, price, title, article, images)
        print('[+]')
