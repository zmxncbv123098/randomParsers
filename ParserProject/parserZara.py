# coding=utf-8
import json
from time import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3


headers = {
    'User-Agent': "User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"}


class UsersDB:
    name = 'Zara.db'

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
        'CREATE TABLE Products(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToProduct TEXT, price TEXT, description TEXT);')


def createImages():
    db = UsersDB()
    db.query(
        'CREATE TABLE Images(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, linkToImage TEXT, productId INTEGER);')


def addProduct(linkToProduct, price, desc, images):
    db = UsersDB()
    db.query('INSERT INTO Products(linkToProduct, price, description) values(\'%s\', \'%s\', \'%s\')' % (
       linkToProduct, price, desc))
    prId = db.fetch("Select id from products order by id DESC limit 1")
    for img in images:
        db.query('INSERT INTO Images(linkToImage, productId) values(\'%s\', %d)' % (img, prId[0][0]))


def get_all_items():
    url = "http://m.zara.com/ru/ru/женщины/юбки-c358006.html"
    html = requests.get(url, headers=headers).text
    sleep(1)
    soup = BeautifulSoup(html, "lxml")  # html5lib
    figcaption = soup.findAll('figcaption')
    for fig in figcaption:
        if fig.find('a', {'class': 'grid-text title'}) is None:
            continue
        # name = fig.find('a').text
        href = fig.find('a')['data-href']
        get_clothes_data(href)
        sleep(1)


def get_clothes_data(url):
    html = requests.get(url, headers=headers).text
    sleep(1)
    soup = BeautifulSoup(html, "lxml")
    images = []
    figures = soup.findAll('figure', {'class': '_product-media product-figure'})
    for fig in figures:
        img = fig.find('img')
        images.append(img['src'].replace('//static', 'http://static'))
    price, name = get_price_and_name(html)
    desc = soup.find('p', {'class': 'info-header'}).text
    addProduct(url, price, desc, images)
    print('[+]')


def get_price_and_name(html):
    start = html.index('product: {') + len('product: ')
    end = html.index('originalProductId') - 7
    info_json = json.loads(html[start:end])
    price = "%d.%d" % (info_json['price'] / 100, info_json['price'] % 100)
    name = info_json['name']
    return price, name

get_all_items()
