# -*- coding:utf-8 -*-

__author__ = 'xhp'

from scrapyTask import scrapyNormal,logger
import time
import os
import json
from taskconf import config,config_desc,ConfPatch,reconfig,patch_conf
import csv

def reloadWS():
    if os.path.exists('chrome.ws'):
        chrome_ws = open('chrome.ws', 'r').readline().strip()
    else:
        chrome_ws = input('which chrome ws?:')
    return chrome_ws


def run(ws, zhuanxiang_num, result_dir, id, url,name):
    chrome_ws = ws
    if len(chrome_ws.strip()) > 0:
        config['chrome_ws'] = chrome_ws.strip()
        app_exit= False
        task_log = open('task.log','a')
        # answer = input("是否修改配置？默认N")
        myconfig = config.copy()
        myconfig['output_path'] = result_dir
        # if answer.strip().lower() == 'y':
        #     myconfig = reconfig(myconfig)
        logger.info('载入配置补丁')
        try:
            cnf_patch = ConfPatch('./site_conf')
        except Exception as e:
            logger.info(e)
            logger.info('补丁载入失败')
            cnf_patch = False
        zhuanxiang_num = zhuanxiang_num
        try:
            current_record_number = 0
            task_status = 'ok'
            current_record = {'id':id,'url':url,'name':name}
            try:
                url = current_record['url']
                if not url.startswith('http://') and not url.startswith("https://"):
                    url = 'http://{}'.format(url)
                current_record['url'] = url
                task_conf = myconfig.copy()
                task_conf["output_folder"] =zhuanxiang_num +'-'+str(current_record["id"]) +'-'+str(current_record["name"])
                logger.info("第{}条记录，网址：{}".format(current_record_number,current_record['url']))
                if cnf_patch:
                    task_conf = cnf_patch.patch_conf(current_record['url'],task_conf)
                task = scrapyNormal(current_record['url'], task_conf)
                current_record["result"] = task
                task_log.write(json.dumps(current_record)+'\n')
                task_log.flush()
            except Exception as e:
                logger.info(e)
                task_status='failed'
        except StopIteration as e:
            logger.info("记录处理完毕")

        task_log.close()
    else:
        print('chrome都没启动，你在玩毛线啊！')