import os
import json
import requests
import time
from scrapy.cmdline import execute
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
    

def sleep(self, *args, seconds):
    return deferLater(reactor, seconds, lambda: None)

def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(dataProcess)
    deferred.addCallback(lambda results: print('waiting 300 seconds before restart...'))
    deferred.addCallback(sleep, seconds=300)
    deferred.addCallback(_crawl, spider)
    return deferred

try:
    s = get_project_settings()
    process = CrawlerProcess(s)
    _crawl(None, SpiderTamriel_EU.SpiderTamrielEu)
    process.start()
except SystemExit:
    pass
