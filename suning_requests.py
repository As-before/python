import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import hashlib
import pymysql

headers = {
    'Host': 'search.suning.com',
    'Referer': 'https://search.suning.com/%E7%BB%8D%E5%85%B4%E9%BB%84%E9%85%92/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}


def getLastDate():
    '''
    获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
    :return: 返回格式化后的时间数据
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def object_mysql(table, goodsList, flag=''):
    '''
    传入相应的数据，插入到指定的数据库
    :param flag:
    :param goodsList:
    :param table: 表名称
    :return:
    '''
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    cursor = db1.cursor()
    if flag == '':
        for item in goodsList:
            sql = 'insert into %s(project,dates,key_id,key_name,key_tag,' \
                  'key_platform,key_place,item_url,item_price,item_title,item_sales,item_' \
                  'comment,shop_url,shop_name,shop_address,tag2) values("%s", ' \
                  '"%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s")' % (
                      table, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],
                      item[9],
                      item[10], item[11], item[12], item[13], item[14], item[15])
            cursor.execute(sql)
    else:
        for item in goodsList:
            sql = 'insert into %s(project,dates,key_id,key_name,key_tag,' \
                  'key_platform,key_place,item_url,item_price,item_title,item_sales,item_' \
                  'comment,shop_url,shop_name,shop_address,tag1,tag2) values("%s", ' \
                  '"%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                      table, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],
                      item[9],
                      item[10], item[11], item[12], item[13], item[14], flag, item[15])
            cursor.execute(sql)
    db1.commit()
    cursor.close()
    db1.close()


def getLastDate():
    '''
    获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
    :return: 返回格式化后的时间数据
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def searchSuningKey(key, num):
    datas = []
    if num % 30 == 0:
        page = num // 30
    else:
        page = (num // 30) + 1
    headers = {
        'Host': 'search.suning.com',
        'Referer': 'https://search.suning.com/%E7%BB%8D%E5%85%B4%E9%BB%84%E9%85%92/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    for p in range(1, page+1):
        url = "https://search.suning.com/emall/searchV1Product.do?keyword={}&ci=0&pg=01&paging={}".format(key,p)
        try:
            rs = requests.get(url, headers=headers, timeout=5)
            datas.append(rs.text)
        except Exception as e:
            return e
    return datas


def suningGoodsUrl(htmlList):
    '''
    解析html数据列表，生成字典数据
    :param htmlList:html数据列表
    :return: 需要的字段字典
    '''
    time = datetime.now()
    dataList = []
    for eachhtml in htmlList:
        soup=BeautifulSoup(eachhtml, 'html.parser')
        items=soup.find_all('div', {'class': 'product-box'})
        for item in items:
            try:
                item_title = item.find('div', {'class': 'res-info'}).find('div', {'class': 'title-selling-point'}).get_text().strip().replace('\n','').replace(' ','')
                item_url = 'https:' + item.find('div', {'class': 'res-info'}).find('div', {'class': 'title-selling-point'}).find('a').get('href')
                shop_name = item.find('div', {'class': 'res-info'}).find('div', {'class': 'store-stock'}).find('a').text
                shop_url = item.find('div', {'class': 'res-info'}).find('div', {'class': 'store-stock'}).find('a').get('href')
                if shop_url == "javascript:void(0);":
                    shop_url = ''
                else:
                    shop_url = 'https:' + shop_url
                prices = item.find('div', {'class': 'res-info'}).find('div', {'class': 'price-box'}).find('span')
                brand_id = prices.get('brand_id')
                datasku = prices.get('datasku').split('|')
                threegroup_id = prices.get('threegroup_id')
                try:
                    price_url = 'https://ds.suning.com/ds/generalForTile/0000000{}__2_{}-025-2-0000000000-1--ds0000000009487.jsonp?callback=ds0000000009487'.format(datasku[0],datasku[-1])
                    price_data = requests.get(price_url,headers)
                    com = re.compile('ds000000000.*?\((.*?)\)', re.S)
                    ds = re.findall(com,price_data.text)
                    item_price = json.loads(ds[0])['rs'][0]['price']
                except Exception as e:
                    print(e)
                    continue
                if not item_price:
                    continue
                try:
                    good_comment = item.find('div', {'class': 'res-info'}).find('div', {'class': 'evaluate-old clearfix'}).find('div', {'class':'info-evaluate'}).find('a').find('i').text
                except:
                    good_comment = ''
                dataList.append({'time': time, "item_url": item_url, 'item_title': item_title,
                                 "item_price": item_price,
                                 'shop_address': '', 'shop_url': shop_url, 'shop_name': shop_name,
                                 'Sales': '', 'comment_num': good_comment})
            except Exception as e:
                print(e)
    print('抓取到{}条数据'.format(len(dataList)))
    return dataList


def get_suning(project, key_name, key_tag, key_platform, key_place, match):
    '''
    主函数，负责协调各函数
    :return:
    '''
    # 判断是否是第一次检测还是持续检测
    flag = input('专项:{} 平台：{} 专项关键词：{} 输入?1(第一次检测),2(持续检测)：'.format(project, key_platform, key_name))
    goodsData = []
    try:
        flag = int(flag)
    except Exception as e:
        return '请正确输入'
    # 设置专项号等数据
    num = 30  # 数据条数
    urlList = set()  # 记录重复数值
    for keys in key_name:
        key_id = keys.split(':')[0]
        key = keys.split(':')[1]
        # 查询搜索商品的所有数据
        dataList = searchSuningKey(key, num)
        dates = getLastDate()  # 获取时间
        goodsList = suningGoodsUrl(dataList)  # 获取所有商品数据
        for i in goodsList:
            try:
                item_url = i['item_url'].split('&')[0]
            except Exception as e:
                item_url = i['item_url']
            item_price = i['item_price']
            item_title = i['item_title']
            res = re.search(match, item_title)
            if not res:
                continue
            item_sales = i['Sales']
            item_comment = i['comment_num']
            shop_url = i['shop_url']
            shop_name = i['shop_name']
            shop_address = i['shop_address']
            m = hashlib.md5()
            m.update(item_url.encode('utf-8'))
            tag2 = m.hexdigest()
            if tag2 not in urlList:
                goodsData.append(
                    [project, dates, key_id, key, key_tag, key_platform, key_place, item_url, item_price, item_title,
                     item_sales, item_comment, shop_url, shop_name, shop_address, tag2])
            urlList.add(tag2)

    if flag == 1:
        pass
        # 第一次检测入数据表以及留证表
        # object_mysql('object', goodsData)
        # object_mysql('licence_object', goodsData, 'new')
    elif flag == 2:
        # 持续检测只入数据表
        # object_mysql('object', goodsData)
        for item in goodsData:
            print(item)
    else:
        return '请输入正确的数字'

# if __name__ == "__main__":
#     project = ['Z2019072', 'Z2019073']  # 专项号
#     key_name = [['6:嘉兴粽子'], ['7:绍兴黄酒']]  # 专项关键词 关键词id：关键词名称
#     key_tag = ["浙江嘉兴;粽子", "浙江绍兴;黄酒"]  # 专项标签
#     # key_platform = [['淘宝', '京东', '拼多多'], ['淘宝', '京东']]  # 专项检测平台
#     key_platform = [['苏宁'], []]  # 专项检测平台
#     key_place = ['嘉兴', '绍兴']  # 检测地区
#     search = ['.*粽.*嘉兴|.*嘉兴.*粽','.*酒.*绍兴|.*绍兴.*酒']
#     for i in range(len(project)):
#         for platform in key_platform[i]:
#             if platform == '苏宁':
#                 # print(platform)
#                 get_suning(project[i], key_name[i], key_tag[i], platform, key_place[i], search[i])
#     # 调用检测函数
#     # licence.run()
#     # 调用查询函数对当日数据进行留证
#     # select_mysql()