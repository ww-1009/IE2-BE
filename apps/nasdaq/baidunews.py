#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
file_name = 'news_top.txt'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome(executable_path=(r'./chromedriver'), options=chrome_options)
driver = webdriver.Chrome(executable_path=(r'./chromedriver'))
driver.implicitly_wait(30)
baseURL='https://top.baidu.com/board?tab=realtime'
driver.get(baseURL)
html = driver.page_source
tree = etree.HTML(html)
try:
    lis=tree.xpath('//div[@class="content_1YWBm"]/a')
    links = tree.xpath('//div[@class="content_1YWBm"]/a/@href')
    title = tree.xpath('//div[@class="content_1YWBm"]/a/div[@class="c-single-text-ellipsis"]/text()')
    img = tree.xpath('//a[@class="img-wrapper_29V76"]/img/@src')
    with open(file_name, 'w',encoding='utf-8') as file_obj:
        for i in range(10):
            file_obj.write(title[i]+';'+links[i]+'\n')
            print(title[i], links[i])
        file_obj.write(img[0] + '\n')
except Exception as e:
    print(e)
driver.close()
driver.quit()
