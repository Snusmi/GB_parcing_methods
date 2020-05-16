from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

link = 'http://127.0.0.1:5000/'
response = requests.get(link).text

soup = bs(response,'lxml')

# elem = soup.find('a').findParent().findParent()

# div = soup.find('p',{'id':'clickable'}).getText()

# text = soup.find('a').getText()

# a = soup.find('a')['href']

# elems = soup.find_all(attrs={'class':'red'})

# elems = soup.find_all('p',limit=3)

# children = soup.find('div',{'id':'d'}).findChildren(recursive=False)

# elem = soup.find(text='Шестой параграф').findParent()

# print(elem)
# print('---------------------------')
pprint(elem)
