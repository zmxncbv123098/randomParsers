import json
import requests
import datetime

domain = "teamnavalny_mos"  # input("String: ")


def parseVK(domain):

    global post
    url = "https://api.vk.com/method/wall.get?domain=%s&access_token=fd60b193fd60b193fd60b1939afd00f510ffd60fd60b193a75e07e94a64518cd67a0271&count=10" % domain
    js = json.loads(requests.get(url).text)["response"]
    del js[0]
    atPh = ['photo', 'posted_photo', 'app', 'graffiti']
    for i in js:
        date = datetime.datetime.fromtimestamp(int(i['date'])).strftime('%Y-%m-%d %H:%M:%S')
        text = i['text']
        likes = i['likes']['count']
        attach = {'photo': None, 'link': None, 'video' : None}
        for j in i['attachments']:
            if j['type'] in atPh:
                ph = j[j['type']]['src_big']
                attach['photo'] = ph
            elif j['type'] == 'link':
                linkURL = j['link']['url']
                attach['link'] = linkURL
            elif j['type'] == 'video':
                v = "https://vk.com/video" + str(j['video']['owner_id']) + "_" + str(j['video']['vid'])
                attach['video'] = v
        post = {'date': date, 'text': text, 'likes': likes, 'attach': attach}

    return print(post)
