from datetime import datetime
from time import sleep
import math
import lxml.html

etree = lxml.html.etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from inspection import run


def spider_jd(item, num, type='默认'):
    type_list = ['综合', '销量', '评价数', '价格升序', '价格降序', '新品', '默认']
    if type not in type_list:
        raise Exception('无效的排序')
    text_list = []
    per_page = 60
    page = math.ceil(num / per_page)
    count = 0
    driver_path = r'chromedriver'
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get('https://www.jd.com/')
    browser.find_element_by_xpath('//*[@id="key"]').send_keys(item)
    browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
    if type == '综合':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[1]').click()
    elif type == '销量':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[2]').click()
    elif type == '评论数':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[3]').click()
    elif type == '新品':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[4]').click()
    elif type == '价格升序':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[5]').click()
    elif type == '价格降序':
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[5]').click()
        sleep(2)
        browser.find_element_by_xpath('//*[@id="J_filter"]/div[1]/div[1]/a[5]').click()
        '''下滑到底'''
    js = 'window.scrollTo(0,document.body.scrollHeight)'
    browser.execute_script(js)
    sleep(2)
    browser.execute_script(js)
    sleep(2)
    wait = WebDriverWait(browser, 10, 0.5)
    print('ok')
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="J_goodsList"]/ul/li[60]')))
    while count < page:
        if count > 1:
            browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
            sleep(2)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            browser.execute_script(js)
            sleep(2)
            browser.execute_script(js)
        text = browser.page_source
        count += 1
        text_list.append(text)
    browser.quit()
    return text_list


def url_list(text_list):
    item_list = []
    time = datetime.now()
    for text in text_list:
        html = etree.HTML(text)
        urls = html.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/@href')
        # print(len(urls))
        i = 0
        for num in range(len(urls)):
            price_html = html.xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[2]/strong/i'.format(num + 1))[0]
            price = price_html.xpath('string(.)').strip()
            # print(type(price))
            title_html = html.xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[3]/a/em'.format(num + 1))[0]
            title = title_html.xpath('string(.)').strip()
            shop_url = html.xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[5]/span/a/@href'.format(num + 1))[0]
            shop_html = html.xpath('//*[@id="J_goodsList"]/ul/li[{}]/div/div[5]/span/a'.format(num + 1))[0]
            shop_name = shop_html.xpath('string(.)').strip()
            item_id = urls[num].split('/')[-1].split('.')[0]
            # print(item_id)
            comment_html = html.xpath('//*[@id="J_comment_{}"]'.format(item_id))[0]
            comment = comment_html.xpath('string(.)').strip()
            item_dict = {}
            item_dict['time'] = time
            item_dict['item_url'] = 'https:' + str(urls[num])
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
        driver_path = r'/home/zhanghaiyan/.config/google-chrome/chromedriver'
        # item_url = 'https://item.jd.com/1030774.html'
        brower = webdriver.Chrome(executable_path=driver_path)
        brower.get(item_url)
        text = brower.page_source
        html = etree.HTML(text)
        title_html = html.xpath('/html/body/div[6]/div/div[2]/div[1]')[0]
        title = title_html.xpath('string(.)').strip()
        price_html = html.xpath('/html/body/div[6]/div/div[2]/div[4]/div/div[1]/div[2]/span[1]/span[2]')[0]
        price = price_html.xpath('string(.)').strip()
        detil_dict['title'] = title
        detil_dict['price'] = price
        detil_dict['item_id'] = item_url.split('/')[-1].split('.')[0]
        detail_list.append(detil_dict)
        detil_dict['time'] = time
        print(detil_dict)
        detail_list.append(detil_dict)
        brower.quit()
    return detail_list


count = 0
dt = url_list(spider_jd('jiu', 1))
for item in dt:
    count = count + 1
    # data = {'id': count, 'url': item['item_url'], 'name': item['title']}
    gg = run('127.0.0.1:9222', count, item['item_url'], item['title'])
