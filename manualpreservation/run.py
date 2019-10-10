# -*- coding:utf-8 -*- 

__author__ = 'xhp'

from scrapyTask import scrapyNormal
import time, sys


config = {
    #  "chrome_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "width": 1280,
    "height": 1024,
    "charset": "utf8",
    "request_timeout": 300,
    "request_interval_timeout": 1000,
    "timeout": 60000,
    "cookies": None,
    "headers": None,
    "inject_js": None,
    "inject_css": None,
    "url_filters": [],
    "exts": [],
    "screenshot_thumbnail_filename": "snapshot",
    "screenshot_thumbnail_format": "png",
    # "output_path": "/mnt/data",
    "output_path": "/tmp",
    "pre_run": False,
    "wait_before_screenshot": 5000,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "js_enable": True,

}

begintime = time.time()

url = input('url?')

task = scrapyNormal.apply_async(args=[url, config], queue='snapshot', routing_key='websnap')  # 向worker发送异步任务
print(task)
while not task.ready():  # 轮询任务是否完成
    # print 'result not ready'
    print("task status:{0}".format(task.status))
    time.sleep(1)
result = task.get()  # 任务完成后，取回任务结果
print('folder name:%s' % result['result']['jobid'])
endtime = time.time()
print('任务耗时：%s秒' % (endtime - begintime))
