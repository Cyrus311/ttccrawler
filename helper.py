import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from enum import Enum
import requests
import random
import json

class Quality(Enum):
    Normal=0
    Fine=1
    Superior=2
    Epic=3
    Legendary=4

def getAgent():
    with open('./user_agents.json') as json_file:
        return random.choice(json.load(json_file)['user_agents'])

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
            foundData = list(filter(lambda x: (x["itemId"] == itemId and float(
                x['price']) <= alarm['price']), crawlerData))
            if len(foundData) > 0:
                sortCrawler = sorted(foundData, key=lambda k: float(
                    k['price']) and int(k['lastSeen']), reverse=False)
                return '{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity}'.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
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

def updateAlarm(itemId,chatId):
    pass
