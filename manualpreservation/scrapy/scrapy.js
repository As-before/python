const puppeteer = require('puppeteer');
const {URL} = require('url');
const fse = require('fs-extra'); // v 5.0.0
const path = require('path');
const cpt = require('crypto');
const GIFEncoder = require('gifencoder');
const PNG = require('png-js');
const fs = require('fs');
const request = require('request');
const process = require('process');
const gm = require('gm');
const devices = require('puppeteer/DeviceDescriptors');
const moment = require('moment');
const iPhone = devices['iPhone 6'];
var setting;
var args = {
    '-h': displayHelp,
    '-c': config,
    '-u': urlVerify,
    '-d': savePath,
};
let browser;
let log_data = {
    logs: [],
    result: {}
}
let myDate = new Date();
let currentPage;

function log(msg) {
    // console.info(msg);
    log_data.logs.push(`${moment(new Date()).format('YYYY-MM-DD HH:mm:ss')}: ${msg}`);
}


function displayHelp() {
    console.log('help:', args);
}

//检测url是否带有http://或者https://的头，没有时加入http://
function urlVerify(url) {

    let url_temp = url.toLowerCase();
    let urlReg = /^(https?:\/\/)/;
    let match = url_temp.match(urlReg);
    if (match && url_temp.length - match[0].length > 0) {
        homepage = url;
    } else if (match === null && url_temp.length > 0) {
        homepage = 'http://' + url;
    }
}

function config(cnf) {
    try {

        let conf = JSON.parse(cnf);
        setting = {
            "chrome_path": conf["chrome_path"] !== undefined ? conf["chrome_path"] : process.env.chrome ? process.env.chrome : '/home/houyuf/projects/workdir/PycharmProjects/manualpreservation/scrapy/node_modules/puppeteer/.local-chromium/linux-555668/chrome-linux/chrome',
            "chrome_ws": conf["chrome_ws"],
            "width": conf["width"] !== undefined ? conf["width"] : 1680,
            "height": conf["height"] !== undefined ? conf["height"] : 1080,
            "charset": conf["charset"] !== undefined ? conf["charset"] : "utf8", //暂未使用
            "request_timeout": conf["request_timeout"] !== undefined ? conf["request_timeout"] : 300, //暂未使用
            "request_interval_timeout": conf["request_interval_timeout"] !== undefined ? conf["request_interval_timeout"] : 400, //翻页前等待
            "timeout": conf["timeout"] !== undefined ? conf["timeout"] : 300000, //总超时
            "cookies": conf["cookies"], //暂未使用
            "headers": conf["headers"], //暂未使用
            "inject_js": conf["full_inject_js"], //暂未使用
            "inject_css": conf["full_inject_css"], //暂未使用
            "url_filters": conf["url_filters"] ? conf["url_filters"] : [], //暂未使用
            "exts": conf["exts"] ? conf["exts"] : [], //暂未使用
            'thumbnail_scale': conf["thumbnail_scale"] !== undefined ? conf["thumbnail_scale"] : 8 / 12.8,  //可调预览图大小比例，等于 高度/宽度,默认 ：8 / 12.8
            'screenshot_scale': conf["screenshot_scale"] !== undefined ? conf["screenshot_scale"] : 29.7 / 21 / 4,  //可调切片大小比例，等于 高度/宽度,默认 ：29.7 / 21 / 4
            "screenshot_thumbnail_filename": conf["screenshot_thumbnail_filename"] !== undefined ? conf["screenshot_thumbnail_filename"] : "screenshot", //截图文件名
            "screenshot_thumbnail_format": conf["screenshot_thumbnail_format"] !== undefined ? conf["screenshot_thumbnail_format"] : "png", //截图类型：png，jpeg
            "screenshot_sliced": conf["screenshot_sliced"] !== undefined ? conf["screenshot_sliced"] : true, //截图切片
            "full_page": conf["full_page"] !== undefined ? conf["full_page"] : false, //截图切片
            "index_page_filename": conf["index_page_filename"] !== undefined ? conf["index_page_filename"] : "source.html", //首页文件名
            "output_path": conf["output_path"] !== undefined ? conf["output_path"] : "/tmp", //输出文件存储路径
            "output_folder": conf["output_folder"], //输出文件存储路径
            "pre_run": conf["pre_run"] !== undefined ? conf["pre_run"] : false, //预运行，针对就自动跳转的，对taobao等跳登录无效
            "wait_before_screenshot": conf["wait_before_screenshot"] ? conf["wait_before_screenshot"] : 1000, //截图前等待
            "user_agent": conf["user_agent"] !== undefined ? conf["user_agent"] : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', //模拟浏览器
            "js_enable": conf["js_enable"] !== undefined ? conf["js_enable"] : true, //禁用js，非浏览器禁用，而是把js文件注释掉，因此仅对js文件起效
            "js_file_block": conf["js_file_block"] !== undefined ? conf["js_file_block"] : ['.js'], //禁用的js文件的文件名列表，当js_enable=false时生效
            "headless": conf["headless"] !== undefined ? conf["headless"] : true, //无头模式
            "wait_before_run": conf["wait_before_run"] !== undefined ? conf["wait_before_run"] : 20, //运行前等等时间，配合headless=false，可以手工处理弹登录等需要人工先行干预的情况
            "full_view": conf["full_view"] !== undefined ? conf["full_view"] : false, //调整view大小，注意，太大会导致浏览器卡死,
            "page_down": conf["page_down"] !== undefined ? conf["page_down"] : true, //是否翻页
            "scroll_element": conf["scroll_element"] !== undefined ? conf["scroll_element"] : "html", //翻页元素，默认是body
            "mobile_emulate": conf['mobile_emulate'] !== undefined ? conf["mobile_emulate"] : false, //模拟手机
            // 'removeList':['.qr_code_pc11','.rich_media_title','#page2'],
            //第一个去除淘宝缩放提示第二个去除淘宝登陆框框
            'updateList':conf['updateList'] !== undefined ? conf["updateList"] : ['body > div.tb-doctor > div','body > div.sufei-dialog.sufei-dialog-kissy'],
            'clickList':conf['clickList'] !== undefined ? conf["clickList"] : ['#sufei-dialog-close1'],

        };
        log_data.result.config = setting
    } catch (error) {
        // console.info(error.message.toString())
        log('错误：', error.message.toString());
        throw new Error('Config Error');
    }


}

