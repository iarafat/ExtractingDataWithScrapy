import re
import csv

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import replace_escape_chars
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from broad_crawler.items import EmailItem


class BroadCrawl(CrawlSpider):
    name = 'scrape_emails'

    start_urls = [
        'http://www.columbia.edu/',
        'https://www.espn.com',
        'https://www.loonycorn.in',
        'https://www.paytm.in'
    ]

    rules = (Rule(LinkExtractor(), callback='parse_item'),)

    def parse_item(self, response):
        loader_object = ItemLoader(item=EmailItem(), response=response)
        loader_object.default_output_processor = MapCompose(lambda x: x.strip(), replace_escape_chars)
        emails = response.xpath('//text()').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}")

        if emails:
            loader_object.add_value('email', emails)
            loader_object.add_value('url', response.url)

        return loader_object.load_item()
