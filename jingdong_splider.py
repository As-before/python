import requests
from urllib import parse
from datetime import datetime
import pymysql
from bs4 import BeautifulSoup
import licence
import hashlib
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


def searchJingdongKey(key, num, sort=''):
    '''
    接受传递过来的参数，查询taobao指定的商品信息
    :param key:搜索关键词
    :param num:搜索条数
    :param sort:搜索排序
    :return: 搜索到的原始html数据列表
    '''
    goodSort = {'价格升序': '2', '价格降序': '1', '销量降序': '3', }
    sortlist = ['2', '1', '3','']
    datas = []
    if sort not in sortlist:
        return '输入错误'
    if num%30 == 0:
        page = num // 30
    else:
        page = (num // 30)+1
    for p in range(1, page+1):
        if sort == '':
            url = "https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}&page={}".format(parse.quote(key),parse.quote(key),p)
        else:
            url = "https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}&psort={}&page={}".format(parse.quote(key),parse.quote(key), sort,p)
        headers = {
            'Host': 'search.jd.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Cookie': 'areaId=2; ipLoc-djd=2-2830-0-0; PCSYCityID=CN_310000_310100_310115; shshshfp=a8ef17a548ada1a6e113f83242779a82; shshshfpa=92c4f543-548a-6665-95c9-162769d0e458-1569831931; shshshfpb=92c4f543-548a-6665-95c9-162769d0e458-1569831931; unpl=V2_ZzNtbUpQSxYmCxUDfhpZBmICFA5LVxZBd1wUAXwdVVJhAhtYclRCFX0URlVnGFgUZwYZXkRcRhJFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZH0ZVARkABttclBzJUUOQVN7GVk1ZjMTbQADHx12CERTeVRaBW8CEV5LZ0Ildg%3d%3d; __jdu=7190228; user-key=c0359716-bdeb-4bff-a88e-9814b2394938; xtest=8115.cf6b6759; __jdc=122270672; rkv=V0100; wlfstk_smdl=fmfig3ovxvsc6cvkhnm7u342bjxqfhiu; TrackID=1tRR0wh43KNEkP6ykmSXttBdihGdKMJLqhv8B1CtjmcY8cCE-T2Fi6h16i-y2KVI5PmJ_u7slkHso0Yzpwpyf_DM3YVcIzQnIBAHz7ZIcVuXZJWNyGuTxCrb4-wMJJeX5; pinId=iM4zB8dU7iHBvEea3rwyY7V9-x-f3wj7; pin=jd_40f2ff2fb337c; unick=%E9%93%B6%E6%B5%B7%E5%B0%8FKiss; ceshi3.com=000; _tp=mQ397xquYbK2Fz9cgxQOza3Kzg09zgLqKHPyALVkq1M%3D; _pst=jd_40f2ff2fb337c; qrsc=3; cn=1; __jda=122270672.7190228.1568019397.1570256867.1570258123.5; __jdv=122270672|baidu|-|organic|not set|1570258122657; 3AB9D23F7A4B3C9B=BJAEHMMKZ6AEQI5EYOFVVNL4F5AS2C4RLI7BS6SXDGRCDV2NA3A5K57ZZEIOFM2DCENXERMTT4QI42ZZ3ZPJ32VDNI; thor=E49B46B06D79D7CE13931D05CBBDF078C4B9C6B76A43DB3430A50DCDA2D1D1EB7B42C03C4DFF3BE296342F3757E70AE8375978996F574ED58180548F3C2A8F31387C78639DFE9D04ECEEEF3677367CBEBC89DF2F0A7330FE8798515411ACF4FEA069FCCFC17336624AEC035C9EACA6BC5C73C07FF1FC663F48C5224C99639B488F9A007B69E87986415CAACB14FF71A2E64229050D0FE43C5194D0C112A67DC0; __jdb=122270672.5.7190228|5.1570258123; shshshsID=7415365a9d5f91958c155a1057c3b282_7_1570258272288',
        }
        try:
            rs = requests.get(url, headers=headers, timeout=5)
            rs.encoding = 'utf-8'
            datas.append(rs.text)
        except Exception as e:
            return e
    return datas


def jingdongGoodsUrl(htmlList):
    '''
    解析html数据列表，生成字典数据
    :param htmlList:html数据列表
    :return: 需要的字段字典
    '''
    time = datetime.now()
    dataList = []
    for eachhtml in htmlList:
        soup=BeautifulSoup(eachhtml,'html.parser')
        items=soup.find_all('li',{'class':'gl-item'})
        for i in items:
            good_price=i.find('div',{'class':'p-price'}).get_text().strip().strip('￥')
            if good_price.find('￥') != -1:
                good_price = good_price.split('￥')[0]
            good_title = i.find('div', {'class': 'p-name p-name-type-2'}).find('a').find('em').text.strip().replace(' ','')
            good_url = i.find('div',{'class':'p-name p-name-type-2'}).find('a').get('href')
            number = re.findall(r"\d+",good_url)[0]
            # 通过商品的id（number）发送请求获取评论数
            url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='+str(number)
            # try:
            #     good_comment = requests.get(url).json()['CommentsCount'][0]['CommentCountStr']
            # except:
            good_comment = ''
            if good_url[0:2] == '//':
                try:
                    p_shop = i.find('div',{'class':'p-shop'}).find('span',{'class':'J_im_icon'})
                    shop_name = p_shop.find('a').get('title')
                    shop_url = p_shop.find('a').get('href')
                except:
                    shop_name = ''
                    shop_url = ''
                dataList.append({'time': time, "item_url": "https:{}".format(good_url), 'item_title': good_title,
                                 "item_price": good_price,'item_comment':good_comment,
                                  'shop_url': "https:{}".format(shop_url), 'shop_name': shop_name})
    print('抓取到{}条数据'.format(len(dataList)))
    return dataList

def get_jd(project, key_name, key_tag, key_platform, key_place, match):
    '''
    主函数，负责协调各函数
    :return:
    '''
    # 判断是否是第一次检测还是持续检测
    flag = input('专项:{} 平台：{} 专项关键词：{} 输入?1(第一次检测),2(持续检测)：'.format(project, key_platform, key_name))
    try:
        flag = int(flag)
    except Exception as e:
        return '请正确输入'
    # 设置专项号等数据
    # 设置专项号等数据
    num = 200  # 数据条数
    urlList = set()  # 记录重复数值
    goodsData = []
    for keys in key_name:
        key_id = keys.split(':')[0]
        key = keys.split(':')[1]
        # 查询搜索商品的所有数据
        dataList = searchJingdongKey(key, num)
        dates = getLastDate()
        lists = jingdongGoodsUrl(dataList)
        for i in lists:
            item_url = i['item_url']
            m = hashlib.md5()
            m.update(item_url.encode('utf-8'))
            tag2 = m.hexdigest()
            item_price = i['item_price']
            item_title = i['item_title']
            res = re.search(match, item_title)
            if not res:
                continue
            item_comment = i['item_comment']
            shop_url = i['shop_url']
            shop_name = i['shop_name']
            if tag2 not in urlList:
                goodsData.append(
                    [project, dates, key_id, key, key_tag, key_platform, key_place, item_url, item_price, item_title,
                     '', item_comment, shop_url, shop_name, '', tag2])
            urlList.add(tag2)
    if flag == 1:
        # 第一次检测入数据表以及留证表
        object_mysql('object', goodsData)
        object_mysql('licence_object', goodsData, 'new')
        # for item in goodsData:
        #     print(item)
    elif flag == 2:
        # 持续检测只入数据表
        object_mysql('object', goodsData)
        # pass
    else:
        return '请输入正确的数字'

# if __name__ == "__main__":
#     project = ['Z2019072', 'Z2019073']  # 专项号
#     key_name = [['6:嘉兴粽子'], ['7:绍兴黄酒']]  # 专项关键词 关键词id：关键词名称
#     key_tag = ["浙江嘉兴;粽子", "浙江绍兴;黄酒"]  # 专项标签
#     key_platform = [['淘宝','京东','拼多多'], ['淘宝','京东']]  # 专项检测平台
#     key_place = ['嘉兴', '绍兴']  # 检测地区
#     for i in range(len(project)):
#         for platform in key_platform[i]:
#             if platform == '京东':
#                 get_jd( project[i], key_name[i], key_tag[i], platform, key_place[i])
#     # 调用检测函数
    # licence.run()
    # 调用查询函数对当日数据进行留证
    # select_mysql()