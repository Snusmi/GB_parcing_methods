from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'https://www.kinopoisk.ru'
params = {'quick_filters':'serials'}
html = requests.get(main_link+'/popular',params=params).text

soup = bs(html,'lxml')

serials_block = soup.find('div',{'class':'selection-list'})
serials_list = serials_block.findChildren(recursive=False)


serials = []
for serial in serials_list:
    serial_data = {}
    serial_link = main_link + serial.find('a',{'class':'selection-film-item-meta__link'})['href']
    serial_name = serial.find('p').getText()
    serial_genre = serial.find('span',{'class':'selection-film-item-meta__meta-additional-item'}).find_next_sibling().getText()
    serial_rating = serial.find('span',{'class':'rating__value'}).getText()

    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['genre'] = serial_genre
    serial_data['rating'] = float(serial_rating)
    serials.append(serial_data)

pprint(serials)
