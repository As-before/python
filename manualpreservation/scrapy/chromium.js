const puppeteer = require('puppeteer');
const {URL} = require('url');
const fse = require('fs-extra'); // v 5.0.0
const path = require('path');
const cpt = require('crypto');
var GIFEncoder = require('gifencoder');
var PNG = require('png-js');
const fs = require('fs');
const request = require('request');
// const Date = require('Date');
const process = require('process');
const gm = require('gm');
var setting;
var args = {
    '-h': displayHelp,
    '-c': config
};


function displayHelp() {
    console.log('help:', args);
}

function config(cnf) {
    try {
//    console.info(typeof(cnf))
        var conf = JSON.parse(cnf);
        setting = {
            "chrome_path": conf["chrome_path"] !== undefined ? conf["chrome_path"] : process.env.chrome ? process.env.chrome : '/home/netboss/manualpreservation/scrapy/node_modules/_puppeteer@1.8.0@puppeteer/.local-chromium/linux-588429/chrome-linux/chrome',
            "headless": conf["headless"] !== undefined ? conf["headless"] : true, //无头模式
            "ws_file":conf["ws_file"] !== undefined?conf["ws_file"]:'./chrome.ws'//ws数据输出文件
        };
    } catch (error) {
        console.info('错误：' + error.message.toString());
    }


}

async function run() {
    const browser = await puppeteer.launch({
        headless: setting.headless,
        executablePath: setting.chrome_path,
        timeout:setting.timeout});
    await fse.outputFile(setting.ws_file,browser.wsEndpoint());
    console.info(browser.wsEndpoint());

}

try {
    if (process.argv.length > 0) {

        process.argv.forEach(function (arg, index) {

            if (arg === '-c' || arg === '-h') {

                args[arg].apply(this, [process.argv.slice(index + 1)[0]]);
            }
        });
        if (setting) {

            run();
        }
    }
} catch (error) {
    console.info('错误：' + error.message.toString());
    process.exit(-1);
}
