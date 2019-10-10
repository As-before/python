# coding=utf-8
import xlrd
from selenium import webdriver
import time
import lxml.html
import pymysql
import math

etree = lxml.html.etree


class excelHandle:

    def decode(self, filename, sheetname):
        return filename, sheetname

    def read_excel(self, filename, sheetname):
        filename, sheetname = self.decode(filename, sheetname)
        rbook = xlrd.open_workbook(filename)
        sheet = rbook.sheet_by_name(sheetname)
        rows = sheet.nrows
        cols = sheet.ncols
        all_content = []
        for i in range(rows):
            row_content = []
            for j in range(cols):
                cell = sheet.cell_value(i, j)
                row_content.append(cell)
            all_content.append(row_content)
            # print('[' + ','.join("'" + str(element) + "'" for element in row_content) + ']')
        return all_content

    def connect_mysql(self, item, table):
        db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                              port=3306)
        cursor = db1.cursor()
        for i in item:
            uid = int(i['uid'])
            zx = 'Z2019064'
            shop_url = i['shop_url']
            shop_name = i['shop_name']
            title = i['title']
            item_url = i['url']
            sale = i['sale']
            price = i['price']
            sql = 'insert into %s(uid,zx,shop_url,shop_name,title,item_url,sale,price) values(%d, "%s","%s","%s","%s","%s","%s",%f)' % (
            table, uid, zx, shop_url, shop_name, title, item_url, sale, float(price))
            cursor.execute(sql)
        db1.commit()
        cursor.close()
        db1.close()


