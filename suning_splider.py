import asyncio
from bs4 import BeautifulSoup
from pyppeteer import *
import time
import requests
from datetime import datetime


head = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}

async def main(url, ws):
    global html
    browser = await connect({
        "browserWSEndpoint": ws
    })
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.setUserAgent(head['user-agent'])
    try:
        await page.goto(url)
        await asyncio.sleep(1)
        await page.waitFor(2000)
        now_high = 0
        while True:
            scroll_high = 400
            height = await page.evaluate('document.body.scrollHeight')
            await page.waitFor(1000)
            await page.evaluate('window.scrollBy(%d,%d)' % (0, scroll_high))
            now_high = now_high + scroll_high
            if now_high >= height:
                break
        html = await page.content()
        await page.close()
        return html
    except Exception as e:
        await page.close()
        return html



def suning_spider(key,ws):
    try:
        dataList = []
        time = datetime.now()
        url='https://search.suning.com/%s/cp=%d' % (key,1)
        page_info = asyncio.get_event_loop().run_until_complete(main(url,ws))
        html=page_info
        if html != 'error':
            soup = BeautifulSoup(html, 'html.parser')
            item_list = soup.find('div', {'id': 'product-list'})
            items = item_list.find_all('li', {'doctype': '1'})
            print(len(items))
            for item in items:
                item_price = item.find('div', {'class': 'price-box'})
                item_price = item_price.get_text()

                title_dom = item.find('div', {'class': 'title-selling-point'})
                title_a_dom = title_dom.find('a')

                item_url = title_a_dom.get('href')
                item_title = title_a_dom.get_text()

                comment = item.find('div', {'class': 'evaluate-old clearfix'})
                comment_num = comment.get_text()

                shop_dom = item.find('div', {'class': 'store-stock'})
                shop_href_dom = shop_dom.find('a')
                shop_url=shop_href_dom.get('href')
                shop_name=shop_href_dom.get_text()
                shop_address = ''
                Sales = ''
                print(comment_num,item_price)
                dataList.append(
                    {'time': time, 'item_url': item_url, 'item_title': item_title, 'shop_address': shop_address,
                     'shop_url': shop_url, 'shop_name': shop_name, 'price': item_price, 'Sales': str(Sales),
                     'comment_num': comment_num})
            return dataList
        else:
            return {'status':'error'}
    except Exception as e:
        print(e)
def getWs(chrome_url):
    ws = requests.get(url='http://' + chrome_url + "/json/version").json()["webSocketDebuggerUrl"]
    return ws
chrome_ws = getWs('127.0.0.1:9222')
spider=suning_spider('裤子',chrome_ws)