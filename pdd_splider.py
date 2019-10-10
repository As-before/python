from pyppeteer import connect
import asyncio
import time
import json
from urllib import parse
from datetime import datetime
from inspection import run
import hashlib
import requests
import pymysql
import licence_test
import re

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

def searchPddKey(key, num, remote_chrome_url):
    """
    :param num:
    :param key:搜索关键词
    :param ws:chrome的ws值,前期需要对chrome进行拼多多登陆，才能获取到数据
    :return:返回每一页商品信息列表
    """
    pageList = []

    def getWs(chrome_url):
        ws = requests.get(url='http://' + chrome_url + "/json/version").json()["webSocketDebuggerUrl"]
        return ws

    async def intercept_response(res):
        if res.request.resourceType in ['other']:
            resp = await res.text()
            if str(resp).find('{"q_opt":0,"server_time":') == 0:
                pageList.append(str(resp))

    async def main(key):
        browser = await connect({
            "browserWSEndpoint": getWs(remote_chrome_url)
        })
        page = await browser.newPage()
        page.on('response', intercept_response)
        # await page.setViewport({'width': 1080, 'height': 960})
        await page.goto('http://yangkeduo.com/search_result.html?search_key={}'.format(parse.quote(key)))
        await asyncio.sleep(3)
        await page.waitFor(2000)
        now_high = 0
        while True:
            scroll_high = 200
            height = await page.evaluate('document.body.scrollHeight')
            await page.evaluate('window.scrollBy(%d,%d)' % (0, scroll_high))
            now_high = now_high + scroll_high
            time.sleep(0.5)
            if now_high >= height:
                break
            if len(pageList) * 20 >= num:
                await page.close()
                return pageList

    try:
        return asyncio.get_event_loop().run_until_complete(main(key))
    except Exception as e:
        print(e)
        return pageList


def pddGoodsUrl(jsonList):
    dataList = []
    time = datetime.now()
    try:
        for i in jsonList:
            if i != '':
                n = json.loads(i)
                try:
                    for n in n['items']:
                        item_title = n['goods_name']
                        item_url = 'http://yangkeduo.com/{}'.format(n['link_url'])
                        item_price = float(n['price'] * 0.01)
                        shop_address = ''
                        try:
                            shop_url = 'http://yangkeduo.com/mall_page.html?mall_id={}'.format(n['mall_id'])
                        except:
                            shop_url = ''
                        try:
                            shop_name = n['mall_name']
                        except:
                            shop_name = ''
                        comment_num = -1
                        try:
                            Sales = n['sales']
                        except Exception as e:
                            Sales = ''
                        dataList.append({'time': time, 'item_url': item_url, 'item_title':item_title, 'shop_address': shop_address,
                                         'shop_url': shop_url, 'shop_name': shop_name, 'price': item_price, 'Sales': str(Sales), 'comment_num': comment_num})
                except Exception as e:
                    return e
    except:
        print('检查chrome是否正常工作')
        print('抓取到{}条数据'.format(len(dataList)))
        return dataList
    print('抓取到{}条数据'.format(len(dataList)))
    return dataList


def pddGoodsDetailed(goodDict, ws):
    item_url = goodDict['item_url']

    async def main():
        browser = await connect({
            "browserWSEndpoint": ws
        })
        page = await browser.newPage()
        await page.goto(item_url)
        html = await page.content()
        await page.close()
        return html

    return asyncio.get_event_loop().run_until_complete(main())


def taobaoGoodsField(data):
    pass


def get_pdd(wsUri, project, key_name, key_tag, key_platform, key_place, match):
    # 判断是否是第一次检测还是持续检测
    flag = input('专项:{} 平台：{} 专项关键词：{} 输入?1(第一次检测),2(持续检测)：'.format(project, key_platform, key_name))
    goodsData = []
    try:
        flag = int(flag)
    except:
        return '请正确输入'
    num = 200  # 数据条数
    dates = getLastDate()  # 获取时间
    urlList = set()  # 记录重复数值
    for keys in key_name:
        key_id = keys.split(':')[0]
        key = keys.split(':')[1]
        jsonList = searchPddKey(key, num, wsUri)
        if not jsonList:
            jsonList = searchPddKey(key, num, wsUri)
        if not jsonList:
            jsonList = searchPddKey(key, num, wsUri)
        if not jsonList:
            jsonList = searchPddKey(key, num, wsUri)
        if not jsonList:
            print('请检查chrome浏览器')
        dataList = pddGoodsUrl(jsonList)
        for data in dataList:
            try:
                item_url = data['item_url'].split('&')[0]
            except:
                item_url = data['item_url']
            item_title = data['item_title']
            res = re.search(match, item_title)
            if not res:
                continue
            item_sales = data['Sales']
            item_price = data['price']
            m = hashlib.md5()
            m.update(item_url.encode('utf-8'))
            tag2 = m.hexdigest()
            item_comment = ''
            shop_url = data['shop_url']
            shop_name = data['shop_name']
            shop_address = ''
            if tag2 not in urlList:
                goodsData.append(
                    [project, dates, key_id, key, key_tag, key_platform, key_place, item_url, item_price, item_title,
                     item_sales, item_comment, shop_url, shop_name, shop_address, tag2])
            urlList.add(tag2)

    if flag == 1:
        # 第一次检测入数据表以及留证表
        object_mysql('object', goodsData)
        object_mysql('licence_object', goodsData, 'new')
    elif flag == 2:
        # 持续检测只入数据表
        object_mysql('object', goodsData)
    else:
        return '请输入正确的数字'

# project = ['Z2019072', 'Z2019073']  # 专项号
# key_name = [['6:嘉兴粽子'], ['7:绍兴黄酒']]  # 专项关键词 关键词id：关键词名称
# key_tag = ["浙江嘉兴;粽子", "浙江绍兴;黄酒"]  # 专项标签
# key_platform = [['拼多多'], ['拼多多']]  # 专项检测平台
# key_place = ['嘉兴', '绍兴']  # 检测地区
# for i in range(len(project)):
#     for platform in key_platform[i]:
#         if platform == '拼多多':
#             get_pdd('127.0.0.1:9222',project[i], key_name[i], key_tag[i], platform, key_place[i])

# licence_test.run()