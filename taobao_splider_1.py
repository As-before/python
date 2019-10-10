import requests
import json
import re
from urllib import parse
from datetime import datetime
import pymysql
import licence
from manualpreservation.inspection import run
import os
import time

def getLastDate():
    '''
    获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
    :return: 返回格式化后的时间数据
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def object_mysql(table, project, dates, key_id, key_name, key_tag, key_platform, key_place, item_url, item_price,
                 item_title, item_sales, item_comment, shop_url, shop_name, shop_address):
    '''
    传入相应的数据，插入到指定的数据库
    :param table: 表名称
    :return:
    '''
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    cursor = db1.cursor()
    sql = 'insert into %s(project,dates,key_id,key_name,key_tag,' \
          'key_platform,key_place,item_url,item_price,item_title,item_sales,item_' \
          'comment,shop_url,shop_name,shop_address) values("%s", ' \
          '"%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s")' % (
              table, project, dates, key_id, key_name, key_tag, key_platform, key_place, item_url, item_price,
              item_title,
              item_sales, item_comment, shop_url, shop_name, shop_address)
    cursor.execute(sql)
    db1.commit()
    cursor.close()
    db1.close()


def licence_mysql(table, project, dates, key_id, key_name, key_tag, key_platform, key_place, item_url, item_price,
                  item_title, item_sales, item_comment, shop_url, shop_name, shop_address, tag1):
    '''
    传入相应的数据，插入到指定的数据库
    :param table:表名称
    :return:
    '''
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    cursor = db1.cursor()
    sql = 'insert into %s(project,dates,key_id,key_name,key_tag,' \
          'key_platform,key_place,item_url,item_price,item_title,item_sales,item_' \
          'comment,shop_url,shop_name,shop_address,tag1) values("%s", ' \
          '"%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s")' % (
              table, project, dates, key_id, key_name, key_tag, key_platform, key_place, item_url, item_price,
              item_title,
              item_sales, item_comment, shop_url, shop_name, shop_address, tag1)
    cursor.execute(sql)
    db1.commit()
    cursor.close()
    db1.close()


def searchTaobaoKey(key, num, sort=''):
    '''
    接受传递过来的参数，查询taobao指定的商品信息
    :param key:搜索关键词
    :param num:搜索条数
    :param sort:搜索排序
    :return: 搜索到的原始html数据列表
    '''
    goodSort = {'价格从低到高': 'price-asc', '价格从高到低': 'price-desc', '总价从低到高': 'total-asc', '总价从高到低': 'price-desc',
                '销量从高到低': 'sale-desc', }
    sortlist = ['price-asc', 'price-desc', 'total-asc', 'price-desc', 'sale-desc', '']
    if sort not in sortlist:
        return '输入错误'
    if num % 44 == 0:
        s = num
    else:
        s = 44 * (num // 44)
    datas = []
    for n in range(0, s + 1, 44):
        if sort == '':
            url = "https://s.taobao.com/search?q={}&s={}".format(parse.quote(key), n)
        else:
            url = "https://s.taobao.com/search?q={}&s={}&sort={}".format(parse.quote(key), n, sort)
        headers = {
            'Host': 's.taobao.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Cookie': 'pnm_cku822=098%23E1hvEvvUvbpvUpCkvvvvvjiPRFLyljlPRFLUljrCPmPU1jE2RsSy1jEjP2Lp1jYRR8wCvvpvvUmmvphvC9v9vvCvpvyCvhQW%2B3yvClswaNoidfUf8zxl%2BE7rVC693Exrz8g78BoxfwCl5t3QpKLOTWowV53Z0f0DyBvOJ1kHsX7veCrTmEcBlwyzhmx%2Ftjc6D464uphvmvvv9bOnVNuFkphvC9QvvpH0LqyCvm9vvvmnphvv2pvv9ttvpvpIvvm2phCvhRvvvURJphvpavvv9ttvpCvh2QhvCPMMvvvtvpvhvvvvvv%3D%3D; cna=+HHzFUEQ0zUCAd2F84RoQAdQ; isg=BOTkUBYGZdMl4ZH3LQ1Bcjzltuvcd72SUQwcDv4FdK9yqYRzJo2TdxgLacEUakA_; l=cBxofPIeqHQ0FrQzKOCNiZ_XJF79SIOYYuWfhbhvi_5Zl6LsDmQOk_pMRFp6csWd93LB43PGn4J9-eteqUy06P1P97RN.; cq=ccp%3D0; OZ_1U_2061=vid=vd706f1f3ffae9.0&ctime=1567651058&ltime=1567651006; hng=CN%7Czh-CN%7CCNY%7C156; lid=tb928237077; enc=gpUMnLtDUI8OXaIKWglYl6UkyC5F3S6Et58PCK61g8AjDL9aDCPS6sjy9PG9O1S2ZL2In%2B4uCBkcRsbzJT%2B%2B7g%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=80d708513c1585384cfe8c70adcab65b; uc4=nk4=0%40U2%2F1BHORTA7DcDbBCJlCPZqbe3mDnEY%3D&id4=0%40U2xt%2BjCc43W6R9x5y38jYfmoyAne; _tb_token_=393b385fb43f3; cookie2=185c77079ef16ccf6ee85770866823d5; dnk=tb928237077; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9aj3yE&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTaEC%2BThAB8Gg%3D%3D&tag=8&lng=zh_CN; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuK3QZdU8MTCxBQ%3D&nk2=F5RMGyu%2Bv4RTkQg%3D&id2=UUphzOfZfIgbMqzt5g%3D%3D; tracknick=tb928237077; _l_g_=Ug%3D%3D; unb=2206577557789; lgc=tb928237077; cookie1=W50Of5XbimjJg19Zbx%2FesTLZciqOUwdUNvbzLdkzDpk%3D; login=true; cookie17=UUphzOfZfIgbMqzt5g%3D%3D; _nk_=tb928237077; sg=79b; csg=7a8d34d5; _m_h5_tk=ebc87bbc290e65c0f708117337e06801_1568963458160; _m_h5_tk_enc=f1802e63f9a22b215ab5ef4c634eff53; swfstore=125837; whl=-1%260%260%260',
        }
        try:
            rs = requests.get(url, headers=headers)
            datas.append(rs.text)
        except Exception as e:
            return e
    return datas


def taobaoGoodsUrl(htmlList):
    '''
    解析html数据列表，生成字典数据
    :param htmlList:html数据列表
    :return: 需要的字段字典
    '''
    time = datetime.now()
    dataList = []
    for html in htmlList:
        try:
            items = json.loads('{%s}' % re.findall('g_page_config = {(.*?)};', html)[0])['mods']['itemlist']['data'][
                'auctions']
        except Exception as e:
            break
        for i in items:
            try:
                item_url = i['detail_url']
            except:
                item_url = ''
            try:
                item_price = float(i['view_price'])
            except:
                item_price = 0.00
            try:
                item_title = i['raw_title']
            except:
                item_title = ''
            try:
                shop_address = i['item_loc']
            except:
                shop_address = ''
            try:
                shop_url = 'https:' + i['shopLink']
            except:
                shop_url = ''
            try:
                shop_name = i['nick']
            except:
                shop_name = ''
            try:
                Sales = i['view_sales']
            except:
                Sales = ''
            comment_num = -1
            try:
                Sales = Sales[0:-3]
            except Exception as e:
                Sales = ''
            if item_url[0:2] == '//':
                dataList.append({'time': time, "item_url": "https:{}".format(item_url), 'item_title': item_title,
                                 "item_price": item_price,
                                 'shop_address': shop_address, 'shop_url': shop_url, 'shop_name': shop_name,
                                 'Sales': Sales, 'comment_num': comment_num})
    return dataList


def taobaoGoodsDetailed(goodDict):
    '''
    获取商品详情页的html数据
    :param goodDict:
    :return:
    '''
    time.sleep(1)
    item_url = goodDict['item_url']
    headers = {
        'Host': 'detail.tmall.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Referer': 'https://s.taobao.com/search?spm=a21bo.2017.201867-links-1.7.5af911d95MnFSX&q=%E5%8D%95%E9%9E%8B+%E5%A5%B3%E9%9E%8B+ifashion&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190202&ie=utf8',
        'Cookie': 'pnm_cku822=098%23E1hvEvvUvbpvUpCkvvvvvjiPRFLyljlPRFLUljrCPmPU1jE2RsSy1jEjP2Lp1jYRR8wCvvpvvUmmvphvC9v9vvCvpvyCvhQW%2B3yvClswaNoidfUf8zxl%2BE7rVC693Exrz8g78BoxfwCl5t3QpKLOTWowV53Z0f0DyBvOJ1kHsX7veCrTmEcBlwyzhmx%2Ftjc6D464uphvmvvv9bOnVNuFkphvC9QvvpH0LqyCvm9vvvmnphvv2pvv9ttvpvpIvvm2phCvhRvvvURJphvpavvv9ttvpCvh2QhvCPMMvvvtvpvhvvvvvv%3D%3D; cna=+HHzFUEQ0zUCAd2F84RoQAdQ; isg=BOTkUBYGZdMl4ZH3LQ1Bcjzltuvcd72SUQwcDv4FdK9yqYRzJo2TdxgLacEUakA_; l=cBxofPIeqHQ0FrQzKOCNiZ_XJF79SIOYYuWfhbhvi_5Zl6LsDmQOk_pMRFp6csWd93LB43PGn4J9-eteqUy06P1P97RN.; cq=ccp%3D0; OZ_1U_2061=vid=vd706f1f3ffae9.0&ctime=1567651058&ltime=1567651006; hng=CN%7Czh-CN%7CCNY%7C156; lid=tb928237077; enc=gpUMnLtDUI8OXaIKWglYl6UkyC5F3S6Et58PCK61g8AjDL9aDCPS6sjy9PG9O1S2ZL2In%2B4uCBkcRsbzJT%2B%2B7g%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=80d708513c1585384cfe8c70adcab65b; uc4=nk4=0%40U2%2F1BHORTA7DcDbBCJlCPZqbe3mDnEY%3D&id4=0%40U2xt%2BjCc43W6R9x5y38jYfmoyAne; _tb_token_=393b385fb43f3; cookie2=185c77079ef16ccf6ee85770866823d5; dnk=tb928237077; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9aj3yE&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTaEC%2BThAB8Gg%3D%3D&tag=8&lng=zh_CN; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuK3QZdU8MTCxBQ%3D&nk2=F5RMGyu%2Bv4RTkQg%3D&id2=UUphzOfZfIgbMqzt5g%3D%3D; tracknick=tb928237077; _l_g_=Ug%3D%3D; unb=2206577557789; lgc=tb928237077; cookie1=W50Of5XbimjJg19Zbx%2FesTLZciqOUwdUNvbzLdkzDpk%3D; login=true; cookie17=UUphzOfZfIgbMqzt5g%3D%3D; _nk_=tb928237077; sg=79b; csg=7a8d34d5; _m_h5_tk=ebc87bbc290e65c0f708117337e06801_1568963458160; _m_h5_tk_enc=f1802e63f9a22b215ab5ef4c634eff53; swfstore=125837; whl=-1%260%260%260',
    }
    rp = requests.get(item_url, headers=headers)
    return rp.text


def searchTaobaoPageCount(key, num, sort=''):
    '''
    获取搜索商品的总页数
    :param key: 搜索关键词
    :param num:搜索条数
    :param sort:搜索排序
    :return: 当前总页数
    '''
    if sort == '':
        url = "https://s.taobao.com/search?q={}".format(parse.quote(key))
    else:
        url = "https://s.taobao.com/search?q={}&sort={}".format(parse.quote(key), sort)
    headers = {
        'Host': 's.taobao.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Cookie': 'pnm_cku822=098%23E1hvEvvUvbpvUpCkvvvvvjiPRFLyljlPRFLUljrCPmPU1jE2RsSy1jEjP2Lp1jYRR8wCvvpvvUmmvphvC9v9vvCvpvyCvhQW%2B3yvClswaNoidfUf8zxl%2BE7rVC693Exrz8g78BoxfwCl5t3QpKLOTWowV53Z0f0DyBvOJ1kHsX7veCrTmEcBlwyzhmx%2Ftjc6D464uphvmvvv9bOnVNuFkphvC9QvvpH0LqyCvm9vvvmnphvv2pvv9ttvpvpIvvm2phCvhRvvvURJphvpavvv9ttvpCvh2QhvCPMMvvvtvpvhvvvvvv%3D%3D; cna=+HHzFUEQ0zUCAd2F84RoQAdQ; isg=BOTkUBYGZdMl4ZH3LQ1Bcjzltuvcd72SUQwcDv4FdK9yqYRzJo2TdxgLacEUakA_; l=cBxofPIeqHQ0FrQzKOCNiZ_XJF79SIOYYuWfhbhvi_5Zl6LsDmQOk_pMRFp6csWd93LB43PGn4J9-eteqUy06P1P97RN.; cq=ccp%3D0; OZ_1U_2061=vid=vd706f1f3ffae9.0&ctime=1567651058&ltime=1567651006; hng=CN%7Czh-CN%7CCNY%7C156; lid=tb928237077; enc=gpUMnLtDUI8OXaIKWglYl6UkyC5F3S6Et58PCK61g8AjDL9aDCPS6sjy9PG9O1S2ZL2In%2B4uCBkcRsbzJT%2B%2B7g%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; t=80d708513c1585384cfe8c70adcab65b; uc4=nk4=0%40U2%2F1BHORTA7DcDbBCJlCPZqbe3mDnEY%3D&id4=0%40U2xt%2BjCc43W6R9x5y38jYfmoyAne; _tb_token_=393b385fb43f3; cookie2=185c77079ef16ccf6ee85770866823d5; dnk=tb928237077; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9aj3yE&cookie15=URm48syIIVrSKA%3D%3D&existShop=false&pas=0&cookie14=UoTaEC%2BThAB8Gg%3D%3D&tag=8&lng=zh_CN; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dByuK3QZdU8MTCxBQ%3D&nk2=F5RMGyu%2Bv4RTkQg%3D&id2=UUphzOfZfIgbMqzt5g%3D%3D; tracknick=tb928237077; _l_g_=Ug%3D%3D; unb=2206577557789; lgc=tb928237077; cookie1=W50Of5XbimjJg19Zbx%2FesTLZciqOUwdUNvbzLdkzDpk%3D; login=true; cookie17=UUphzOfZfIgbMqzt5g%3D%3D; _nk_=tb928237077; sg=79b; csg=7a8d34d5; _m_h5_tk=ebc87bbc290e65c0f708117337e06801_1568963458160; _m_h5_tk_enc=f1802e63f9a22b215ab5ef4c634eff53; swfstore=125837; whl=-1%260%260%260',
    }
    try:
        rs = requests.get(url, headers=headers)
        html = rs.text
        items = json.loads('{%s}' % re.findall('g_page_config = {(.*?)};', html)[0])
        return items['mods']['pager']['data']['totalPage']
    except Exception as e:
        return e


def taobaoGoodsField(data):
    '''
    解析商品详情页
    :param data: 商品详情页html数据
    :return:
    '''
    print(data)
    cp = re.compile('<div class="tb-wrap">(.*?)<div class="tb-key">', re.S)
    print(re.findall(cp, data))
    # lm = etree.HTML(data)
    # xp = lm.xpath('//*[@class="tb-wrap"]')[0]
    # title = xp.xpath('div[@class="tb-detail-hd"]/h1/text()')
    # for i in xp.xpath('ul[@class="tm-ind-panel"]/li'):
    #     print(i.xpath('//span/text()'))
    # print(xp.xpath('//span[@class="tm-count"]/text()'))


def get():
    '''
    主函数，负责协调各函数
    :return:
    '''
    # 判断是否是第一次检测还是持续检测
    flag = input('输入?1(第一次检测),2(持续检测)：')
    try:
        flag = int(flag)
    except Exception as e:
        return '请正确输入'
    # 设置专项号等数据
    project = 'Z2019072'  # 专项号
    key_id = '6'  # 专项ID
    key_name = ['嘉兴粽子']  # 专项关键词
    key_tag = "浙江嘉兴;粽子"  # 专项标签
    key_platform = '淘宝'  # 专项检测平台
    key_place = '嘉兴'  # 检测地区
    for key in key_name:
        # 查询搜索商品的所有数据
        dataList = searchTaobaoKey(key, 220)
        dates = getLastDate()
        for i in taobaoGoodsUrl(dataList):
            item_url = i['item_url']
            item_price = i['item_price']
            item_title = i['item_title']
            item_sales = i['Sales']
            item_comment = i['comment_num']
            shop_url = i['shop_url']
            shop_name = i['shop_name']
            shop_address = i['shop_address']
            if flag == 1:
                # 第一次检测入数据表以及留证表
                object_mysql('object', project, dates, key_id, key, key_tag, key_platform, key_place, item_url,
                             item_price,
                             item_title, item_sales, item_comment, shop_url, shop_name, shop_address)
                licence_mysql('licence_object', project, dates, key_id, key, key_tag, key_platform, key_place,
                              item_url,
                              item_price,
                              item_title, item_sales, item_comment, shop_url, shop_name, shop_address, 'new')

            elif flag == 2:
                # 持续检测只入数据表
                object_mysql('object', project, dates, key_id, key, key_tag, key_platform, key_place, item_url,
                             item_price,
                             item_title, item_sales, item_comment, shop_url, shop_name, shop_address)
            else:
                return '请输入正确的数字'


def select_mysql():
    """
    查询object库中所有数据
    :return: 返回查询到的数据
    """
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    today = datetime.now().strftime('%Y-%m-%d')  # 当前日期
    # 创建游标
    cursor = db1.cursor()
    # sql语句
    sql = 'SELECT t.* FROM did_new.licence_object t'
    # 查询
    cursor.execute(sql)
    # 获取全部数据
    results = cursor.fetchall()
    for item in results:
        if item[2].split(' ')[0] == today:
            type = item[-5]
            zx = item[1]
            paths = '{}/data/tmp/{}/{}/{}'.format(os.getcwd(), zx, type, today)
            if not os.path.exists(paths):
                os.makedirs(paths)
            id = item[0]
            url = item[8]
            flag = '天猫'
            run(zx,paths,id,url,flag)


if __name__ == "__main__":
    # 运行主函数
    get()
    # 调用检测函数
    # licence.run()
    # 调用查询函数对当日数据进行留证
    # select_mysql()