if __name__ == '__main__':
    # ll = [{'domain': '.taobao.com', 'expiry': 1585138926, 'httpOnly': False, 'name': 'isg', 'path': '/', 'secure': False, 'value': 'BKWlls5RFCntsnB16eFFeW7LtGjV6OwB2ElEgqeKXVztvsUwbzJqRq1cTGNtvnEs'}, {'domain': '.taobao.com', 'expiry': 1601122932, 'httpOnly': False, 'name': 'x', 'path': '/', 'secure': False, 'value': 'e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0'}, {'domain': 'shop73352554.taobao.com', 'httpOnly': False, 'name': 'swfstore', 'path': '/', 'secure': False, 'value': '314040'}, {'domain': '.taobao.com', 'expiry': 1601122923.19327, 'httpOnly': False, 'name': 'tracknick', 'path': '/', 'secure': False, 'value': 'tb928237077'}, {'domain': 'shop73352554.taobao.com', 'expiry': 1572178924, 'httpOnly': False, 'name': 'pnm_cku822', 'path': '/', 'secure': False, 'value': '098%23E1hv09vUvbpvjQCkvvvvvjiPRFcZgjlhPFFwgjivPmPp0jYjRsM90jEVPLsWtj%2F5vpvhphvhHvhCvvXvppvvvvmivpvUphvhrL5xFjmEvpvVpyUUmE%2BOKphv8hCvvVQvvhv2phvwYvvvp%2FxvpCQmvvChNhCvjPpvvhBXphvwYvvvBHyEvpCWBmwsv8RKNCyf8z7gndUKoLBwMRvXVzC8JZ5vsCOqb6OyCW2%2B%2BfvsxeCBtR9t%2BFBCWDAvD40fjovDN%2BClHdUf8169D70fdeQEVAilYvGCvvpvvvvvRphvChCvvvv%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie1', 'path': '/', 'secure': False, 'value': 'W50Of5XbimjJg19Zbx%2FesTLZciqOUwdUNvbzLdkzDpk%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_nk_', 'path': '/', 'secure': False, 'value': 'tb928237077'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'sg', 'path': '/', 'secure': False, 'value': '79b'}, {'domain': '.taobao.com', 'expiry': 1572178923.193194, 'httpOnly': True, 'name': 'uc4', 'path': '/', 'secure': False, 'value': 'nk4=0%40FY4HXgGxbq6eLVJtd%2FTYrf1dRH%2BItw%3D%3D&id4=0%40U2grF8wUokjWxmLX1oPiKpYlcwHEm3IX'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'skt', 'path': '/', 'secure': False, 'value': 'de229007ea421237'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie17', 'path': '/', 'secure': False, 'value': 'UUphzOfZfIgbMqzt5g%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'whl', 'path': '/', 'secure': False, 'value': '-1%260%260%260'}, {'domain': '.taobao.com', 'expiry': 1623586923.193541, 'httpOnly': False, 'name': 'tg', 'path': '/', 'secure': False, 'value': '5'}, {'domain': '.taobao.com', 'expiry': 1601122923.193422, 'httpOnly': False, 'name': '_cc_', 'path': '/', 'secure': False, 'value': 'U%2BGCWk%2F7og%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_tb_token_', 'path': '/', 'secure': False, 'value': 'db855b3b736e'}, {'domain': '.taobao.com', 'expiry': 1572178923.192631, 'httpOnly': True, 'name': 'uc3', 'path': '/', 'secure': False, 'value': 'nk2=F5RMGyu%2Bv4RTkQg%3D&id2=UUphzOfZfIgbMqzt5g%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuHatwgF1wI76Gc%3D'}, {'domain': '.taobao.com', 'expiry': 1585138927, 'httpOnly': False, 'name': 'l', 'path': '/', 'secure': False, 'value': 'cBQtUL_VqmzKdaTbBOCimZ_XJF7TvIRAguWfhbhvi_5Ix1LwKFQOk6a05ep6cjXd9I8BqbJ1Qkw9-eteihX_JuPkDBWN.'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'uc1', 'path': '/', 'secure': False, 'value': 'cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=URm48syIZx9a&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTaEcQaFA8aFw%3D%3D&tag=8&lng=zh_CN'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': '_l_g_', 'path': '/', 'secure': False, 'value': 'Ug%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'csg', 'path': '/', 'secure': False, 'value': '45f60420'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'v', 'path': '/', 'secure': False, 'value': '0'}, {'domain': '.taobao.com', 'expiry': 1570191726.202845, 'httpOnly': False, 'name': 'mt', 'path': '/', 'secure': False, 'value': 'ci=1_1'}, {'domain': '.taobao.com', 'expiry': 2200306904, 'httpOnly': False, 'name': 'cna', 'path': '/', 'secure': False, 'value': '2OwUFlt++FUCAd2F84S1Q577'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'existShop', 'path': '/', 'secure': False, 'value': 'MTU2OTU4NjkyMw%3D%3D'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'unb', 'path': '/', 'secure': False, 'value': '2206577557789'}, {'domain': '.taobao.com', 'httpOnly': True, 'name': 'cookie2', 'path': '/', 'secure': False, 'value': '1769fff091a245316bb8b2cdf427194e'}, {'domain': '.taobao.com', 'expiry': 1577362923.192888, 'httpOnly': False, 'name': 't', 'path': '/', 'secure': False, 'value': '8e6027f3281e576848a5095ec47b693c'}, {'domain': '.taobao.com', 'expiry': 1572178923.192829, 'httpOnly': False, 'name': 'lgc', 'path': '/', 'secure': False, 'value': 'tb928237077'}, {'domain': '.taobao.com', 'httpOnly': False, 'name': 'dnk', 'path': '/', 'secure': False, 'value': 'tb928237077'}, {'domain': '.taobao.com', 'expiry': 1601122898.498865, 'httpOnly': False, 'name': 'thw', 'path': '/', 'secure': False, 'value': 'cn'}]
    eh = excelHandle()
    filename = r'/home/pang/gitlab/test/did_automation/pang/1092.xlsx'
    sheetname = 'Sheet1'
    browser = webdriver.Chrome()
    browser.get('https://shop73352554.taobao.com/category.htm?search=y')
    # time.sleep(30)
    # print(browser.get_cookies())
    # browser.close()
    # exit(0)
    # for i in ll:
    #     browser.add_cookie(i)
    texts = eh.read_excel(filename, sheetname)
    for text in range(len(texts)):
        if texts[text][4] == '淘宝':
            item_list = []
            text_list = []
            url = texts[text][2]
            browser.get('{}'.format(url))
            time.sleep(2)
            try:
                browser.find_element_by_xpath('//a[@class=" jCurrent   down "]').click()
                time.sleep(10)
            except Exception as a:
                time.sleep(10)
                with open('fail_txt', 'a') as fb:
                    fb.write(str(texts[text][1]))
                    fb.close()
                continue
            time.sleep(10)
            text1 = browser.page_source
            text_list.append(text1)
            html1 = etree.HTML(text1)
            try:
                most_project = html1.xpath('//*[@class="jPage"]//a/text()')[-1]
                page = int(most_project)
            except Exception as e:
                page = int(html1.xpath('//*[@class="jPage"]//a/text()')[-2])
                with open('fail_txt', 'a') as sb:
                    sb.write(str(texts[text][1]))
                    sb.close()
                continue
            page = math.ceil(int(most_project) / 24)
            for i in range(page):
                try:
                    browser.find_element_by_xpath('//*[@class="jPage"]/a[-1]').click()
                    time.sleep(2)
                except Exception as a:
                    with open('fail_txt', 'a') as sb:
                        sb.write(str(texts[text][1]))
                        sb.close()
                    break
                text2 = browser.page_source
                text_list.append(text2)
            j = 0
            for Html in text_list:
                html = etree.HTML(Html)
                count = len(html.xpath('//*[@id="J_GoodsList"]/ul//li'))
                print(count)
                for i in range(int(count)):
                    item_dict = {}
                    try:
                        item_url = 'https:' + html.xpath('//*[@class="item "or@class="item last"]/dt/a/@href')[i]
                        title = html.xpath('//*[@class="item "or@class="item last"]/dt/a/img/@alt')[i]
                        price = html.xpath('//*[@class="item "or@class="item last"]/dd[1]/div/div/span[2]/text()')[i]
                        sale = html.xpath('//*[@class="sale-area"]/span/text()')[i]
                    except Exception as a:
                        break
                    old_id = texts[text][0]
                    shop_url = texts[text][2]
                    shop_name = texts[text][6]
                    item_dict['uid'] = old_id
                    item_dict['shop_url'] = shop_url
                    item_dict['shop_name'] = shop_name
                    item_dict['title'] = title
                    item_dict['url'] = item_url
                    item_dict['sale'] = sale
                    item_dict['price'] = price
                    if j < 1:
                        if i <= 4:
                            print(item_dict)
                            item_list_fifith = []
                            item_list_fifith.append(item_dict)
                            eh.connect_mysql(item_list_fifith, 'Top5_shop_url')
                            with open('text3.txt', 'a') as fp:
                                fp.write(str(item_dict) + ',')
                            fp.close()
                    item_list.append(item_dict)
                j += 1
            eh.connect_mysql(item_list, 'add_goods')
        else:
            continue
    browser.quit()
