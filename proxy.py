
import scrapy

class Proxy(scrapy.Spider):
    name = 'proxy'
    start_urls = ['https://free-proxy-list.net']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
		'Connection': 'keep-alive',
		'DNT': '1',
		'Host': 'r2---sn-uv2oxuuo-u0oz.googlevideo.com',
		'Origin': 'https://www.youtube.com',
		'Referer': 'https://www.youtube.com/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'cross-site',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
		'X-Client-Data': 'CJa2yQEIpLbJAQjBtskBCIqSygEIqZ3KAQiZtcoBCKe4ygEI9cfKAQjnyMoBCOnIygEIq8nKAQi0y8oB36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }

    def parse(self, response):
        rows= response.css('#proxylisttable tr')
        cols = [row.css('td::text').getall() for row in rows]
        proxies = []
        for col in cols:
            if col and col[4] == 'elite proxy' and col[6] == 'yes':
                proxies.append('https://' + col[0] + ':' + col[1])
            
        print('proxies: \n', proxies)

    #     for proxy in proxies:
    #         test_url = 'https://scrapingkungfu.herokuapp.com/api/request'
    #
    #         # use your video url here
    #         video_url = 'https://www.youtube.com/watch?v=RxFNvRsHuzQ'
    #         print('********************************** test ***************************************')
    #         yield scrapy.Request(video_url, dont_filter=True, headers=self.headers, meta={'proxy': proxy}, callback=self.check_response)
    #
    # def check_response(self, response):
    #     print('\n\nRESPONSE:', response.status)
