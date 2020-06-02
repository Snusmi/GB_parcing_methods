
# -*- coding: utf-8 -*-
import scrapy
from GB_parcing_methods.Lesson6.leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, my_text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={my_text}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        product_links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)
        yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath("name", "//h1[@class='header-2']/text()")
        loader.add_xpath("photo", "//picture[@slot='pictures']/img/@src")
        loader.add_xpath("price", "//meta[@itemprop='price']/@content")
        loader.add_xpath("currency", "//meta[@itemprop='priceCurrency']/@content")
        loader.add_xpath("price_unit", "//span[@slot='unit']/text()")
        yield loader.load_item()