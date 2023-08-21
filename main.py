import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    quote_list = []
    author_list = []

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            self.quote_list.append({
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            })
            author_link = quote.xpath("span/a/@href").get()
            yield scrapy.Request(url=self.start_urls[0] + author_link, callback=self.author_parse)
        next_link = response.xpath("//li[@class='next']/a/@href").get()

        if next_link:
                yield scrapy.Request(url=self.start_urls[0] + next_link)
                
        with open('data/quotes.json', 'w') as json_file:
            json.dump(self.quote_list, json_file)   
 
    def author_parse(self, response):
         for author in response.xpath("/html//div[@class='author-details']"):
            self.author_list.append({
                "fullname": author.xpath("h3 [@class='author-title']/text()").get(),
                "born_date": author.xpath("p/span [@class='author-born-date']/text()").get(),
                "born_location": author.xpath("p/span [@class='author-born-location']/text()").get(),
                "description": author.xpath("div [@class='author-description']/text()").get().strip()
            })
            print(self.author_list)
              
              
         
         


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()

