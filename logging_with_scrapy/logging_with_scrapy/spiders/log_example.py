import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from logging_with_scrapy.items import QuestionItem


class LogExampleSpider(scrapy.Spider):
    name = 'logger'
    start_urls = ['https://stackoverflow.com/questions?sort=featured']

    def parse(self, response):
        questions = response.css('div.question-summary')

        if len(questions) == 0:
            self.logger.error('No elements found on the current page with the selector...')

        self.logger.info('loading the items with scraped data...')
        for question in questions:
            object_loader = ItemLoader(item=QuestionItem(), selector=question)
            object_loader.default_output_processor = TakeFirst()

            self.logger.debug('Adding data to item loader object')

            object_loader.add_css('question', 'h3 > a::text')
            object_loader.add_css('url', 'h3 > a::attr(href)')

            yield object_loader.load_item()
