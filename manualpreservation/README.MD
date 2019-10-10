#OWL2的人工协助留证工具说明

## 基本运行环境

在ubuntu、mac都测试过了，windows下面未测试，可能存在一些问题

## 架设服务器

### 基本服务器

#### ubuntu server 18.04/rabbitmq/postgresql

安装rabbitmq

```bash
echo "deb https://dl.bintray.com/rabbitmq/debian artful main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo locale-gen zh_CN.UTF-8
sudo su
rabbitmqctl add_vhost splab
rabbitmqctl add_user splab splab
rabbitmqctl set_user_tags splab administrator
rabbitmqctl set_permissions -p splab '.*' '.*' '.*'
rabbitmq-plugins enable rabbitmq_management
```
安装supervisor及pip

```bash
apt-get install supervisor
apt-get install python-pip

pip install --upgrade pip
mkdir ~/.pip
vim ~/.pip/pip.conf
```

pip.conf文件内容

```bash
[global]
index-url = https://pypi.mirrors.ustc.edu.cn/simple/
```

如果pip升级后出错，处理：

```
sudo ln -s /usr/local/bin/pip /usr/bin/pip
```

安装celery

```
pip install celery flower --user

```

设置celery自启动

```bash
sudo vi /etc/superviso/conf.d/flow.conf
```

flow.conf内容：

```bash
[program:flow]
command=python -m celery flower --broker=amqp://splab:spb@127.0.0.1:5672/splab
directory=/home/userroot/celery
user=userroot
autostart=true
autorestart=true
#log文件的位置
stdout_logfile=/home/userroot/celery/flower.log
```

supervisor使用

```bash
sudo supervisorctl reload #重新载入config，并且会重启所以任务 
sudo supervisorctl status
sudo supervisorctl start
sudo supervisorctl stop
```

安装postgrel

Create the file /etc/apt/sources.list.d/pgdg.list and add a line for the repository

```bash

deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main
```

```bash

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update

/usr/lib/postgresql/10/bin/pg_ctl -D /var/lib/postgresql/10/main -l logfile start

```

