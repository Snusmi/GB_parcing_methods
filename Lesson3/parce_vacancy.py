from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
import numpy as np
import urllib.parse
import re

class Vacancies:
    """searching vacancies in Moscow on hh.ru and/or superjob.ru"""
    
    def __init__(self):
        pass
    
    def find(self, yourtext, n_pages, site):
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
        vacansies = []
        
        if site == 'hh' or site == 'all':
            main_link = 'https://hh.ru/search/vacancy'
            
            for i in range(n_pages):
                params = {'area': 1, 'st': 'searchVacancy', 'text': yourtext, 'page': i}
                response = requests.get(main_link, params=params, headers = header)
                soup = bs(response.text,'lxml')

                vacansies_block = soup.find('div',{'class':'vacancy-serp'})
                vacansies_list = vacansies_block('div',{'class':'vacancy-serp-item'})

                for element in vacansies_list:
                    element_data = {}
                    element_link = None
                    element_name = None
                    element_employer_name = None
                    element_address = None
                    salary_text = None
                    salary_min = None
                    salary_max = None
                    salary_crrency = None

                    element_link = element.find(attrs={'data-qa': 'vacancy-serp__vacancy-title'}, href=True)['href'].split('?')[0]
                    element_name = element.find(attrs={'data-qa': 'vacancy-serp__vacancy-title'}).getText()
                    element_employer_name = element.find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).getText()
                    element_address = element.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).getText()
                    salary_text = element.find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})

                    if salary_text:
                        salary_text = salary_text.getText().replace(u'\xa0', u'')
                        salaries =  re.findall('\d+', salary_text)
                        text = re.findall('[a-zA-Zа-яА-Я]+', salary_text)
                        if 'до' in text:
                            salary_max = int(salaries[0])
                            salary_crrency = text[1]
                        elif 'от' in text:
                            salary_min = int(salaries[0])
                            salary_crrency = text[1]
                        elif len(salaries) == 2:
                            salary_min = int(salaries[0])
                            salary_max = int(salaries[1])
                            salary_crrency = text[0]

                    element_data['name'] = element_name
                    element_data['link'] = element_link
                    element_data['salary_min'] = int(salary_min)
                    element_data['salary_max'] = int(salary_max)
                    element_data['salary_currency'] = salary_crrency
                    element_data['employer'] = element_employer_name
                    element_data['address'] = element_address
                    element_data['site'] = 'hh.ru'

                    vacansies.append(element_data)

                next_button = soup.find(attrs={'data-qa': 'pager-next'}, href=True)
                if not next_button:
                    break  
                    
        if site == 'sj' or site == 'all':                    
            main_link = 'https://www.superjob.ru/vacancy/search/'

            for i in range(n_pages):
                params = {'keywords': yourtext, 'geo%5Bt%5D%5B0%5D': 4, 'page': i+1}
                response = requests.get(main_link, params=params, headers = header)
                soup = bs(response.text,'lxml')

                vacansies_block = soup.find('div',{'class':'_1ID8B'})
                vacansies_list = vacansies_block('div',{'class':'_3zucV f-test-vacancy-item _3j3cA RwN9e _3tNK- _1NStQ _1I1pc'})

                for element in vacansies_list:
                    element_data = {}
                    element_link = None
                    element_name = None
                    element_employer_name = None
                    element_address = None
                    salary_text = None
                    salary_min = None
                    salary_max = None
                    salary_crrency = None

                    element_link = element.find(href=True)['href'].split('?')[0]
                    element_link = 'https://www.superjob.ru' + element_link
                    element_name = element.find(href=True).getText()
                    element_employer_name = element.find(attrs={'class': 'f-test-text-vacancy-item-company-name'}).getText()
                    element_address = element.find(attrs={'class': 'f-test-text-company-item-location'})
                    element_address = element_address('span')[-1].getText()
                    salary_text = element.find(attrs={'class': 'f-test-text-company-item-salary'}).getText().replace(u'\xa0', u'')

                    salaries =  re.findall('\d+', salary_text)
                    text = re.findall('[a-zA-Zа-яА-Я]+', salary_text)

                    if 'до' in text:
                        salary_max = int(salaries[0])
                        salary_crrency = text[1]
                    elif 'от' in text:
                        salary_min = int(salaries[0])
                        salary_crrency = text[1]
                    elif len(salaries) == 2:
                        salary_min = int(salaries[0])
                        salary_max = int(salaries[1])
                        salary_crrency = text[0]

                    element_data['name'] = element_name
                    element_data['link'] = element_link
                    element_data['salary_min'] = int(salary_min)
                    element_data['salary_max'] = int(salary_max)
                    element_data['salary_currency'] = salary_crrency
                    element_data['employer'] = element_employer_name
                    element_data['address'] = element_address
                    element_data['site'] = 'superjob.ru'

                    vacansies.append(element_data)

                next_button = soup(attrs={'class': 'f-test-button-dalshe'})
                if not next_button:
                    break
                    
        return vacansies
    
    def get_table(self, vacansies):
        df = pd.DataFrame.from_dict(vacansies)
        return df