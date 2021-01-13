import os
import json
import requests
import time
import SpiderTamriel_EU
from helper import Quality,getMessage,sendNotification,getUrls,addChatLog
from scrapy.utils.project import get_project_settings   
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from twisted.internet.task import deferLater

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def dataProcess(self, *args):
    print('================================== DATA PROCESS ===============================')
    with open('./out.json') as json_file:
        crawlerData = json.load(json_file)
        mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
        mainDataResponse = requests.get(mainGetUrl)
        for item in mainDataResponse.json():
            for alarm in item['alarms']:
                messageObj = getMessage(item['id'],alarm,crawlerData)
                if len(messageObj['message'])>0:
                    notificationObj = {
                        "chat_id": alarm['chatId'],
                        "text": messageObj['message']
                    }
                    sended=sendNotification(notificationObj)
                    if sended:
                        addChatLog(alarm['chatId'],messageObj['tradeId'])
                    #updateAlarm(item['tradeId'],alarm['chatId'])
    open('out.json','w').close()

def cleanOutJson():
    open('out.json','w').close()

def sleep(self, *args, seconds):
    return deferLater(reactor, seconds, lambda: None)

def _crawl(result, spider):
    start_urls=getUrls()
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
