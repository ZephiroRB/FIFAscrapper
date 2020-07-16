import scrapy
from scrapy.crawler import CrawlerProcess

player_list = []

class FIFAscrapper(scrapy.Spider):
  name = 'FIFAscrapper'

  allowed_domains = ['www.fifaindex.com']
  start_urls = ['https://www.fifaindex.com/players/fifa21/']

  def parse(self, response):
    link_players = response.css('a.link-player::attr(href)')

    for players in link_players:
      rel_link = players.extract()
      player_url = 'https://www.fifaindex.com' + rel_link
      player_list.append(player_url)

    if (response.css('ul.pagination').xpath('./li//text()').extract_first() == 'Next Page'):
      new_page = response.css('ul.pagination').xpath('./li').css('a.btn::attr(href)').extract_first()
     
      if new_page is not None:
        url = 'https://www.fifaindex.com' + new_page
        yield scrapy.Request(url, callback=self.parse_next_page)


  def parse_next_page(self, response):
    link_players = response.css('a.link-player::attr(href)')

    for players in link_players:
      rel_link = players.extract()
      player_url = 'https://www.fifaindex.com' + rel_link 
      player_list.append(player_url)

    if (response.css('ul.pagination').xpath('./li//text()').extract_first() == 'Previous Page'):
      new_page = response.css('ul.pagination').xpath('./li[2]').css('a.btn::attr(href)').extract_first()

      if new_page is not None:
        url = 'https://www.fifaindex.com' + new_page
        yield scrapy.Request(url, callback=self.parse_next_page)

process = CrawlerProcess()
process.crawl(FIFAscrapper)
process.start()

f = open('players_urls.csv', 'w+')
for player in player_list:
  f.write(str(player))
  f.write(',')
f.close()