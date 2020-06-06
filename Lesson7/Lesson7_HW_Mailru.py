""""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NewPassword172
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

driver = webdriver.Chrome()
driver.get('https://m.mail.ru/login')

elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)

letters_links = []

while True:
    letters = driver.find_elements_by_class_name('messageline__link')
    for letter in letters:
        link = letter.get_attribute('href')
        letters_links.append(link)
    next_button = driver.find_element_by_xpath('//a[@title="Следующая страница"]')
    if not next_button:
        break
    next_button.click()

letters=[]
for link in letters_links:
    letter_data = {}
    driver.get(link)
    letter_theme = driver.find_element_by_class_name('readmsg__theme').text
    letter_from = driver.find_element_by_xpath("//div[@class='readmsg__text-container__inner-line']/a/strong").text
    letter_date = driver.find_element_by_class_name('readmsg__mail-date').text
    letter_message = driver.find_element_by_id('readmsg__body').text
    letter_data['from'] = letter_from
    letter_data['date'] = letter_date
    letter_data['theme'] = letter_theme
    letter_data['message'] = letter_message
    letters.append(letter_data)

driver.quit()


client = MongoClient('localhost', 27017)
db = client['letters']
mailru = db.mailru

for element in letters:
    mailru.insert_one(element)