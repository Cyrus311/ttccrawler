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
from helper import getAgent

class SpiderTamrielAlarm(scrapy.Spider):
    name = 'SpiderTamrielAlarm'

    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "CONCURRENT_REQUESTS": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "COOKIES_ENABLED":False,
        "FEED_FORMAT": "json",
        "FEED_URI": "out.json"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,method='GET',headers={"User-Agent":getAgent()})

    def parse(self, response):
        self.logger.info('='*15+'PARSE'+'='*15)
        self.logger.info(response.request.headers)
        time.sleep(1)
        divs = response.xpath('//tr[contains(@class,"cursor-pointer")]')
        for div in divs:
            item = ElderScrollsItem()
            parsed = urlparse(response.request.url)
            item['itemId'] = parse_qs(parsed.query)['ItemID'][0].strip()
            tradeLink = div.xpath(
                ".//@data-on-click-link").extract_first()
            item['tradeId'] = tradeLink.split('/')[4]
            item['name'] = div.xpath(
                "normalize-space(.//td//div[contains(@class,'item-quality-')])").extract_first()
            item['trait'] = div.xpath(
                "normalize-space(.//td//img//@data-trait)").extract_first()

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