function savePath(path) {
    setting.output_path = path
}

function mergeArray(arr1, arr2) {
    for (let i = 0; i < arr1.length; i++) {
        for (let j = 0; j < arr2.length; j++) {
            if (arr1[i] === arr2[j]) {
                arr1.splice(i, 1); //利用splice函数删除元素，从第i个位置，截取长度为1的元素
            }
        }
    }
    //alert(arr1.length)
    for (let i = 0; i < arr2.length; i++) {
        arr1.push(arr2[i]);
    }
    return arr1;
}

let md5 = str => {
    // console.info(str)
    let md5sum = cpt.createHash('md5');
    md5sum.update(str);
    str = md5sum.digest('hex');
    return str;
};

async function getPage(url, isSaveFile, browser, jsEnable, datapath) {
    let targetList = [];
    let pageisok = true;
    const page = await browser.newPage();
    currentPage = page;
    // try {
    // let timeout = false;
    if (setting.cookies && (setting.cookies instanceof Array) && setting.cookies.length>0) {
        log('开始注入cookies');
        let cookies = [];
        try {
            cookies = JSON.parse(setting.cookies);
            for (let i = 0; i < cookies.length; i++) {
                // TODO： cookie注入格式
                let cookie = cookies[i];
                await page.setCookie(cookie);

            }
            log(`当前cookies内容：${JSON.stringify(await page.cookies(url))}`);

        } catch (error) {
            log('错误：' + '设置的cookies格式错误');
            log('错误：' + error.message.toString());
        }
    }


    page.setCacheEnabled(false);

    if (setting.mobile_emulate === true) {

        await page.emulate(iPhone);
        setting.width = iPhone.viewport.width;
    } else {
        page.setUserAgent(setting.user_agent);
        await page.setViewport({width: setting.width, height: setting.height});
    }


    page.on('framenavigated', async target => {
        if (targetList.indexOf(target.url()) < 0) {
            targetList.push(target.url());
        }
        log('页面跳转至：' + await target.url());

    });

    const tag = md5(url + Date.now());

    if (log_data.result.tags === undefined) {
        log_data.result.tags = []
    }

    log_data.result.tags.push(tag);
    // todo 生成datapath文件夹


    page.once('load', () => log('页面加载完成'));

    if (!setting.js_enable) {
        await page.setRequestInterception(true);
        // await page.setJavaScriptEnabled(jsEnable === true ? true : false);
        // var todolist = []
        page.on('request', async interceptedRequest => {
            // console.info(retry)
            // retry = 5
            var block_this = false;
            if (setting.js_file_block && setting.js_file_block instanceof Array && setting.js_file_block.length>0){
                for (var i = 0; i < setting.js_file_block.length; i++) {
                    var obj = setting.js_file_block[i];
                    try{
                        if (interceptedRequest.url().endsWith(obj)){
                            block_this = true;
                        }
                    }catch(error){
                    log('js拦截文件错误：'+rror.message.toString())
                }
                }
            }else{
                try{
                    if (interceptedRequest.url().endsWith(setting.js_file_block)){
                        block_this = true;
                    }
                }catch(error){
                    log('js拦截文件错误：'+rror.message.toString())
                }

            }

            if (block_this) {
                // log(interceptedRequest.url(),jsEnable)

                let options = {
                    url: interceptedRequest.url(),
                    headers: interceptedRequest.headers(),
                    method: interceptedRequest.method()
                };
                await request(options, async (error, response, body) => {
                    log('拦截的请求：' + interceptedRequest.url(), '@' + response.connection.remoteAddress + ":" + response.connection.remotePort);
                    // 内容检测点
                    pos = body.search('setTimeout');
                    if (pos >= 0) {
                        // log('========================================')
                        log(`Warning: keyword{setTimeout} find in ${interceptedRequest.url()}`)
                        // log(`position:${pos},context:${body.substr(pos,30)}`)
                        // log('========================================')

                    }
                    if (body) {

                        await interceptedRequest.respond({
                            status: 200,
                            contentType: 'text/plain',
                            body: '//block by owl2 \n/*\n' + body + '\n*/\n//block by owl2'
                        });
                    }
                })

            } else {
                log('请求地址：' + interceptedRequest.url());
                interceptedRequest.continue();
            }

        });
    }


    page.on('response', async resp => {
        if (isSaveFile) {
            if (resp.ok()) {
                if (resp.url().substr(0, 5) === 'data:') {
                    return;
                }
                let urls = resp.url().split(',');
                let url_str = urls.length > 1 ? `${"http://"}${new URL(urls[0]).hostname}${urls[urls.length - 1]}` : urls[urls.length - 1]
                try {
                    const url = new URL(url_str);
                    let filePath = path.resolve(`${datapath}/${tag}/${url.hostname}${url.pathname}`);
                    if (path.extname(url.pathname).trim() === '') {
                        filePath = `${filePath}/index.html`;
                    }
                    await fse.outputFile(filePath, await resp.buffer().catch(error => log('caught' + error.message.toString()))).catch(error => {
                        log('错误：' + error.message.toString());
                    });
                } catch (error) {
                    log('错误：' + error.message.toString());
                }

            }

        }

    })


    await page.goto(url, {waitUntil: 'networkidle2'});

    // 截图前的等待时间
    await page.waitFor(setting.wait_before_run)

    //
    // try {
    var ele = undefined;
    let retry_ele = 5;
    while (ele === undefined || ele === null) {
        ele = await page.$(setting.scroll_element).catch(err => {
            log(err.message.toString())
            throw err;
        });
        retry_ele = retry_ele - 1;
        if (retry_ele < 0) {
            log('错误：Element not found!');
            throw new Error('错误：Element not found!');
        }
    }
    log("主元素获取成功");
    if (isSaveFile) {

        try {
            let kb = page.keyboard;
            let pagefullsize = 0;
            let pages = 100;
            let i = 0;

            if (setting.page_down) {
                // await page.$eval('#content > div > div.detail-content',elem=>elem.click());
                log("开始翻页加载");
                await page.evaluate(async (request_interval_timeout, elem) => {
                    await new Promise((resolve, reject) => {
                        let totalHeight = 0;
                        let distance = 200;
                        let timer = setInterval(() => {
                            let scrollHeight = elem.scrollHeight;
                            elem.scrollBy(0, distance);
                            totalHeight += distance;
                            if (totalHeight >= scrollHeight) {
                                clearInterval(timer);
                                resolve();
                            }
                        }, request_interval_timeout)
                    });
                }, setting.request_interval_timeout, ele).catch(error => {
                    log(error.message);
                    throw error;
                });

            } else {
                result = await page.evaluate(async elem => {

                    return Promise.resolve({
                        width: document.body.scrollWidth,
                        height: elem.scrollHeight,
                        top: document.body.scrollTop,
                        deviceScaleFactor: window.devicePixelRatio

                    })
                }, ele);
                // console.info(result)
                if (pagefullsize !== result.height) {
                    // console.info(pagefullsize,result.height)

                    pagefullsize = result.height
                    pages = Math.ceil(pagefullsize / setting.height)
                    // log(pages)
                }
            }
        } catch (error) {
            log('错误：' + error.message.toString());
            throw error;
        }
        log_data.result.title = await page.title();
                if (setting.updateList && (setting.updateList instanceof Array) && setting.updateList.length > 0) {
            log('开始修改元素相关属性.');
            let updateList = [];
            updateList = setting.updateList;
            for (let i = 0; i < updateList.length; i++) {
                try {
                    log('正在修改'+updateList[i])
                    await page.$eval(updateList[i],div => div.setAttribute('style','display:none;') );
                }catch (e) {
                    log('元素不存在：'+updateList[i])
                }
            }
        }
        // 点击指定元素
        if (setting.clickList && (setting.clickList instanceof Array) && setting.clickList.length > 0) {
            log('开始点击指定元素....');
            let clickList = [];
            clickList = setting.clickList;
            for (let i = 0; i < clickList.length; i++) {
                try {
                    log('正在点击'+clickList[i])
                    await page.$eval(clickList[i],a => a.click());
                }catch (e) {
                    log('元素不存在：'+clickList[i])
                }
            }
        }
        if (pageisok) {
            log('开始截屏...');
            await page.evaluate(elem => {
                elem.scrollTo(0, 0); //截图前移动至首页，否则容易出现截图内容错误
            }, ele);


            // let kb = page.keyboard;
            let scrollBarWidth = await page.evaluate(() => {
                var scrollBarWidthA = window.innerWidth - document.documentElement.clientWidth;
                var scrollBarWidthB = window.innerWidth - document.body.clientWidth;


                return scrollBarWidthA <= scrollBarWidthB ? scrollBarWidthA : scrollBarWidthB
            });
            let viewWidth = setting.width - scrollBarWidth;


            // let pagefullsize = await  page.evaluate(() => {
            //     console.info(document.body.offsetHeight);
            pagefullsize = await page.evaluate(elem => {
                return Promise.resolve(elem.scrollHeight);
                // return 1205
            }, ele);

            if (setting.full_view) {
                await page.setViewport({width: setting.width, height: pagefullsize});
            }

            // pagefullsize = lt

            log_data.result.screenshot_files = [];
            //create THUMBNAIL
            log('生成预览图');
            let scaled_height = parseInt(viewWidth * setting.thumbnail_scale);
            let thumbnail_height = pagefullsize > scaled_height ? scaled_height : pagefullsize;
            await page.screenshot({
                path: `${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail_origin.${setting.screenshot_thumbnail_format}`,
                clip: {x: 0, y: 0, width: viewWidth, height: thumbnail_height}
            });
            // let thumbnail_filename_path = `${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail_origin.${setting.screenshot_thumbnail_format}`;
            //缩小预览图大小，宽度为640px
            // gm会和git gm命令冲突
            await gm(`${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail_origin.${setting.screenshot_thumbnail_format}`)
                .resize(640)
                .autoOrient()
                .write(`${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail.${setting.screenshot_thumbnail_format}`, err => {
                    // console.info(err)
                    if (err !== undefined) {
                        // console.info("错误："+"预览图缩放出错 "+err)
                        log("错误：" + "预览图缩放出错 " + err)
                        log_data.result.thumbnail_file = `${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail_origin.${setting.screenshot_thumbnail_format}`
                    } else {
                        // console.info("信息："+"预览图缩放 "+err)
                        log("缩略图生成成功")
                        log_data.result.thumbnail_file = `${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail.${setting.screenshot_thumbnail_format}`
                        fse.remove(`${datapath}/${setting.screenshot_thumbnail_filename}_thumbnail_origin.${setting.screenshot_thumbnail_format}`)
                    }

                });
            // log_data.result.thumbnail_file = thumbnail_filename_path;
            if (setting.screenshot_sliced || setting.full_page) { //  { //分片截图
                log('生成分片图');
                viewHeight = parseInt(viewWidth * setting.screenshot_scale);
                pages = Math.ceil(pagefullsize / viewHeight);
                //create screenshot sliced files
                for (let i = 0; i < pages; i++) {
                    if ((pages - i) === 1) {
                        height = pagefullsize - viewHeight * i
                    } else {
                        height = viewHeight
                    }
                    await page.waitFor(setting.wait_before_screenshot);
                    await page.screenshot({
                        path: `${datapath}/${setting.screenshot_thumbnail_filename}_${i}.${setting.screenshot_thumbnail_format}`,
                        clip: {x: 0, y: i * viewHeight, width: viewWidth, height: height}
                    });
                    log_data.result.screenshot_files.push(`${datapath}/${setting.screenshot_thumbnail_filename}_${i}.${setting.screenshot_thumbnail_format}`);

                }
            }
            //输出全屏截图文件，默认不生成
            if (setting.full_page) {
                log('生成全屏图')
                let sf = gm();
                for (let i = 0; i < log_data.result.screenshot_files.length; i++) {
                    // sf.in('-page')
                    //     .in(log_data.result.sceenshot_files[i])
                    await sf.append(log_data.result.screenshot_files[i])

                }
                sf.write(`${datapath}/${setting.screenshot_thumbnail_filename}.${setting.screenshot_thumbnail_format}`, (error) => log(error));
            }

            //输出主要页面文件
            log('输出主要页面文件');
            await fse.outputFile(`${datapath}/${setting.index_page_filename}`, await page.content()).catch(error => {
                log(error.message.toString())
            });
            log_data.result.page_file = `${datapath}/${setting.index_page_filename}`;


            await page.close();
        }
        return targetList;

    }


}

