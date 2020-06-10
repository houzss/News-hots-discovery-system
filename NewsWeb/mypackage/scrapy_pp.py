from bs4 import BeautifulSoup
import requests
import time
import re
from db_operate import *
from csv_operate import *
import sys
import json

def get_url(text):
    return re.findall(r'href="(.+?)"', text).pop()
def get_datetime(text):
    return re.findall(r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})', text).pop()
def get_data(TotalNum,batch): #
    datas = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Cookies': 'UM_distinctid=170d98c295a191-02c55bc809753f-396f7406-1fa400-170d98c295b24b; paperSearhType=3; aliyungf_tc=AQAAAInvVBjuRAcAaMvrc72/ZJLK+SFE; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=3141DA08BDA29731EE039E6628E95B91; uuid=5210d978-1e0b-4c9a-892d-bf0da9fa37d8; SERVERID=srv-omp-ali-portal12_80; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1585208113,1585211253,1585221331,1586414878; CNZZDATA1261102524=797740587-1584194824-null%7C1586410230; __ads_session=du0MrnOtdAlicuMFSQA=; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1586415240',
        'Host': 'www.thepaper.cn',
        'Referer': 'https://www.thepaper.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    headers_txt ={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Cookies': 'UM_distinctid=170d98c295a191-02c55bc809753f-396f7406-1fa400-170d98c295b24b; paperSearhType=3; aliyungf_tc=AQAAAInvVBjuRAcAaMvrc72/ZJLK+SFE; route=030e64943c5930d7318fe4a07bfd2a3c; JSESSIONID=3141DA08BDA29731EE039E6628E95B91; uuid=5210d978-1e0b-4c9a-892d-bf0da9fa37d8; SERVERID=srv-omp-ali-portal12_80; Hm_lvt_94a1e06bbce219d29285cee2e37d1d26=1585208113,1585211253,1585221331,1586414878; CNZZDATA1261102524=797740587-1584194824-null%7C1586410230; __ads_session=g5zHjmmtdAlvO5QCSwA=; Hm_lpvt_94a1e06bbce219d29285cee2e37d1d26=1586415145',
        'Host': 'www.thepaper.cn',
        'Referer': 'https://www.thepaper.cn/',
    }
    home_url ='https://www.thepaper.cn/'
    count = 0
    i = 0
    while i <= TotalNum:
        if count != 0:
            time.sleep(1)
        tsp = int(time.time() * 1000)
        url = f'''https://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=6882016,6879104,6883411,6883496,6883635,&pageidx={count}&lastTime={tsp}'''
        #print(url)
        try:
            wb_data = requests.get(url, headers=headers,timeout=5)
        except:
            #print('requests error')
            return datas
        if(wb_data.status_code != 200):
            return datas
        soup = BeautifulSoup(wb_data.text, 'lxml')
        #print(soup)
        #titles = soup.select('div.news_li > h2 ')
        #overviews = soup.select('div.news_li > p')
        urls = soup.select('div.news_li > h2 > a')
        for single_url in urls:
            if(i == TotalNum):
                return datas
            data={}
            urll = home_url + get_url(str(single_url))
            #time.sleep(1)
            #print(urll)
            try:
                txt_data = requests.get(urll, headers=headers_txt, timeout=5)
            except  requests.exceptions.ConnectionError:
                #print(1)
                continue
            except:
                continue
            if (txt_data.status_code != 200):
                if urls.index(single_url) != len(urls):
                    continue
                else:
                    return datas
            soup1 = BeautifulSoup(txt_data.text, 'xml')
            if soup1.select('div.newscontent > h1'):
                data['title'] = soup1.select('div.newscontent > h1').pop().get_text().strip()
                data['txt'] = soup1.select('div.news_txt').pop().get_text().strip()
                if soup1.select('div.news_about > p >span').pop().get_text().strip() != '':
                    #print(1)
                    data['datetime'] = get_datetime(soup1.select('div.news_about > p').pop().get_text().strip())
                    data['source'] = soup1.select('div.news_about > p >span').pop().get_text().strip().strip('来源：').strip('@')
                else:
                    #print(2)
                    news_about = soup1.select('div.news_about > p')
                    data['datetime'] = news_about.pop(1).get_text().strip()
                    data['source'] = news_about.pop(0).get_text().strip().strip('来源：').strip('@')
            elif soup1.select('div.video_txt_t > h2'):
                #print(3)
                data['title'] = soup1.select('div.video_txt_t > h2').pop().get_text().strip()
                data['txt'] = soup1.select('div.video_txt_l > p').pop().get_text().strip()
                news_about = soup1.select('div.video_info_left > span')
                data['datetime'] = news_about.pop(0).get_text().strip()
                data['source'] = news_about.pop().get_text().strip().strip('来源：').strip('@')
            else:
                continue
            #print(data)
            data['web'] ='pp'
            data['id'] = batch + str(i+1)
            data['batch'] = batch
            datas[str(i).zfill(4)] = data
            i += 1
        count += 1
        #print(str(i)+': ok')
    #print(datas)
    #print(len(datas.keys()))
    return datas

def scrapy(TotalNum):
    #TotalNum = 50
    #filename = '/private/tmp/mysql_dumpdata/test.csv'
    #print(TotalNum)
    timestamp = time.localtime()
    batch = time.strftime("%Y%m%d%H%M%S", timestamp)
    filename = '/Users/bubblesponge/Desktop/new_hot_system/NewsWeb/mypackage/csv/pp_' + batch + '.csv'
    datas = get_data(TotalNum, batch)
    #print('get datas ok')
    write_csv(datas,TotalNum,filename)
    #print('write datas into csv ok')
    count = write_into_db(datas,TotalNum)
    #print('write datas into db ok')
    result={'batch':batch,'Num':count}
    result_json = json.dumps(result)
    print(result_json)

def mains(argv):
    scrapy(int(argv[1]))
    # parse_data(datas)
if __name__ == '__main__':
    mains(sys.argv)

