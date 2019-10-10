import pymysql
from datetime import datetime, date, timedelta


def getLastDate():
    '''
    获取时间函数，把当前时间格式化为str类型nowdate.strftime('%Y-%m-%d %H:%M:%S')
    :return: 返回格式化后的时间数据
    '''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def select_mysql(date):
    """
    查询object库中所有数据
    :return: 返回查询到的数据
    """
    items = []
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    # 创建游标
    cursor = db1.cursor()
    # sql语句
    sql = "select * from object_test1 where dates like '{}%'".format(date)
    # 查询
    cursor.execute(sql)
    # 获取全部数据
    results = cursor.fetchall()
    for item in results:
        # 对每条数据执行操作代码
        items.append(item)
    return items


def select_goods_mysql(url_md5):
    """
    查询object库中所有数据
    :return: 返回查询到的数据
    """
    items = []
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    # 创建游标
    cursor = db1.cursor()
    # sql语句
    sql = "select * from object_test1 where tag2='{}' order by id".format(url_md5)
    # 查询
    cursor.execute(sql)
    # 获取全部数据
    results = cursor.fetchall()
    for item in results:
        # 对每条数据执行操作代码
        items.append(item)
    return items


def judge():
    """
    根据当前日期，取得昨天日期，生成列表
    :return: 当天数据列表，昨天数据列表
    """
    today = datetime.now().strftime('%Y-%m-%d')  # 当前日期
    yesterday = str(date.today() + timedelta(days=-1))  # 昨天日期
    # 查询数据
    todayList = select_mysql(today)
    yesterdayList = select_mysql(yesterday)
    # 判断今天和昨天的数据，并添加的相应的列表
    return todayList


def monitor(todayList):
    """
    获取当天和昨天的数据，统计新添加的数据，以及价格浮动的数据，以及价格低于80%的数据
    :return: 新加数据列表，价格浮动数据列表，低价数据列表
    """
    newList = []
    changesList = []
    for item in todayList:
        goodsData = select_goods_mysql(item[-4])
        if len(goodsData) == 1:
            newList.append(item)
        elif len(goodsData) >= 2:
            todayGoods = goodsData[-1]
            yesterdayGoods = goodsData[-2]
            t_price = float(todayGoods[9])
            y_price = float(yesterdayGoods[9])
            # 对今天和昨天的价格进行比较，如果价格出现异动，就放入异动列表
            if t_price < y_price:
                changesList.append(item)
            elif t_price > y_price:
                changesList.append(item)
    return newList, changesList


def licence_mysql(table, items, type):
    """
    插入传入的数据到数据库
    :param table: 表名称
    :param items: 数据列表
    :param type: 标签
    :return:
    """
    # 构建表中需要用到的字段
    project = items[1]
    dates = getLastDate()
    key_id = items[3]
    key_name = items[4]
    key_tag = items[5]
    key_platform = items[6]
    key_place = items[7]
    item_url = items[8]
    item_price = items[9]
    item_title = items[10]
    item_sales = items[11]
    item_comment = items[12]
    shop_url = items[13]
    shop_name = items[14]
    shop_address = items[15]
    tag2 = items[17]
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    cursor = db1.cursor()
    # 插入语句
    sql = 'insert into %s(project,dates,key_id,key_name,key_tag,' \
          'key_platform,key_place,item_url,item_price,item_title,item_sales,item_' \
          'comment,shop_url,shop_name,shop_address,tag1,tag2) values("%s", ' \
          '"%s","%s","%s","%s","%s","%s","%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
              table, project, dates, key_id, key_name, key_tag, key_platform, key_place, item_url, item_price,
              item_title,
              item_sales, item_comment, shop_url, shop_name, shop_address, type, tag2)
    cursor.execute(sql)
    db1.commit()
    cursor.close()
    db1.close()


def putLibrary(table, newList, changesList):
    '''
    获取新加数据表，低价表，价格异动表，调用licence_mysql保存到数据库
    :param newList: 新加表
    :param changesList:价格异动表
    :return:
    '''
    # 循环各个表数据，将有数据的列表数据插入到数据库
    if newList:
        for n_item in newList:
            licence_mysql(table, n_item, 'new')
    if changesList:
        for e_item in changesList:
            licence_mysql(table, e_item, 'changes')

def run():
    '''
    运行函数
    :return:
    '''
    todayList = judge()
    print('今天入库数据共:%s条'%(len(todayList)))
    # 检测新增数据，异动数据， 低价数据
    newList, changesList = monitor(todayList)
    print('查询到新增数据:%s条; 异动数据:%s条'%(len(newList), len(changesList)))
    # 将数据入库
    putLibrary('object_test2', newList, changesList)
