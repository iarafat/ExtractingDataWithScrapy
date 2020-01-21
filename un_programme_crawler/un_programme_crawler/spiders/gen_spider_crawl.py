from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GenSpiderCrawl(CrawlSpider):
    name = 'un_programme_crawler'

    allowed_domains = ['un.org']
    start_urls = ['http://www.un.org/en/sections/about-un/funds-programmes-specialized-agencies-and-others/index.html']

    rules = (Rule(LinkExtractor(allow=('funds-programmes-specialized-agencies-and-other'),
                                deny=('zh/sections', 'fr/sections', 'ru/sections')),
                  callback='parse_page'),)

    def parse_page(self, response):
        list_of_agencies = response.css('div.field-item.even > h4::text').extract()

        with open('un_agencies.txt', 'a+') as file:
            for agency in list_of_agencies:
                file.write(agency + '\n')
