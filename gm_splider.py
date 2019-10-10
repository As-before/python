import requests
from datetime import datetime
import json
import re
import hashlib
#
def getLastDate():
    '''
    获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
    :return: 返回格式化后的时间数据
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def searchGmKey(key, num):
    datas = []
    if num % 48 == 0:
        page = num // 48
    else:
        page = (num // 48) + 1
    headers = {
        "Host": "search.gome.com.cn",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Referer": "https://search.gome.com.cn/search?question=%E8%8B%B9%E6%9E%9C&searchType=goods&search_mode=normal&reWrite=true&instock=1"
    }
    for p in range(1, page+1):
        url = "https://search.gome.com.cn/search?search_mode=normal&question={}&searchType=goods&page={}&type=json".format(key,p)
        try:
            rs = requests.get(url, headers=headers, timeout=5)
            datas.append(rs.text)
        except Exception as e:
            return e
    return datas


def GmGoodsUrl(htmlList):
    '''
    解析html数据列表，生成字典数据
    :param htmlList:html数据列表
    :return: 需要的字段字典
    '''
    time = datetime.now()
    dataList = []
    for eachhtml in htmlList:
        htmlJson = json.loads(eachhtml)
        goods = htmlJson['content']['prodInfo']['products']
        for item in goods:
            try:
                item_comment = item['evaluateCount']
            except:
                item_comment = ''
            try:
                item_name = item['name'].replace(' ','')
            except:
                item_name = ''
            try:
                item_url = 'https:' + item['sUrl']
            except:
                item_url = ''
            try:
                shop_name = item['sName']
            except:
                shop_name = ''
            try:
                shop_url = 'https:' + item['mUrl']
            except:
                shop_url = ''
            try:
                skuId = item['skuId']
                pId = item['pId']
                price_url = "https://ss.gome.com.cn/search/v1/price/single/{}/{}/11010000/flag/item/fn1570701205124?callback=fn1570701205124".format(pId, skuId)
                prices = requests.get(price_url)
                com = re.compile('fn.*?\((.*?)\)', re.S)
                ds = re.findall(com, prices.text)
                item_price = json.loads(ds[0])['result']['price']
            except Exception as e:
                print(e)
                continue
            dataList.append({'time': time, "item_url": item_url, 'item_title': item_name,
                             "item_price": item_price,
                             'shop_address': '', 'shop_url': shop_url, 'shop_name': shop_name,
                             'Sales': '', 'comment_num': item_comment})
    print('抓取到{}条数据'.format(len(dataList)))
    return dataList


def get_gm(project, key_name, key_tag, key_platform, key_place, match):
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
        dataList = searchGmKey(key, num)
        dates = getLastDate()  # 获取时间
        goodsList = GmGoodsUrl(dataList)  # 获取所有商品数据
        for i in goodsList:
            try:
                item_url = i['item_url'].split('&')[0]
            except Exception as e:
                item_url = i['item_url']
            item_price = i['item_price']
            item_title = i['item_title'].replace("<labelstyle='color:red;'>",'').replace('</label>','')
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
        for i in goodsData:
            print(i)
    else:
        return '请输入正确的数字'

if __name__ == "__main__":
    project = ['Z2019072', 'Z2019073']  # 专项号
    key_name = [['6:嘉兴粽子'], ['7:绍兴黄酒']]  # 专项关键词 关键词id：关键词名称
    key_tag = ["浙江嘉兴;粽子", "浙江绍兴;黄酒"]  # 专项标签
    # key_platform = [['淘宝', '京东', '拼多多'], ['淘宝', '京东']]  # 专项检测平台
    key_platform = [['国美'], []]  # 专项检测平台
    key_place = ['嘉兴', '绍兴']  # 检测地区
    search = ['.*粽.*嘉兴|.*嘉兴.*粽','.*酒.*绍兴|.*绍兴.*酒']
    for i in range(len(project)):
        for platform in key_platform[i]:
            if platform == '国美':
                # print(platform)
                get_gm(project[i], key_name[i], key_tag[i], platform, key_place[i], search[i])
    # 调用检测函数
    # licence.run()
    # 调用查询函数对当日数据进行留证
    # select_mysql()
