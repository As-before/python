# -*- coding:utf-8 -*-

__author__ = 'xhp'

from manualpreservation.scrapyTask import scrapyNormal, logger
from manualpreservation.taskconf import config, ConfPatch
import requests
import json

def run(ws, id, url, name):
    def getWs(chrome_url):
        ws = requests.get(url='http://' + chrome_url + "/json/version").json()["webSocketDebuggerUrl"]
        return ws
    chrome_ws = getWs(ws)
    config['chrome_ws'] = chrome_ws.strip()
    app_exit = False
    task_log = open('task.log', 'a')
    myconfig = config.copy()
    logger.info('载入配置补丁')
    try:
        cnf_patch = ConfPatch('./site_conf')
    except Exception as e:
        logger.info(e)
        logger.info('补丁载入失败')
        cnf_patch = False
    zhuanxiang_num = '留证专项'
    try:
        task_status = 'ok'
        current_record = {'url': url, 'name': name, 'id': id}
        try:
            if not url.startswith('http://') and not url.startswith("https://"):
                url = 'http://{}'.format(url)
            task_conf = myconfig.copy()
            task_conf["output_folder"] = zhuanxiang_num + '-' + str(current_record["id"]) + '-' + str(
                current_record["name"])
            logger.info("编号:{},网址：{}".format(current_record['id'], current_record['url']))
            if cnf_patch:
                task_conf = cnf_patch.patch_conf(current_record['url'], task_conf)
            task = scrapyNormal(current_record['url'], task_conf)
            current_record["result"] = task
            task_log.write(json.dumps(current_record) + '\n')
            task_log.flush()
        except Exception as e:
            logger.info(e)
            task_status = 'failed'
    except StopIteration as e:
        logger.info("记录处理完毕")
    task_log.close()

# run('127.0.0.1:44179','1','https://product.suning.com/0000000000/11346304303.html','甜蜜')