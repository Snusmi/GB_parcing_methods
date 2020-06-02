# -*- coding: utf-8 -*-
import scrapy
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    # https://www.avito.ru/izhevsk?q=BMW
    def __init__(self,text,city):
        self.start_urls = [f'https://www.avito.ru/{city}?q={text}']

    def parse(self, response):
        ads_links = response.xpath("//h3/a[@class='snippet-link']/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self,response):
        loader = ItemLoader(item=AvitoparserItem(),response=response)
        loader.add_xpath('name','//h1/span/text()')
        loader.add_xpath('photo',"//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url")
        loader.add_value('link',response.url)
        yield loader.load_item()


        # name = response.xpath('//h1/span/text()').extract_first()
        # photo = response.xpath("//div[@class='gallery-img-frame js-gallery-img-frame']/@data-url").extract()
        # yield AvitoparserItem(name=name, photo=photo)