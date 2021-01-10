import scrapy
import pylint
import requests
import time
import urllib.parse as urlparse
from urllib.parse import parse_qs
from item import ElderScrollsItem
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
from urllib.parse import urlparse

mainGetUrl = 'http://ttccrawler-8176c.appspot.com/list'

class SpiderTamrielEu(scrapy.Spider):
    name = 'SpiderTamrielEU'

    start_urls = []
    mainDataResponse = requests.get(mainGetUrl)
    custom_settings = {
        "USER_AGENT":"TTC Crawler",
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "CONCURRENT_REQUESTS": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "HTTPCACHE_ENABLED": True,
        "FEED_FORMAT": "json",
        "FEED_URI": "out.json"
    }
    for esoItem in mainDataResponse.json():
        qualityIds = []

        for alarm in esoItem['alarms']:
            url = ''
            if 'quality' in alarm:
                if not alarm['quality'] in qualityIds:
                    qualityIds.append(alarm['quality'])
                    url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                        esoItem['id']+'&ItemQualityID=' + \
                        str(alarm['quality'])+'&SortBy=LastSeen&Order=asc'
            else:
                url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=' + \
                    esoItem['id']+'&SortBy=LastSeen&Order=asc'
            start_urls.append(url)

        qualityIds.clear()

    def parse(self, response):
        time.sleep(10)
        divs = response.xpath('//tr[contains(@class,"cursor-pointer")]')
        for div in divs:
            item = ElderScrollsItem()
            parsed = urlparse(response.request.url)
            item['itemId'] = parse_qs(parsed.query)['ItemID'][0].strip()
            tradeLink = div.xpath(
                "normalize-space(//tr//@data-on-click-link)").extract_first()
            item['tradeId'] = tradeLink.split('/')[4]
            item['name'] = div.xpath(
                "normalize-space((.//td//div[contains(@class,'item-quality-')]))").extract_first()
            qualityClassName = div.xpath(
                "normalize-space(.//div//@class)").extract_first()

            qualityText = qualityClassName.split('-')[2]
            if qualityText == 'normal':
                item['quality'] = 0
            elif qualityText == 'fine':
                item['quality'] = 1
            elif qualityText == 'superior':
                item['quality'] = 2
            elif qualityText == 'epic':
                item['quality'] = 3
            elif qualityText == 'legendary':
                item['quality'] = 4

            item['location'] = div.xpath("normalize-space((.//td[@class='hidden-xs']//div)[2])").extract_first(
            ) + " -> " + div.xpath("normalize-space((.//td[@class='hidden-xs']//div)[3])").extract_first()
            priceRow = div.xpath(
                "normalize-space(.//td[4])").extract_first()
            item['price'] = priceRow.split('X')[0].replace(',', '').strip()
            quantityArray = priceRow.split('=')[0].strip()
            item['quantity'] = quantityArray.split('X')[1].strip()
            item['totalPrice'] = priceRow.split('=')[1].strip()
            item['lastSeen'] = div.xpath(
                ".//td[5]//@data-mins-elapsed").extract_first()
            yield item
