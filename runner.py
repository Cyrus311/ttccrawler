import os
import json
import requests
from scrapy.cmdline import execute
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from quality import Quality

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def getMessage(itemId,alarm,crawlerData):
    if 'quality' in alarm:
        if 'price' in alarm:
            foundData = list(filter(lambda x: (x["itemId"] == itemId and x['quality'] == alarm['quality'] and float(
                x['price']) <= alarm['price']), crawlerData))
            if len(foundData) > 0:
                sortCrawler = sorted(foundData, key=lambda k: float(
                    k['price']) and int(k['lastSeen']), reverse=False)
                return '{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity}'.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
                    sortCrawler[0]['quantity']), location=sortCrawler[0]['location'])
    else:
        if 'price' in alarm:
            foundData = list(filter(lambda x: (x["itemId"] == itemId and int(
                x['price']) <= alarm['price']), crawlerData))
            if len(foundData) > 0:
                sortCrawler = sorted(foundData, key=lambda k: float(
                    k['price']) and int(k['lastSeen']), reverse=False)
                return '{item} available in \n{location} \nPrice: {price} \nQuantity: {quantity}'.format(item=sortCrawler[0]['name'], price=str(sortCrawler[0]['price']), quantity=str(
                    sortCrawler[0]['quantity']), location=sortCrawler[0]['location'])
    return ''


def sendNotification(notificationObj):
    postMessageUrl = 'https://api.telegram.org/bot1309224660:AAGfsYCMeDnlz5DL1DZ96e29aWkp9vQEeXA/sendMessage'
    url_parts = list(urlparse.urlparse(postMessageUrl))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(notificationObj)
    url_parts[4] = urlencode(query)
    new_url=urlparse.urlunparse(url_parts)
    requests.post(new_url)


try:
    execute(
        [
            'scrapy',
            'runspider',
            'SpiderTamriel_EU.py',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass
finally:
    print('='*15+'FINALLY'+'='*15)
    mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
    mainDataResponse = requests.get(mainGetUrl)
    with open('./out.json') as json_file:
        crawlerData = json.load(json_file)
    for item in mainDataResponse.json():
        for alarm in item['alarms']:
            message = getMessage(item['id'],alarm,crawlerData)
            if len(message)>0:
                notificationObj = {
                    "chat_id": alarm['chatId'],
                    "text": message
                }
                sendNotification(notificationObj)

