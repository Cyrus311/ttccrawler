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

def getTradeIds(chatId):
    with open('./chatlog.json') as json_file:
        userChatData=list(filter(lambda x: (x["chatId"] == str(chatId) ), json.load(json_file)))
        return [e['tradeId'] for e in userChatData]

def getMessage(itemId,alarm,crawlerData):
    tradeIds=getTradeIds(alarm['chatId'])
    if 'quality' in alarm:
        if 'price' in alarm:
            foundData = list(filter(lambda x: (x["itemId"] == itemId and x['quality'] == alarm['quality'] and x['tradeId'] not in tradeIds and float(
                x['price']) <= alarm['price']), crawlerData))
            if len(foundData) > 0:
                sortCrawler = sorted(foundData, key=lambda k: float(
                    k['price']) and int(k['lastSeen']), reverse=False)
                if sortCrawler[0]['trait']!="":
                    return {
                        'message':'{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity} \nTrait: {trait}'.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
                            sortCrawler[0]['quantity']), location=sortCrawler[0]['location'], trait=sortCrawler[0]['trait']), 
                        'tradeId':sortCrawler[0]['tradeId']
                        }
                else:
                    return {
                        'message':'{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity} '.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
                            sortCrawler[0]['quantity']), location=sortCrawler[0]['location']), 
                        'tradeId':sortCrawler[0]['tradeId']
                        }
    else:
        if 'price' in alarm:
            foundData = list(filter(lambda x: (x["itemId"] == itemId and x['tradeId'] not in tradeIds and float(
                x['price']) <= alarm['price']), crawlerData))
            if len(foundData) > 0:
                sortCrawler = sorted(foundData, key=lambda k: float(
                    k['price']) and int(k['lastSeen']), reverse=False)
                if  sortCrawler[0]['trait']!="":
                    return {
                        'message':'{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity} \nTrait: {trait}'.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
                            sortCrawler[0]['quantity']), location=sortCrawler[0]['location'], trait=sortCrawler[0]['trait']), 
                        'tradeId':sortCrawler[0]['tradeId']
                        }
                else:
                    return {
                        'message':'{item} available in \n{location} \nQuality: {quality} \nPrice: {price} \nQuantity: {quantity}'.format(item=sortCrawler[0]['name'], quality=Quality(sortCrawler[0]['quality']).name, price=str(sortCrawler[0]['price']), quantity=str(
                            sortCrawler[0]['quantity']), location=sortCrawler[0]['location']), 
                        'tradeId':sortCrawler[0]['tradeId']
                        }
    return {'message':'','tradeId':''}

def write_json(data, filename='chatlog.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def addChatLog(chatId,tradeId):
    with open('chatlog.json') as json_file: 
        data = json.load(json_file) 
        
        y = {'chatId':str(chatId),'tradeId':tradeId} 
    
        data.append(y) 
      
    write_json(data) 


def sendNotification(notificationObj):
    postMessageUrl = 'https://api.telegram.org/bot1309224660:AAGfsYCMeDnlz5DL1DZ96e29aWkp9vQEeXA/sendMessage'
    url_parts = list(urlparse.urlparse(postMessageUrl))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(notificationObj)
    url_parts[4] = urlencode(query)
    new_url=urlparse.urlunparse(url_parts)
    response=requests.post(new_url)
    return response.ok

def getUrls():
    urls=[]
    mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
    mainDataResponse = requests.get(mainGetUrl)
    for esoItem in mainDataResponse.json():
        qualityIds = []
        traitIds = []
        itemUrlAdded=False
        for alarm in esoItem['alarms']:
            if 'quality' in alarm:
                if not alarm['quality'] in qualityIds:
                    if 'trait' in alarm:
                        if not alarm['trait'] in traitIds:
                            qualityIds.append(alarm['quality'])
                            traitIds.append(alarm['trait'])
                            urls.append( 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                                esoItem['id']+'&ItemQualityID=' + \
                                str(alarm['quality'])+'&ItemTraitID='+str(alarm['trait'])+'&SortBy=LastSeen&Order=desc')
                    else:
                            qualityIds.append(alarm['quality'])
                            urls.append( 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                                esoItem['id']+'&ItemQualityID=' + \
                                str(alarm['quality'])+'&SortBy=LastSeen&Order=desc')
            else:
                if not itemUrlAdded:
                    if 'trait' in alarm:
                        if not alarm['trait'] in traitIds:
                            traitIds.append(alarm['trait'])
                            urls.append('https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                                esoItem['id']+'&ItemTraitID='+str(alarm['trait'])+'&SortBy=LastSeen&Order=desc')
                    else:
                        urls.append('https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                            esoItem['id']+'&SortBy=LastSeen&Order=desc')
                    itemUrlAdded=True
        qualityIds.clear()
    return urls

def updateAlarm(itemId,chatId):
    pass
