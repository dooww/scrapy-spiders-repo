import scrapy
import  re
from scrapy_splash import SplashRequest
import scrapy_splash
from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest



# clean the text  from spaces and all  uneeded things
def clean_up(text):
    text = re.sub(r"[-()\"#/@;:<>{}-=~|.?,]","",text)
    return (re.sub(r'\\t|\\r|\\n','',text))




#use proxy and user agent rotate that already integrated in scrapy

 # custom_settings = {DOWNLOADER_MIDDLEWARES = {
 #
 #   ‘myproject.middlewares.CustomProxyMiddleware’: 350,
 #
 #   ‘scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware’: 400,}



class BabnetSpider(scrapy.Spider):
    name = 'babnet'
    allowed_domains = ['babnet.net']
    start_urls = ['https://www.babnet.net/']
   
                

    def parse(self, response):
        blocks=response.css('.post-content , .post-block-style , .col-md-6')
        # list=response.css('.post-block-style.text-center.clearfix .post-thumb a ::attr(href)').getall()
        for block in blocks:
            url=block.css('a::attr(href)').get()
            full_url= response.urljoin(url)
            print(full_url)
            yield scrapy.Request(full_url,header=self.headers,callback=self.parse_post)

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,header=self.headers,callback=self.parse)



    def parse_post(self, response):
        print('test')
        title=response.css('.post-title::text').get()
        image_url=response.css('.img-fluid::attr(src)').get()
        date= response.css('.post-date::text').get()
        post_text=response.css('.entry-content::text').extract()

        yield {'title':title ,
                'image_url':image_url,
                'date' :date,
                'post_text' :clean_up(post_text).strip(),
                }