function asyncFinish() {
    return new Promise((resolve, reject) => {
        "use strict";
        setTimeout(function () {
            // console.log('超时关闭');
            if (!setting.chrome_ws) {
                browser.close();
            } else {
                if (currentPage) {
                    currentPage.close();
                }
            }
            reject(new Error('Timeout 任务超时'));
            // throw
        }, setting.timeout)
    });

    // 时间可以根据具体设置, 在python中设置的是600秒
};


async function run(url) {

    if (setting.chrome_ws !== undefined) {
        // console.info('run as ws')

        browser = await puppeteer.connect({browserWSEndpoint: setting.chrome_ws});

    } else {
        // console.info('run as standlone',setting.chrome_path)

        browser = await puppeteer.launch({
            headless: setting.headless,
            executablePath: setting.chrome_path,
            timeout: setting.timeout,
            args: ['--no-sandbox', '--disable-setuid-sandbox']  // root用户运行需加上这行
        });
    }


    // log(browser.wsEndpoint());
    let targetList = [];
    let todoList = [];
    if (!setting.output_folder) {
        let timestamp = md5(url + Date.now());
        setting.data_path = `${setting.output_path}/${timestamp}`;
    } else {
        setting.data_path = `${setting.output_path}/${setting.output_folder}`;
    }
    await fse.mkdirs(setting.data_path)
    log_data.result.data_path = setting.data_path;
    // log_data.result.jobid = timestamp;
    if (setting.pre_run) {
        browser.on('targetchanged', async target => {
            if (targetList.indexOf(target.url()) < 0) {
                targetList.push(target.url())
            }
            log('目标发生变化:' + await target.url());


        });
        log('待处理清单：' + targetList);
        log('执行跳转检查');
        result = await getPage(url, isSaveFile = false, browser, jsEnable = false, datapath = setting.data_path);
        log('检查结果：' + result);

        // log(mergeArray(targetList, result));
        todoList = mergeArray(targetList, result);

    } else {
        todoList.push(url);
    }


    log('开始执行固证');
    for (let i = 0; i < todoList.length; i++) {
        log(`开始处理：${todoList[i]}`);
        await getPage(todoList[i], isSaveFile = true, browser, jsEnable = setting.js_enable, datapath = setting.data_path)

        log(`处理完成：${todoList[i]}`);
    }
    if (!setting.chrome_ws) {

        await browser.close();
    }
    // console.info(values)
    fse.outputFileSync(`${setting.data_path}/tmp.log`, log_data.logs.join('\n'), function (error) {
        log('错误：' + error.message.toString());
        throw new Error('生成日志文件出错')
    });

    log_data.result.log_file = `${setting.data_path}/tmp.log`;
    console.info(JSON.stringify(log_data.result));
    process.exit(0);

}

