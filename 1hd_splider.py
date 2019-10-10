import pymysql
import hashlib

def update_msyql(id, tag2):
    db1 = pymysql.connect(host='10.0.6.17', user='did', password='did1505', database='did_new', charset='utf8',
                          port=3306)
    cursor = db1.cursor()
    # 插入语句
    sql = "UPDATE licence_object SET tag2='{}' WHERE id={}".format(tag2, id)
    cursor.execute(sql)
    db1.commit()
    cursor.close()
    db1.close()


def select_goods_mysql():
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
    sql = "select * from licence_object"
    # 查询
    cursor.execute(sql)
    # 获取全部数据
    results = cursor.fetchall()
    for item in results:
        try:
            item_url = item[8].split('&')[0]
        except Exception as e:
            item_url = item[8]
        m = hashlib.md5()
        m.update(item_url.encode('utf-8'))
        tag2 = m.hexdigest()
        update_msyql(item[0], tag2)
select_goods_mysql()