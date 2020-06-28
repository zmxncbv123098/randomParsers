from bs4 import BeautifulSoup
import requests


class Sneakers_article:
    title_ = None
    img_ = None
    desc = None

    def show_article(self):
        print(self.title_)
        print(self.img_)
        print(self.desc)

    def __init__(self, title_, img_, desc):
        self.title_ = title_
        self.img_ = img_
        self.desc = desc


class Article:
    art_title = None
    art_desc = None
    art_text = None
    art_imgs = []

    def show_art(self):
        print(self.art_title)
        print(self.art_desc)
        print(self.art_text)
        print(self.art_imgs)

    def __init__(self, art_title, art_desc, art_text, art_imgs):
        self.art_title = art_title
        self.art_desc = art_desc
        self.art_text = art_text
        self.art_imgs = art_imgs

url = "http://hypebeast.com/footwear"

html = requests.get(url).text

soup = BeautifulSoup(html, "lxml")

post_boxes = soup.find_all('div', {'class': 'post-box'})
# print(post_boxes[0])
result_articles = []
for row_number in range(len(post_boxes)):
    title = post_boxes[row_number].find('a', {'class': 'thumbnail'}).get("title")
    img = post_boxes[row_number].find('img', {'class': 'img-responsive'}).get('src')
    descript = post_boxes[row_number].find('div', {'class': 'post-box-excerpt hidden-sm hidden-xs'}).text
    res = Sneakers_article(title, img, descript)
    result_articles.append(res)


for elem in result_articles:
    elem.show_article()
    print()


print('=' * 100)
art = []
for i in range(len(result_articles)):

    article_html = requests.get(post_boxes[i].find('a', {'class': 'thumbnail'}).get("href")).text

    article_soup = BeautifulSoup(article_html, "lxml")

    article_title = article_soup.find('h1', {'class': 'title header-color-change-point'}).text

    article_descript = article_soup.find('div', {'class': 'excerpt'}).text

    article_text = article_soup.find('div', {'class': 'content-wrapper'}).find('div', {'class': 'content'}).text

    img_container = article_soup.find('div', {'class': 'flexslider'})
    imgs = img_container.find_all('li', {'class': 'slide'})

    all_imgs = []
    for img in imgs:
        src = img.find('img').get('src')
        all_imgs.append(src)
    del all_imgs[-1]  # delete the commercial
    res = Article(article_title, article_descript, article_text, all_imgs)
    art.append(res)


for elem in art:
    elem.show_art()
    print()
