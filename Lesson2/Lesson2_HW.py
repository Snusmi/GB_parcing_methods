from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import numpy as np
import urllib.parse

yourtext = 'python разработчик'
main_link = 'https://hh.ru/search/vacancy'
params = {'area': 1, 'st': 'searchVacancy', 'text': yourtext}
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}

response = requests.get(main_link, params=params, headers = header)
soup = bs(response.text,'lxml')
vacansies_block = soup.find('div',{'class':'vacancy-serp'})
vacansies_list = vacansies_block.findChildren(recursive=False)

vacansies = []
for element in vacansies:
    element_data = {}
    element_name = element.find('span', {'class': 'resume-search-item__name'}).getText()
    print(element_name)
    break

