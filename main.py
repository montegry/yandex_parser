import re
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import nltk
import json


def searching_clicker(search_name):
    '''
    Searching on page
    :param search_name: name of search
    :return: page
    '''
    q1 = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div[1]/span/span/input')
    q1.send_keys(search_name)
    q = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div[2]/button')
    q.click()


def searching_clicker_next_search(search_name):
    '''
    Searching on page
    :param search_name: name of search
    :return: page
    '''
    q1 = driver.find_element_by_xpath('/html/body/header/div/div/div[3]/form/div[1]/span/span/input')
    q1.clear()
    q1.send_keys(search_name)
    q = driver.find_element_by_xpath('/html/body/header/div/div/div[3]/form/div[2]/button/div')
    q.click()


def next_page(soup, cat_name):
    '''
    Going on next page in search results and parse all links there
    :return:
    '''
    for every_page in soup:
        if every_page['aria-label'] != "Следующая страница":
            zapros = "https://yandex.ru" + every_page['href']
            driver.get(zapros)
            search_page_parser(driver.page_source, cat_name)


def page_parser(soup):
    '''
    Parsing to token
    :param soup: page to parse
    :return: list with words
    '''
    tokenizer = nltk.RegexpTokenizer(r'[^\d\W]\w+')
    # return tokenizer.tokenize(soup.text)
    print("Cooking token...")


def that_i_need(tag):
    return tag.has_attr('aria-label') and tag.name == 'a'


def search_page_parser(page, key_name):
    '''
    Taking page with search results and goes to every result page and parse it
    :param key_name: Name of category to be addded as key in json
    :param page: page source from driver
    :return:  tokenized all pages in result
    '''
    soup = BeautifulSoup(page, "lxml")
    list_of_tokenized_words = []
    # for i in soup.find_all('h2'):
    #   print (i)
    for i in soup.find_all('h2', 'OrganicTitle Typo Typo_text_l Typo_line_m organic__title-wrapper'):
        url_result = i.a['href']
        req_result = requests.get(url_result)
        soup_result = BeautifulSoup(req_result.text, "lxml")
        tokenizer = nltk.RegexpTokenizer(r'[^\d\W]\w+')
        q = tokenizer.tokenize(soup_result.text)
        list_of_tokenized_words.append(q)
    # for i in range(len(list_of_tokenized_words)):
        # print("One token size = ", len(list_of_tokenized_words[i]), "\t Token:", list_of_tokenized_words[i])
    print("Cooking token...", len(list_of_tokenized_words))
    for_json_dict = {key_name: list_of_tokenized_words}
    with open('tokenize.json', "a", encoding='utf-8') as f:
        print("Token cooked, writing in file...")
        json.dump(for_json_dict, f)
    return list_of_tokenized_words


categories = ['События', 'Советы', 'Справочники развлечений']
driver = webdriver.Chrome(executable_path='/home/a123456/Downloads/chromedriver')
driver.get('https://ya.ru')

  # FIRST CATEGORY SEARCH
searching_clicker(categories[0])  # Open Search enter first category and click Find
time.sleep(1)
search_page_parser(driver.page_source, categories[0])  # Parsing all pages from search results PAGE 1
soup = BeautifulSoup(driver.page_source, 'lxml')  # making soup from page 1 to make links
soup_of_a = soup.find_all('div', 'pager__items')[0].find_all('a')  # finding paginator on page
next_page(soup_of_a, categories[0])  # Paginator chain, going on every next page (5 pages) parsing all links in results
  # NEXT CATEGORIES SEARCH
for i in range(2):  # takes next in categories
    searching_clicker_next_search(categories[i + 1])  # Open Search enter category and click FIND
    search_page_parser(driver.page_source, categories[i + 1])  # Parsing all pages from search results
    soup = BeautifulSoup(driver.page_source, "lxml")
    soup_of_a = soup.find_all('div', 'pager__items')[0].find_all('a')
    next_page(soup_of_a, categories[i+1])
