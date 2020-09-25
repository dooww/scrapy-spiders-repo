import scrapy


class PlayerInfoSpider(scrapy.Spider):
    name = 'player_info'
    allowed_domains = ['nfl.com']
    start_urls = ['https://www.nfl.com/players/active/a']

    def parse(self, response):
        base_link='https://www.nfl.com'
        player_profiles_links=response.css(".d3-o-player-fullname nfl-o-cta--link::attr(href)").getall()
        for x in player_profiles_links:
            url=base_link + x +'/stats'
            yield request(url ,callback=self.parse_player)

    def parse_player(self,response):
        teams= response.css(".nfl-t-stats__col-13:nth-child(2)::text").getall()
        years= response.css("td.nfl-t-stats__col-13:nth-child(1)::text").getall()


       