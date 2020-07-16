import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

links = pd.read_csv('players_urls.csv')
player_list = list(links)

f2 = open('players_info.csv', 'w+')

class FIFAscrapper_info(scrapy.Spider):
  name = 'FIFAscrapper_info'

  allowed_domains = ['www.fifaindex.com']
  start_urls = player_list

  def parse(self, response):
  
    player = response.css('h1::text').extract_first()
    measure = response.css('div.card-body>p:nth-of-type(1)>*> span.data-units::text').extract_first()
    
    f2.write(str(player))
    f2.write(',')
    f2.write(str(measure))
    f2.write('\n')


process2 = CrawlerProcess()
process2.crawl(FIFAscrapper_info)
process2.start()

f2.close()