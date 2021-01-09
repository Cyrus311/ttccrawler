import os
import json
import requests
from scrapy.cmdline import execute
import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode

os.chdir(os.path.dirname(os.path.realpath(__file__)))

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
    postMessageUrl = 'https://api.telegram.org/bot1309224660:AAGfsYCMeDnlz5DL1DZ96e29aWkp9vQEeXA/sendMessage'
    with open('./out.json') as json_file:
        crawlerData = json.load(json_file)
    mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'
    mainDataResponse = requests.get(mainGetUrl)
    for item in mainDataResponse.json():
        for alarm in item['alarms']:
            mustSend = False
            message=''
            if 'quality' in alarm:
                if 'price' in alarm:
                    foundData=list(filter(lambda x: (x["itemId"] == item['id'] and x['quality'] == alarm['quality'] and float(
                        x['price']) <= alarm['price']), crawlerData))
                    if len(foundData)>0:
                        mustSend = True
                        message=foundData[0]['name']+' items quality:'+str(foundData[0]['quality'])+' price:'+str(foundData[0]['price'])+' avaible in ' + foundData[0]['location']
                        print(message)
                        print(list(filter(lambda x: (x["itemId"] == item['id'] and x['quality'] == alarm['quality'] and float(
                            x['price']) <= alarm['price']), crawlerData)))

                else:
                    foundData=list(filter(lambda x: (
                        x["itemId"] == item['id'] and x['quality'] == alarm['quality']), crawlerData))
                    if len(foundData)>0:
                        mustSend = True
                        message=item['name']+' items quality:'+item['quality']+' avaible in ' + item['location']
                        print(list(filter(lambda x: (
                            x["itemId"] == item['id'] and x['quality'] == alarm['quality']), crawlerData)))
            else:
                if 'price' in alarm:
                    foundData=list(filter(lambda x: (x["itemId"] == item['id'] and int(
                        x['price']) <= alarm['price']), crawlerData))
                    if len(foundData)>0:
                        mustSend = True
                        message=item['name']+' items price:'+item['price']+' avaible in ' + item['location']
                        print(list(filter(lambda x: (x["itemId"] == item['id'] and int(
                            x['price']) <= alarm['price']), crawlerData)))
                else:
                    foundData=list(filter(lambda x: (x["itemId"] == item['id']), crawlerData))
                    if len(foundData)>0:
                        mustSend = True
                        print(
                            list(filter(lambda x: (x["itemId"] == item['id']), crawlerData)))
            # if mustSend:
            #     telegram = {
            #         "chat_id": alarm['chatId'],
            #         "text": message
            #     }

            #     url_parts = list(urlparse.urlparse(postMessageUrl))
            #     query = dict(urlparse.parse_qsl(url_parts[4]))
            #     query.update(telegram)

            #     url_parts[4] = urlencode(query)
            #     new_url=urlparse.urlunparse(url_parts)
            #     print(urlparse.urlunparse(url_parts))                

            #     apiResponsePost = requests.post(new_url)


    