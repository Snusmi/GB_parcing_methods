from lxml import html
from pprint import pprint
import requests

header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
main_link = 'https://www.etsy.com/listing/667282692/fathers-day-gift-for-dadengraved?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery-1-1&plkey=3df417be871fdadaf3c05a8cbd4ac2e78a8ad045%3A667282692&pro=1'
response = requests.get(main_link, headers = header)
dom = html.fromstring(response.text)

next_page = dom.xpath("//li[@class='wt-action-group__item-container'][last()]/a[@data-page]/@href")
# print(next_page)
response = requests.get(next_page[0], headers = header)
dom = html.fromstring(response.text)

# dates = dom.xpath('//div[@data-review-region]/div[1]/p/text()')
# rating = dom.xpath("//div[@data-review-region]//span[contains(@class,'display-inline-block')]/span[2]/span[last()]/@data-rating")
# text = dom.xpath("//div[contains(@class,'break-word')]/text()")
#
reviews = []
# for i in range(len(dates)):
#     data = {}
#     data['date'] = dates[i]
#     data['rating'] = rating[i]
#     data['text'] = text[i]
#     reviews.append(data)
#
# pprint(reviews)

blocks = dom.xpath("//div[@data-review-region]")
for block in blocks:
    data = {}
    data['date'] = block.xpath('./div[1]/p/text()')
    data['rating'] = int(block.xpath(".//span[contains(@class,'display-inline-block')]/span[2]/span[last()]/@data-rating")[0])+1
    data['text'] = block.xpath(".//div[contains(@class,'break-word')]/text()")[0].replace('\n','')
    reviews.append(data)
pprint(reviews)