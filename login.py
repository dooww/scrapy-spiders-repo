import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['login']
    start_urls = ['http://login/']

    def parse(self, response):
        pass
