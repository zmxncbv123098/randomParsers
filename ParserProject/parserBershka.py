# coding=utf-8
import requests
from bs4 import BeautifulSoup
import sqlite3
import time


class UsersDB:
    name = 'Bershka.db'

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
        'CREATE TABLE Products(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToProduct TEXT, price TEXT, title TEXT);')


def createImages():
    db = UsersDB()
    db.query(
        'CREATE TABLE Images(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToImage TEXT, productId INTEGER);')


def addProduct(linkToProduct, price, title, images):
    db = UsersDB()
    db.query('INSERT INTO Products(linkToProduct, price, title) values(\'%s\', \'%s\', \'%s\')' % (
       linkToProduct, price, title))
    prId = db.fetch("Select id from products order by id DESC limit 1")
    for img in images:
        db.query('INSERT INTO Images(linkToImage, productId) values(\'%s\', %d)' % (img, prId[0][0]))


headers = {
    'User-Agent': "User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"}

url = "https://www.bershka.com/ru/женщина/одежда/платья-c1010193213.html"
html = requests.get(url).text
time.sleep(2)
# print html
soup = BeautifulSoup(html, "lxml")  # html5lib
# get all rows
noscript = soup.findAll('noscript')
lis = noscript[1].findAll('li')
for l in lis:
    images = []
    item_src = l.find('a')['href']
    image_src = l.find('img')['src']
    ps = l.findAll('p')
    title = ps[0].text
    price = ps[1].text
    image_src = image_src[:image_src.rfind('?')]
    for i in range(1,11):
        image_src = image_src.split("_")
        image_src[1] = '2'
        image_src[2] = str(i)
        image_src = "_".join(image_src)
        if str(requests.get(image_src, headers=headers)) == '<Response [200]>':
            time.sleep(1)
            images.append(image_src)
        else:
            break
    addProduct(item_src, price, title, images)
    time.sleep(1)
    print("[+]")
