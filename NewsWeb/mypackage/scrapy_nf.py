import requests
import json
from bs4 import BeautifulSoup
import re
import time
from db_operate import *
from csv_operate import *
import sys

home_url ='http://www.infzm.com/contents/'

headers={
    'Cookies' : 'acw_tc=7819730615841978594274616e09ebb31184b13914dfe17657a6e9150151c9; machine_id=6fe7a7f3939daca29e592d52a0cab045; XSRF-TOKEN=eyJpdiI6IlpZZEtnQmNXaHdTTTRkZ1NDQWttRnc9PSIsInZhbHVlIjoiWDZlUER2KzVtMXAxRjZmZ0ZqTjIxakVnUDNyamZwakx4M0cxUnp3MHRDMHVja1IrT2FvVHRuV2xNY1luWUNLayIsIm1hYyI6IjI3NjgwZmVmZmI0ODQ2NTQzNDk3MjUwZTA3MmZlNmY0OWY0ZDA4YzQ0YTcxMTNmOWRmYTI2MWQ0OGZiMWIyYjgifQ%3D%3D; passport_session=eyJpdiI6IjdsaWVGQlJ3K1lVWGl4bVFOZ2cxTGc9PSIsInZhbHVlIjoiRUt0TVEwWVRIbFVUb0lPZ2RVc0QxRTdvTk9iTUVEZTMrVjlXVEtGKzVJVm14dXRSK2I0aUwwM3lKeEp2c244QiIsIm1hYyI6IjZkYTk4NjRjMmUzNjhmYTFkZTFkMGM2YWZiNWM0YmQwNTIyZTY4M2NiNGM5OGZmYzZmMjczOTgxNTI2MWJjODkifQ%3D%3D',
    'Host' : 'www.infzm.com',
    'Referer': 'http://www.infzm.com/',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}
def get_datetime(text):
    return re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', text).pop()
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
    try:
        new['title'] = soup.select('div.nfzm-content__title').pop().get_text().strip()
        text = ''
        txts = soup.select('div.nfzm-content__fulltext > p ')
        for txt in txts:
            text += txt.get_text().strip()
        new['txt'] = text.replace('\n', '').replace('\t', '')
        if(new['txt'] == ''):
            return {}
        new['datetime'] = get_datetime(str(soup.select('span.nfzm-content__publish').pop()))
        new['source'] = soup.select('p.nfzm-content__author >span').pop().get_text().strip('作者：')
    except:
        #print('error')
        return {}
    new['id'] = str(batch)+str(id)
    new['web'] = web
    new['batch'] = batch
    return new


def parse_data(html):
    data = json.loads(html)
    news = data['data']['contents']
    #print(news)
    id_list = []
    for new in news:
        id_list.append(new['id'])
    return id_list

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
        urll = 'http://www.infzm.com/contents?term_id=1&page=%s&format=json' % count
        try:
            id_list = parse_data(geturl_data(urll))
        except:
            #print('errors happens when getting id_list')
            continue
        url_list = parse_url(id_list)
        # print(url_list)
        for url in url_list:
            #print(url)
            new = get_data(url, i+1, 'nf', batch)
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
    filename = '/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/csv/nf_' + batch + '.csv'
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
    # parse_data(datas)
if __name__ == '__main__':
    mains(sys.argv)
