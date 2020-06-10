import pymysql
import codecs
import csv

def conn_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='330324zhs', db='Hot_News', port=3306, autocommit=True)
    return conn
def query_all(cur,sql,args):
    cur.execute(sql, args)
    return cur.fetchall()

def write_into_db(datas,TotalNum):
    db =conn_mysql()
    cursor = db.cursor()
    #sql_create_database = 'CREATE DATABASE Hot_News DEFAULT CHARACTER SET utf8'
    sql_create_table = 'CREATE TABLE IF NOT EXISTS news (id varchar(50) PRIMARY KEY, title varchar(50) not null, txt LONGTEXT not null, datetime varchar(30) not null, source varchar(50) not null, web varchar(5) not null, batch varchar(50) not null)DEFAULT CHARSET=utf8;'
    cursor.execute(sql_create_table)
    count = 0
    for tmp in datas.keys():
        if (count == TotalNum):
            break
        data = datas[tmp]
        id = data['id']
        title = data['title']
        txt = data['txt'].replace('"','\"')
        datetime = data['datetime']
        source = data['source']
        web = data['web']
        batch =data['batch']
        values = (id,title,txt,datetime,source,web,batch)
        #print(values)
        sql_insertdb = 'INSERT  INTO news(id,title,txt,datetime,source,web,batch) VALUES("%s","%s","%s","%s","%s","%s","%s");'%values
        try:
            cursor.execute(sql_insertdb)
        except:
            continue
        #print(cursor.fetchall())
        count += 1
            #print('err')
            #continue
    db.close()
    return count

def write_into_db_cluster(datas,TotalNum):
    db = conn_mysql()
    cursor = db.cursor()
    sql_create_table = 'CREATE TABLE IF NOT EXISTS clustering(clusterid varchar(50) PRIMARY KEY, categoryid int(5) not null, clusternum int(11) not null, batch varchar(50) not null,  vectors LONGTEXT not null, clusterbatch varchar(30) not null, web varchar(5) not null)DEFAULT CHARSET=utf8;'
    cursor.execute(sql_create_table)
    count = 0
    for tmp in datas.keys():
        if (count == TotalNum):
            break
        data = datas[tmp]
        clusterid= data['clusterid']
        categoryid = data['categoryid']
        clusternum = data['clusternum']
        batch = data['batch']
        vectors = data['vectors']
        clusterbatch = data['clusterbatch']
        web = data['web']
        values = (clusterid, categoryid, vectors,  clusternum, batch, clusterbatch, web)
        # print(values)
        sql_insertdb = 'INSERT  INTO clustering(clusterid, categoryid, vectors,  clusternum, batch, clusterbatch, web) VALUES("%s",%s,"%s",%s,"%s", "%s","%s");' % values
        try:
            cursor.execute(sql_insertdb)
        except:
            continue
        # print(cursor.fetchall())
        count += 1
        # print('err')
        # continue
    db.close()
    return count

def write_into_db_keyhots(datas,TotalNum):
    db = conn_mysql()
    cursor = db.cursor()
    sql_create_table = 'CREATE TABLE IF NOT EXISTS keyhots(keyhotsid varchar(50) PRIMARY KEY, categoryid int(5) not null, batch varchar(50) not null,  keywords LONGTEXT not null, keywords_num int(5) not null, hotvalues varchar(20) not null, keyhotsbatch varchar(30) not null, web varchar(5) not null)DEFAULT CHARSET=utf8;'
    cursor.execute(sql_create_table)
    count = 0
    for tmp in datas.keys():
        if (count == TotalNum):
            break
        data = datas[tmp]
        keyhotsid = data['keyhotsid']
        categoryid = data['categoryid']
        batch = data['batch']
        keywords = data['keywords']
        keywords_num = data['keywords_num']
        hotvalues = data['hotvalues']
        keyhotsbatch = data['keyhotsbatch']
        web = data['web']

        values = (keyhotsid, categoryid, batch, keywords, keywords_num, hotvalues, keyhotsbatch, web)
        # print(values)
        sql_insertdb = 'INSERT  INTO keyhots(keyhotsid, categoryid, batch, keywords, keywords_num, hotvalues, keyhotsbatch, web) VALUES("%s",%s,"%s","%s",%s,"%s","%s","%s");' % values
        try:
            cursor.execute(sql_insertdb)
        except:
            continue
        # print(cursor.fetchall())
        count += 1
        # print('err')
        # continue
    db.close()
    return count


def read_mysql_to_csv(filename):
    with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
        write = csv.writer(f, dialect='excel')
        conn = conn_mysql()
        cur = conn.cursor()
        sql = 'select * from tb_csv'
        results = query_all(cur=cur, sql=sql, args=None)
        for result in results:
            print(result)
            write.writerow(result)
