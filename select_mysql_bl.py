import pymysql
import os
from datetime import datetime
from manualpreservation.inspection import run
import requests

def getWs(chrome_url):
    ws = requests.get(url='http://' + chrome_url + "/json/version").json()["webSocketDebuggerUrl"]
    return ws

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
    sql = "select * from licence_object where dates like '{}%'".format(today)
    # 查询
    cursor.execute(sql)
    # 获取全部数据
    results = cursor.fetchall()
    for item in results:
        type = item[-5]
        zx = item[1]
        paths = '/Volumes/did/2019/{}/02-采集-留证/原始留证/inspection/{}/{}'.format(zx, type, today)
        if not os.path.exists(paths):
            os.makedirs(paths)
        id = item[0]
        url = item[8]
        flag = item[6]
        if flag=="拼多多":
            #run(getWs('127.0.0.1:9222'), zx, paths, id, url, flag)
            pass
        else:
            # print(zx, paths, id, url, flag)
            if id == 5478:
                run(getWs('127.0.0.1:9222'), zx, paths, id, url, flag)

select_mysql()