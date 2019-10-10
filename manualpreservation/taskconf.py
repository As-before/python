# -*- coding:utf-8 -*-
import re
import json
import os

config = {
    # "chrome_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", #默认情况下无需指定该参数
    "width": 1920,
    "height": 1024,
    "charset": "utf8",
    "request_timeout": 20000,
    "request_interval_timeout": 200,
    "timeout": 600000,
    "cookies": [],
    "headers": None,
    "inject_js": None,
    "inject_css": None,
    "url_filters": [],
    "exts": [],
    "screenshot_thumbnail_filename": "snapshot",
    "screenshot_thumbnail_format": "png",
    "screenshot_sliced": True,
    "screenshot_scale": 5000.0 / 1680,  # 可调切片大小比例，等于 高度/宽度,默认 ：29.7 / 21 / 4
    "full_page":True,
    "output_path": "tmp",  # 确保每个worker上面都存在该目录
    "pre_run": False,
    "wait_before_screenshot": 1000,
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36",
    "js_enable": True,
    "headless": False,
    "wait_before_run": 5000,  # 单位ms,运行前等待时间用于绕过验证
    "scroll_element":"html", #默认滚动元素是html，等价于document.documentElement
    # "assist_id"
    'clickList': ['#sufei-dialog-close'],
    'updateList': ['body > div.tb-doctor > div', 'body > div.sufei-dialog.sufei-dialog-kissy'],
}

config_desc = {
    "width": "页面宽度",
    "height": "页面高度",
    "charset": "编码",
    "request_timeout": "页面请求总超时",
    "request_interval_timeout": "滚动|请求的间隔",
    "timeout": "任务超时",
    "cookies": "Cookies",
    "headers": "请求头",
    "inject_js": "注入JS",
    "inject_css": "注入样式",
    "url_filters": "网址过滤",
    "exts": "扩展名白名单",
    "screenshot_thumbnail_filename": "截图文件名",
    "screenshot_thumbnail_format": "截图后缀",
    "screenshot_sliced": "是否切片",
    "screenshot_scale": "切片宽高比",  # 可调切片大小比例，等于 高度/宽度,默认 ：29.7 / 21 / 4
    "output_path": "结果输出路径",  # 确保每个worker上面都存在该目录
    "pre_run": "预运行",
    "wait_before_screenshot": "截图前等待",
    "user_agent": "UA",
    "js_enable": "JS启用",
    "headless": "无头模式",
    "wait_before_run": "运行前等待",  # 单位ms,运行前等待时间用于绕过验证
    "scroll_element": "滚动元素",  # 默认滚动元素是html，等价于document.documentElement
    "full_view": "是否全屏显示",
    "page_down":"是否翻页",
    "mobile_emulate":"是否模拟手机",
    "output_folder":"输出文件的目录名", #默认为空时，以时间戳代替
    "index_page_filename":"首页的文件名",
    "full_page":"是否生成完整截图文件",
    "chrome_ws":"Chrome-WS入口"

}


def reconfig(myconfig):

    for k,v in myconfig.iteritems():
        quest = k if not config_desc.has_key(k) else config_desc[k]
        if type(v) in (dict,list,set,tuple):
            default_value = json.dumps(v)
        else:
            default_value = str(v)
        answer = input("{},参考默认值:{}[回车跳过]?".format(quest,default_value))
        if answer != '':
            try:
                if (answer.strip().lower()) == 'none':
                    answer = None
                elif (answer.strip().lower()) == 'false':
                    answer = False
                elif (answer.strip().lower()) == 'true':
                    answer = True
                myconfig[k] = eval(answer.strip())
            except Exception as e:
                myconfig[k] = answer if type(answer) != str else answer.strip()

    return myconfig

def patch_conf(url):
    rules=[]


class ConfPatch:

    def __init__(self,conf_path):
        self.rules = []
        for root,dirs,files in os.walk("site_conf"):
            for conf in files:
                try:
                    self.rules.append(json.load(open(os.path.join(root,conf), 'r')))
                except Exception as e:
                    raise e

    def patch_conf(self,url,conf):
        for rule in self.rules:
            if re.search(rule['url'],url):
                for k,v in rule['config'].items():
                    conf[k]=v
                return conf
        return conf

    def has_patch(self,url):
        for rule in self.rules:
            if re.search(rule['url'],url):
                return True
        return False