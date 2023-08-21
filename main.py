import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    quote_list = []

    def parse(self, response):
        with open('data/quotes.json', 'w') as json_file:
            for quote in response.xpath("/html//div[@class='quote']"):
                self.quote_list.append({
                    "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").extract(),
                    "quote": quote.xpath("span[@class='text']/text()").get()
                })
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                    yield scrapy.Request(url=self.start_urls[0] + next_link)
            json.dump(self.quote_list, json_file)

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    author_list = []

    def parse(self, response):
        with open('data/quotes.json', 'w') as json_file:
            for author in response.xpath("/html//div[@class='quote']/a/@href"):
                self.quote_list.append({
                    "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").extract(),
                    "quote": quote.xpath("span[@class='text']/text()").get()
                })
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                    yield scrapy.Request(url=self.start_urls[0] + next_link)
            json.dump(self.quote_list, json_file)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()

