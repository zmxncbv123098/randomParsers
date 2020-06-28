# coding=utf-8
import requests
import json
from bs4 import BeautifulSoup
import time
import re
import datetime


def delliter(stri):
    while True:
        l = stri.find('<')
        g = stri.find('>')
        delit = stri[l:g + 1]
        if delit == '<br/>':
            stri = stri.replace(delit, '\n')
        else:
            stri = stri.replace(delit, '')

        if l == -1:
            break
    return stri



u = 'http://msk.posrednikovzdes.net/adv.php?city=73&oper=4'
text = requests.get(u).text
pages = str(text)[str(text).find('Страницы'):]
pages = pages[:pages.find('<TBODY>')]
s = BeautifulSoup(pages, 'lxml')
a = str(s.find_all('a')[-1].get('href'))
a = int(a[a.find('page=') + 5:a.rfind('&')])
ALL_OFFERS = []
for al in range(1, a + 1):
    print(al)
    u = 'http://msk.posrednikovzdes.net/adv.php?city=73&oper=4&metro=0&realty=0&oplt=0&price1=0&price2=0&page=%s&paiin=0' % al
    text = requests.get(u).text
    soup = BeautifulSoup(text, "lxml")
    table = soup.find('table', {'class': 'tab'})
    tr = table.find_all('tr')  # [/// , /// , ///]
    for i in tr:
        td = i.find_all('td')
        if len(td) == 9:
            dat = delliter(str(td[1]))
            idd = dat[dat.find('№') + 1:]
            idd = re.sub(r' ', '', idd)
            # print(idd)
            url = 'http://msk.posrednikovzdes.net/offer.php?id=%s' % idd
            # print(url)

            dat = dat[:dat.find('№')]
            dat = re.sub(r'\d\d:\d\d:\d\d', '', dat)
            if "Сегодня" in dat:
                dat = datetime.date.today().strftime("%d.%m.%Y")
            elif "Вчера" in dat:
                yesterday = datetime.date.today() - datetime.timedelta(1)
                dat = yesterday.strftime("%d.%m.%Y")
            # print(dat)

            obj = delliter(str(td[2]))
            obj = obj.split('\n')
            distr = None
            metro = None
            for j in range(len(obj)):
                obj[j] = re.sub(r'\xa0|\t|\r', '', obj[j])
                if 'Район' in obj[j]:
                    distr = obj[j]
                if 'Метро' in obj[j]:
                    metro = obj[j]
            room = obj[1]
            if "квартира" in room:
                room = int(re.sub(r'квартира|к\.|-| ', '', room))
            elif "Койко-место" in room:
                room = -1
            elif "Комната" in room:
                room = 0
            # print(room, distr, metro, sep='||')

            pay = delliter(str(td[3]))
            pay = re.sub(r'\xa0|\t|\r', '', pay).split('\n')
            if len(pay) < 3:
                payment = "no"
            else:
                payment = pay[0] + pay[1] + pay[2]
            payment = re.sub(r'Помесячно| |Предоплата|Посуточно', '', payment)
            if 'тыс.руб.' in payment:
                payment = re.sub(r'тыс\.руб\.', '', payment)
                if '.' in payment:
                    payment = payment.replace('.', '')
                    payment += '00'
                else:
                    payment += '000'
            elif 'руб.' in payment:
                payment = re.sub(r'руб\.', '', payment)
            # print(payment)

            descript = td[7].find('span', {'style': "color:#CC0000; "}).text
            # print(descript)

            phone = delliter(str(td[7]))
            phone = re.sub(r'\xa0|\t|\r', '', phone).split('\n')
            for z in phone:
                if "Контакты" in z:
                    ph = z[z.find('+'):]
                    ph = ph[:17]
            # print(ph)

            x = {'room_num': room, 'metro': metro,
                 "cost": payment,  "contacts": dict(phone=ph, person_name=None), "loc": None,
                 "url": url,  "adr": str(distr), "descr": descript}
            ALL_OFFERS.append(x)
            print('[+]')
            time.sleep(1)
