# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from GB_parcing_methods.Lesson5.jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacansy):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={vacansy}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,' f-test-link-Dalshe')]/@href").extract_first()
        job_links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9 f-test-link')]/@href").extract()
        for link in job_links:
            link = link.split('?')[0]
            yield response.follow(link, callback=self.vacansy_parce)

        yield response.follow(next_page, callback=self.parse)


    def vacansy_parce(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        company_name = response.xpath("//h2[@class='_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI']/text()").extract()
        company_address = response.xpath("//span[@class='_3mfro _1hP6a _2JVkc']/text()").extract_first()
        yield JobparserItem(name=name, salary=salary, company_name=company_name, company_address=company_address, link=link)
