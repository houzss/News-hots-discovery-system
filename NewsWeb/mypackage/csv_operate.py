import csv
def write_csv(datas,TotalNum,filename):
    with open(filename,'w') as csvfile:
        fieldnames = ['id','title','txt','datetime','source', 'web' ,'batch']
        writer = csv.DictWriter(csvfile,delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        for tmp in datas.keys():
            if(count == TotalNum) :
                return
            data = datas[tmp]
            writer.writerow({'id': data['id'],'title': data['title'],'txt': data['txt'],'datetime': data['datetime'], 'source' :data['source'], 'web' :data['web'], 'batch':data['batch']})
            count += 1