import requests
import json
from bs4 import BeautifulSoup
import re
import time
from db_operate import *
from csv_operate import *
import sys

home_url ='http://www.bjnews.com.cn'

headers={
    'Cookies' : 'vir_ID=158883696563531350_133241c930796c2e4219d2f9a3f566fc; Hm_lvt_ba0e7859a57505c5640c98a3fa61b61d=1588836608,1588936609,1588943462,1590048626; Hm_lpvt_ba0e7859a57505c5640c98a3fa61b61d=1590048626',
    'Host' : 'www.bjnews.com.cn',
    'Referer': 'http://www.bjnews.com.cn/',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
def get_datetime(text):
    return re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', text).pop()
def get_source(text):
    return re.findall(r'来源：([\u4e00-\u9fa5]+)', text).pop()
def geturl_data(url):
    try:
        wb_data = requests.get(url, headers=headers, timeout=5)
    except:
        #print('requests error')
        return
    return wb_data.text
def get_data(url,id,web,batch):
    new = {}
    try:
        wb_data = requests.get(url, headers=headers, timeout=5)
    except:
        #print('requests error')
        return new
    soup = BeautifulSoup(wb_data.text,'lxml')
    new['title'] = soup.select('div.title').pop().get_text().strip()
    try:
        text = ''
        txts = soup.select('div.content > p ')
        for txt in txts:
            text += txt.get_text().strip()
        new['txt'] = text.replace('\n', '').replace('\t', '')
        if(new['txt'] == ''):
            return {}
        new['datetime'] = get_datetime(str(soup.select('span.date').pop()))
        new['source'] = get_source(text)
    except:
        #print('error')
        return {}
    new['id'] = str(batch)+str(id)
    new['web'] = web
    new['batch'] = batch
    return new


def parse_data(html):
    data = json.loads(html)
    news = data['data']
    #print(news)
    url_list = []
    for new in news:
        url_list.append(new['url'])
    return url_list

def parse_url(id_list):
    url_list = []
    for id in id_list:
        url_list.append(home_url + str(id))
    return url_list
def get_datas(Scrapy_num,batch):
    i = 0
    count = 1
    news = {}
    while i < Scrapy_num:
        urll = 'http://www.bjnews.com.cn/webapi/hotlist?page=%s' % count
        try:
            id_list = parse_data(geturl_data(urll))
        except:
            print('errors happens when getting id_list')
            continue
        url_list = parse_url(id_list)
        #print(url_list)
        for url in url_list:
            #print(url)
            new = get_data(url, i+1, 'bj', batch)
            #print(new)
            if new == {}:
                continue
            else:
                news[str(i).zfill(4)] = new
                i += 1
        count += 1
    return news

def scrapy(Scrapy_num):
    #Scrapy_num = 50
    #print(Scrapy_num)
    timestamp = time.localtime()
    batch = time.strftime("%Y%m%d%H%M%S", timestamp)
    filename = '/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/csv/bj_' + batch + '.csv'
    news = get_datas(Scrapy_num,batch)

    #print('get datas ok')

    write_csv(news, Scrapy_num, filename)
    #print('write datas into csv ok')
    count = write_into_db(news,Scrapy_num)
    #print('write datas into db ok')
    result = {'batch': batch, 'Num': count}
    result_json = json.dumps(result)
    print(result_json)

def mains(argv):
    scrapy(int(argv[1]))
    #scrapy(50)
    # parse_data(datas)
if __name__ == '__main__':
    mains(sys.argv)
