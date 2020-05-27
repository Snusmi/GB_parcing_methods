from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from GB_parcing_methods.Lesson5.jobparser.spiders.hhru import HhruSpider
from GB_parcing_methods.Lesson5.jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # answer = input('Введите вакансию')

    process.crawl(HhruSpider,vacansy = 'python')
    process.crawl(SjruSpider, vacansy='python')

    process.start()