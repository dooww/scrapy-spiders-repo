import scrapy
import logging
# import pprint
from scrapy.http import FormRequest
# from scrapy_splash import SplashRequest ,SplashFormRequest
# from scrapy_scrapingbee import ScrapingBeeSpider, ScrapingBeeRequest


# chess games scraper class
class ChessGamesScraper(scrapy.Spider):
    # spider name
    name = 'lichess'

    # base url
    base_url = 'https://lichess.org/@/hediiiiiii/search'
    login_url='https://lichess.org/login?referrer=%2F'

    # custom headers
    headers = {

        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-length': '351',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryXhSTIYuwQIDB2OId',
        'cookie': 'lila2=316f783e67b683830f0b492240f502bf805901c0-sessionId=PcqP9VUhlTqJwDp8tvzU4o&sid=Tp8hdSRVpZfWqvgW4X6ktS; __stripe_mid=05f4c7cc-2e68-44c3-96e6-f53186998c9068b04a',
        'dnt':'1',
        'origin': 'https://lichess.org',
        'referer': 'https://lichess.org/login?referrer=/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',

        }

    # start crawling
    #we cam add the arg here by passing **args
    def start_requests(self):
        # lichess specific API key
        key_id = 1584694629328

        # loop over pages
        for page in range(1, 50):   # set max pages up to 1500 up to
            next_page = self.base_url + '?page=' + str(page) + '&perf=2&sort.field=d&sort.order=desc&_=' + str(key_id)
            yield scrapy.Request(url=self.login_url, headers=self.headers, callback=self.parse_login_lichess)
            key_id += 1

    # parse game list
    def parse_game_list(self, res):
        # extract game links
        games = res.css('a.game-row__overlay::attr(href)').getall()

        # loop over game links
        for game in games:
            yield res.follow(url=game, headers=self.headers, callback=self.parse_game)

    # parse game
    def parse_game(self, res):
        # extract PGN game
        pgn = res.css('div.pgn::text').get()

        # write PGN game to file
        # (PGN) is the most popular standard for the representation of chess games
        with open('kingscrusher.pgn', 'a') as f:
            f.write(pgn + '\n\n\n')

    #login method to allow  us  to get  all the games from lichess
    def parse_login_lichess(self, response):
        return scrapy.FormRequest(
            url=self.login_url,
            headers=self.headers,
            formdata={'username': 'Hediiiiiii', 'password': '********', 'token':'16'},
            callback=self.after_login
         )

    def after_login(self, response):
        if (not (response.css('a #user_tag ::text').extract_first() == 'Hediiiiiii')):
                print('fail to login  verify your info')
            # Something wrong.
        else :
            print('succeeded you\'r connected to  '+response.css('a #user_tag ::text').extract_first()+'account' )
            response.follow(self.base_url,headers=self.headers,callback=self.parse_game_list)
    # You have successfully logged in. Put you code here.

#             if "Error while logging in" in str(response.body):
#                 self.logger.error("Login failed!")
#             else:
#                 self.logger.error("Login succeeded!")
#                 yield  response
# FormRequest("INSERT URL", formdata={"user":"user",  "pass":"pass"}, callback=self.parse)]
