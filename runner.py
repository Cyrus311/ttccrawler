import os
import json
import requests
import sched,time
from scrapy.cmdline import execute
from helper import Quality
from helper import getMessage
from helper import sendNotification

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def runner():
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
                        "chat_id": 493821865,#alarm['chatId'],
                        "text": message
                    }
                    sendNotification(notificationObj)


