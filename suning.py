from time import sleep
from selenium import webdriver
import sys
import math
import re
from importlib import reload
import lxml.html
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
etree = lxml.html.etree
reload(sys)
import time
from inspection import run

def seleium_suning(item, num, type='综合'):
    type_list = ['综合', '销量', '评价数', '价格升序', '价格降序', '默认']
    if type not in type_list:
        raise Exception('无效的排序方法')
    per_page = 118
    page = math.ceil(num / per_page)
    count = 0
    text_list = []
    driver_path = r'chromedriver'
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get('https://search.suning.com/{}/'.format(item))
    if type == '综合':
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[1]').click()
    elif type == '销量':
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[2]').click()
    elif type == '评价数':
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[3]').click()
    elif type == '价格升序':
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[4]').click()
    elif type == '价格降序':
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[4]').click()
        sleep(2)
        browser.find_element_by_xpath('//*[@id="second-filter"]/div/div[1]/span[4]').click()
    js = 'window.scrollTo(0,document.body.scrollHeight)'
    browser.execute_script(js)
    sleep(2)
    browser.execute_script(js)
    sleep(2)
    while count < page:
        if count > 1:
            browser.find_element_by_xpath('//*[@id="nextPage"]').click()
            sleep(2)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            browser.execute_script(js)
            sleep(2)
            browser.execute_script(js)
        text = browser.page_source
        count += 1
        text_list.append(text)

    return text_list


def url_list(text_list):
    item_list = []
    time = datetime.now()
    for text in text_list:
        html = etree.HTML(text)
        urls = html.xpath('//*[@class="img-block"]/a/@href')
        # print(len(urls))
        i = 0
        for num in range(len(urls)):
            id1 = urls[num].split('/')[-2]
            id2 = urls[num].split('/')[-1].split('.')[0]
            item_id = id1 +'-'+id2
            try:
                price1 = html.xpath('//*[@class="def-price"]//text()')[num]
                price_html2 = html.xpath('//*[@id="{}"]/div/div/div[2]/div[1]/span/i'.format(item_id))[1]
                price2 = price_html2.xpath('string(.)').strip()
                price = price1 +price2
            except Exception as a:
                price = ''
            title_html = html.xpath('//*[@id="{}"]/div/div/div[2]/div[2]/a'.format(item_id))[0]
            title = title_html.xpath('string(.)').strip()
            item_url = 'https:'+str(urls[num])
            shop_html = html.xpath('//*[@id="{}"]/div/div/div[2]/div[4]/a'.format(item_id))[0]
            shop_name = shop_html.xpath('string(.)').strip()
            shop_url = html.xpath('//*[@id="{}"]/div/div/div[2]/div[4]/a/@href'.format(item_id))
            try:
                comment = html.xpath('//*[@id="{}"]/div/div/div[2]/div[3]/div/a/i/text()'.format(item_id))[0]
            except Exception as e:
                comment = ''
            item_dict = {}
            item_dict['time'] = time
            item_dict['item_url'] = item_url
            item_dict['price'] = price
            item_dict['title'] = title
            item_dict['shop_url'] = 'https:' + str(shop_url)
            item_dict['shop_name'] = shop_name
            item_dict['comment'] = comment.split('+')[0]
            item_list.append(item_dict)
            i += 1
    return item_list






def dict_to_list(item_list):
    detail_list = []
    for item in item_list:
        time = item['time']
        item_url = item['item_url']
        detil_dict = {}
        # item_url = 'https://product.suning.com/0000000000/646483774.html'
        driver_path = r'/home/zhanghaiyan/.config/google-chrome/chromedriver'
        brower = webdriver.Chrome(executable_path=driver_path)
        brower.get(item_url)
        text = brower.page_source
        html = etree.HTML(text)
        title_html = html.xpath('//*[@id="itemDisplayName"]')[0]
        title = title_html.xpath('string(.)').strip()
        price_html = html.xpath('//*[@id="mainPrice"]/dl[1]/dd/span')[0]
        price = price_html.xpath('string(.)').strip()
        detil_dict['title'] = title
        detil_dict['price'] = price
        detil_dict['item_id'] = item_url.split('/')[-1].split('.')[0]
        detail_list.append(detil_dict)
        detil_dict['time'] = time
        brower.quit()
    return detail_list

count = 0
for i in url_list(seleium_suning('手机', 100)):
    count = count + 1
    run('127.0.0.1:44179', str(count), i['item_url'], '苏宁')
    break



