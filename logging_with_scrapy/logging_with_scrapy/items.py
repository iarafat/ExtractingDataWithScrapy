import scrapy
from scrapy.loader.processors import MapCompose


def process_url(value):
    domain = 'https://stackoverflow.com/'
    return domain + value


class QuestionItem(scrapy.Item):
    question = scrapy.Field()
    url = scrapy.Field(input_processor=MapCompose(process_url))