function errorDeal(error) {
    switch (error.message.toString().split(' ')[0]) {
        case 'net::ERR_NAME_NOT_RESOLVED':
            console.error('Ex1001', error.message.toString());
            break;
        case 'net::ERR_CONNECTION_RESET':
            console.error('Ex1002', error.message.toString());
            break;
        case 'net::ERR_TOO_MANY_REDIRECTS':
            console.error('Ex2001', error.message.toString());
            break;
        case 'Navigation':
            console.error('Ex2002', error.message.toString());
            break;
        case 'EACCES:':
            console.error('Ex3001', error.message.toString());
            break;
        case 'connect':
            console.error('Ex4001', error.message.toString());
            break;
        case 'Protocol':
            console.error('Ex4002', error.message.toString());
            break;
        case 'Config':
            console.error('Ex0001', error.message.toString()); //config的错误
            break;
        case 'Timeout':
            console.error('Ex0002', error.message.toString()); //config的错误
            break;
        default:
            // console.error(error)
            console.error("Ex0000 Unknown Error.", error.message.toString())
    }
}

try {
    if (process.argv.length > 0) {
        let url;
        process.argv.forEach(function (arg, index) {
            if (arg === '-c' || arg === '-h' || arg === '-u' || arg === '-d') {
                args[arg].apply(this, [process.argv.slice(index + 1)[0]]);

            }
        });
        if (setting && homepage) {


            log('固证对象：' + homepage);
            var tasks = Promise.all([run(homepage), asyncFinish()]);

            tasks.then((values) => {
                "use strict";

            }).catch(error => {
                "use strict";
                // console.info(error)
                if (currentPage) {
                    currentPage.close().catch(error => {
                        log('错误：' + error.message.toString());
                    })
                }
                fse.outputFileSync(`${setting.data_path}/tmp.log`, log_data.logs.join('\n'), function (error) {
                    log('错误：' + error.message.toString());
                    throw new Error('生成日志文件出错')
                });
                log('错误：' + error.message.toString());
                errorDeal(error);
                if (!setting.chrome_ws && browser) {
                    browser.close();
                }
                process.exit(-1)

            });

        }
    }
} catch (error) {
    // console.info(error.message.toString())
    errorDeal(error);
    if (browser) {
        browser.close()
    }
    process.exit(-1);
}