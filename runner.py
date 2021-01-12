import os
import json
import requests
import time
from scrapy import settings
from helper import Quality
from helper import getMessage
from helper import sendNotification
from scrapy.utils.project import get_project_settings   
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from twisted.internet.task import deferLater
import SpiderTamriel_EU

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def is_json(myjson):
    try:
        json.load(myjson)
    except ValueError:
        return False
    except TypeError:
        return False
    return True



def dataProcess(self, *args):
    print('================================== DATA PROCESS ===============================')
    with open('./out.json') as json_file:
        crawlerData = json.load(json_file)
        mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
        mainDataResponse = requests.get(mainGetUrl)

        for item in mainDataResponse.json():
            for alarm in item['alarms']:
                message = getMessage(item['id'],alarm,crawlerData)
                if len(message)>0:
                    notificationObj = {
                        "chat_id": alarm['chatId'],
                        "text": message
                    }
                    sendNotification(notificationObj)
                    #updateAlarm(item['tradeId'],alarm['chatId'])
    open('out.json','w').close()

def cleanOutJson():
    open('out.json','w').close()

def sleep(self, *args, seconds):
    return deferLater(reactor, seconds, lambda: None)

def _crawl(result, spider):
    start_urls=[]
    mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
    mainDataResponse = requests.get(mainGetUrl)
    for esoItem in mainDataResponse.json():
        qualityIds = []
        itemUrlAdded=False
        for alarm in esoItem['alarms']:
            if 'quality' in alarm:
                if not alarm['quality'] in qualityIds:
                    qualityIds.append(alarm['quality'])
                    start_urls.append( 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                        esoItem['id']+'&ItemQualityID=' + \
                        str(alarm['quality'])+'&SortBy=LastSeen&Order=desc')
            else:
                if not itemUrlAdded:
                    start_urls.append('https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                        esoItem['id']+'&SortBy=LastSeen&Order=desc')
                    itemUrlAdded=True
        qualityIds.clear()
    deferred = process.crawl(spider,start_urls=start_urls)
    deferred.addCallback(dataProcess)
    deferred.addCallback(lambda results: print('waiting 300 seconds before restart...'))
    deferred.addCallback(sleep, seconds=300)
    deferred.addCallback(_crawl, spider)
    return deferred

try:
    s = get_project_settings()
    process = CrawlerProcess(s)
    _crawl(None, SpiderTamriel_EU.SpiderTamrielAlarm)
    process.start()
except SystemExit:
    pass