[参考文档](http://wiki.ubuntu.org.cn/PostgreSQL)



#### worker服务器

安装git
部分系统没有自带git的，需要自行安装git

```bash
sudo apt-get install git
```

安装node

```bash
curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
chmod +x ./nodesource_setup.sh
sudo ./nodesource_setup.sh
apt-get install nodejs,npm,build-essential
```


安装chrome依赖库

```bash
sudo apt-get install -y ﻿libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils 

```

注意安装时chrome的路径，安装完毕后将chrome写入环境变量,修改~/.bashrc文件

```bash
vi ~/.bashrc


```
在文件末尾写入一下内容：

```bash
export chrome=/chrome_path
```

安装python-pip及更新

    参考上小节

克隆代码

```bash
ssh-keygen -t rsa -C "user@mail"
cat ~/.ssh/id_rsa.pub
git clone git@10.0.5.4:splab/manualpreservation.git
git checkout -b develop
git branch --set-upstream-to=origin/develop develop
git pull
cd scrapy
npm install
```

添加dns

```bash
sudo vi /etc/resolv.conf
```

添加：nameserver 202.96.209.133，不同的IDC自行修改dns
需要重启后生效，不能省略

安装python依赖

```bash
cd /code_folder
pip install -r requirement.txt --user
```

测试

```bash
python runtest.py
```

可以正常运行，说明nodejs、chrome及python安装正确了。

添加共享目录

```bash
﻿apt-get install cifs-utils
﻿sudo mount -t cifs //10.0.5.151/temp /mnt/data -o user=****,password=*****,vers=1.0,dir_mode=0777,file_mode=0777
 sudo mount.cifs  //10.10.181.211/temp/专项 /mnt/data -o user=trainee,password='123!@#qwe',vers=1.0,dir_mode=0777,file_mode=0777

```

注意vers=1.0 协议不对会链接不上，151必须是1.0,后面是写入权限
自行修改共享的账号密码

开机自动挂载共享目录


    1.需要新建立一个文件/etc/sambapassword，这个凭证的文件名可以不同，也可以为，相应的2中的文件名也修改（也可以为：/etc/smbpasswd或者其他）
    该文件的内容为：
        username=value
        password=value
    2.在文件/etc/fstab文件中新加一行：
        //10.0.0.7/Public /home/binaryhat/Public cifs credentials=/etc/sambapasswd 0 0
    遇到权限问题，可能是你所在的用户组没有相应权限，在credentials=/etc/sambapasswd,gid=998,uid=998,vers=1.0,dir_mode=0777,file_mode=0777 0 0
    id命令可以查看相应的组用户的gid和uid
    参考：http://www.cnblogs.com/linux130/p/5682368.html
    3.以管理员身份运行(重新挂载)：
        mount -a
    如果没有错误的话，就可以挂载了。
    
共享及自动挂载非必须步骤，且共享目录可以挂载在代码目录下，因为mac下面没有mnt，这样程序运行时就无法保证输出目录统一。

启动worker

```bash
python run.py -Q snapshot -E -n scrapy
```

-n 是worker的名称，唯一不能重复

自启动worker

```bash
sudo vi /etc/supervisor/conf.d/worker.conf

```

worker.conf文件内容：

```bash
[program:scrapy]
command=python /code_path/scrapyTask.py -Q snapshot -E -n scrapy207
directory=/code_path/owlscrapy
user=username
autostart=true
autorestart=true
#log文件的位置
stdout_logfile=/code_path/scrapy.log
```

注意 code_path替换成代码所在路径，username替换成所使用的系统用户账号名

## 运行

run.py是向worker发送任务的程序，在客户端机器运行，所需依赖包见requirements_client.txt。

```bash
python run.py
```


## 注意事项


//使用终端打开pycharm
```bash

sh pycharm.sh

```

http://afnkwh.bdy.bjkhzx.com/cont/184.html（不知何意）

如果遇到无头浏览器被关掉的情况，需要使用如下命令打开：
```bash

//使用终端打开无头浏览器（确保在根目录下：spsp@spsp-desktop:~$ )
/home/spsp/manualpreservation/scrapy/node_modules/puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --remote-debugging-port=9222

/home/spsp/manualpreservation/scrapy/node_modules/puppeteer/.local-chromium/linux-575458/chrome-linux/chrome --remote-debugging-port=9222 --ppapi-flash-path=/home/spsp/manualpreservation/scrapy/node_modules/puppeteer/.local-chromium/linux-575458/chrome-linux/plugins/libpepflashplayer.so --ppapi-flash-version=30.0.0.134

//调用chrome
/opt/google/chrome/google-chrome --remote-debugging-port=9222 --ppapi-flash-path=/home/spsp/manualpreservation/scrapy/node_modules/puppeteer/.local-chromium/linux-575458/chrome-linux/plugins/libpepflashplayer.so --ppapi-flash-version=30.0.0.134

```

将scrapy.js中的第467行替换成生成的这个信息：

```bash
ws://127.0.0.1:9222/devtools/browser/b440061e-bc47-4f3b-8f5d-84357cbc9c63

```

node scrapy.js -c "{\"chrome_ws\":\"ws://127.0.0.1:9222/devtools/browser/8f9b3e59-bb55-4b4e-b371-66bb07650f60\"}" -u http://www.zxgd.com.cn

## mpClient2.py
1. 进入scrapy目录，运行chromium.sh，会自动打开chrome并将ws数据填入程序根目录的chrome.ws中
2. 启动虚拟环境，source ./venv/bin/activate
3. 然后执行./venv/bin/python mpClient2.py

# 专项巡检专用客户端说明

## inspection.py

- 支持csv格式输入待处理数据，格式见sample.csv
- 支持配置补丁，自动适配不同网站

## 配置补丁格式

```json
{
    "url":"\\w*?\\.baidu\\.com",
    "config":{
      "width": 1920,
      "height": 1024,
      "request_interval_timeout": 400,
      "mobile_emulate": true
    },
    "description":"baidu的配置"
}

```
配置中url支持通配符

## 可用配置

```json
 {
    "chrome_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", #默认情况下无需指定该参数
    "width": 1920,
    "height": 1024,
    "charset": "utf8",
    "request_timeout": 20000,
    "request_interval_timeout": 400,
    "timeout": 50000,
    "cookies": None,
    "headers": None,
    "inject_js": None,
    "inject_css": None,
    "url_filters": [],
    "exts": [],
    "screenshot_thumbnail_filename": "snapshot",
    "screenshot_thumbnail_format": "png",
    "screenshot_sliced": True,
    "screenshot_scale": 5000.0 / 1680,  # 可调切片大小比例，等于 高度/宽度,默认 ：29.7 / 21 / 4
    "output_path": "/Users/xhp/ls",  # 确保每个worker上面都存在该目录
    "pre_run": False,
    "wait_before_screenshot": 1000,
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36",
    "js_enable": True,
    "headless": False,
    "wait_before_run": 5000,  # 单位ms,运行前等待时间用于绕过验证
    "scroll_element":"html", #默认滚动元素是html，等价于document.documentElement
    "assist_id": "" #用于标签
}
```

