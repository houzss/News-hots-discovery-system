const express = require('express')
const path = require('path')
const mysql = require('mysql')
const ejs =require('ejs')
const bodyParser = require('body-parser')
const exec = require('child_process').exec;
const app = express()
app.set('views', path.join(__dirname,'views'))
app.set('view engine','ejs')
app.use(bodyParser.urlencoded({extended:false}))
app.use(bodyParser.json())
app.use(express.static(path.join(__dirname, 'public')))
//数据库创建连接
const db = mysql.createConnection({
  host:'localhost',
  user:'root',
  password:'330324zhs',
  database: 'Hot_News'
})
db.connect((err) =>{
  if(err) throw err;
  console.log('数据库localhost连接成功')
})

app.get("/scrapy_results",(req,res)=>{//
  db.query('SELECT * FROM his_tasks',[],(err,result) => {
    if(err){
      console.log(err)
      console.log('no datas were found')
    }
    else{
      console.log(result)
      res.render("scrapy_results",{data:result})
    }
  })
})
app.get("/cluster_results",(req,res)=>{//
  db.query('SELECT * FROM his_clusters',[],(err,result) => {
    if(err){
      console.log(err)
      console.log('no datas were found')
    }
    else{
      console.log(result)
      res.render("cluster_results",{data:result})
    }
  })
})
app.get("/keyhots_results",(req,res)=>{//
  db.query('SELECT * FROM his_keyhots',[],(err,result) => {
    if(err){
      console.log(err)
      console.log('no datas were found')
    }
    else{
      console.log(result)
      res.render("keyhots_results",{data:result})
    }
  })
})



app.get("/index",(req,res)=>{//
      res.render("index.html")
})
app.get("/selectdatas",(req,res) =>{
  console.log(req.query.his_select)
  db.query('SELECT * FROM news WHERE  batch = ?',[req.query.his_select],(err,result) => {
    if(err){
        console.log(err)
        console.log('no datas were found')
        res.send({data:"error"})
    }
    else{
      //console.log(result)
      res.send({data:result})
    }
  })
})
app.get("/selectclusters",(req,res) =>{
  console.log(req.query.his_select)
  db.query('SELECT * FROM clustering WHERE  clusterbatch = ? order by categoryid;',[req.query.his_select],(err,result) => {
    if(err){
        console.log(err)
        console.log('no datas were found')
        res.send({data:"error"})
    }
    else{
      //console.log(result)
      res.send({data:result})
    }
  })
})
app.get("/selectkeyhots",(req,res) =>{
  console.log(req.query.his_select)
  db.query('SELECT * FROM keyhots WHERE  keyhotsbatch = ? order by hotvalues desc;',[req.query.his_select],(err,result) => {
    if(err){
        console.log(err)
        console.log('no datas were found')
        res.send({data:"error"})
    }
    else{
      //console.log(result)
      res.send({data:result})
    }
  })
})
app.get('/newsscrapy_pp',function(req,res){
  Scrapy_num = req.query.scrapy_num
  console.log(Scrapy_num)
  exec('python ./mypackage/scrapy_pp.py '+ Scrapy_num, function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + stderr);
            res.send({data:"error"})
        }else if(stdout.length = 0){
            console.log('error for no results')
            res.send({data:"error"})
        }else{
            var data = JSON.parse(stdout)
            console.log('receive: ' + data.batch + ' ' + data.Num);
            db.query('SELECT * FROM news WHERE  batch = ?',[data.batch],(err,result) => {
              if(err){
                console.log(err)
                console.log('no datas were found')
                  res.send({data:"error"})
              }
              else{
                res.send({data:result})
              }
            })
        }
    });
});
app.get('/newsscrapy_bj',function(req,res){
  Scrapy_num = req.query.scrapy_num
  console.log(Scrapy_num)
  exec('python ./mypackage/scrapy_bj.py '+ Scrapy_num, function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + stderr);
            res.send({data:"error"})
        }else if(stdout.length = 0){
            console.log('error for no results')
            res.send({data:"error"})
        }else{
            var data = JSON.parse(stdout)
            console.log('receive: ' + data.batch + ' ' + data.Num);
            db.query('SELECT * FROM news WHERE  batch = ?',[data.batch],(err,result) => {
              if(err){
                console.log(err)
                console.log('no datas were found')
                  res.send('error')
              }
              else{
                res.send({data:result})
              }
            })
        }
    });
});
app.get('/newsscrapy_nf',function(req,res){
    Scrapy_num =req.query.scrapy_num
    console.log(Scrapy_num)
  exec('python ./mypackage/scrapy_nf.py '+ Scrapy_num, function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + stderr);
            res.send({data:"error"})
        }else if(stdout.length = 0){
            console.log('error for no results')
            res.send({data:"error"})
        }else{
            var data = JSON.parse(stdout)
            console.log('receive: ' + data.batch + ' ' + data.Num);
            db.query('SELECT * FROM news WHERE  batch = ?',[data.batch],(err,result) => {
              if(err){
                console.log(err)
                console.log('no datas were found')
                  res.send({data:"error"})
              }
              else{
                res.send({data:result})
              }
            })
        }
    });
});

app.get("/cluster",(req,res)=>{//
  db.query('SELECT * FROM todo_clusters',[], (err,result) => {
    if(err){
      console.log(err)
      console.log('no datas were found')
    }
    else{
      console.log(result)
      res.render("cluster",{data:result})
    }
  })
})

app.get('/news_cluster',function(req,res){
  filename = req.query.todo_cluster
  console.log(filename)
  exec('python ./mypackage/clustering.py '+ filename, function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + stderr);
            res.send({data:"error"})
        }else if(stdout.length = 0){
            console.log('error for no results')
            res.send({data:"error"})
        }else{
            var data = JSON.parse(stdout)
            console.log('receive: ' + data.clustered_batch);
            db.query('SELECT * FROM clustering WHERE  clusterbatch = ? order by categoryid;',[data.clustered_batch],(err,result) => {//order by categoryid保证类号有序
              if(err){
                console.log(err)
                console.log('no datas were found')
                  res.send({data:"error"})
              }
              else{
                res.send({data:result})
              }
            })
        }
    });
});
app.get("/keyhots",(req,res)=>{//
  db.query('SELECT * FROM his_clusters',[], (err,result) => {
    if(err){
      console.log(err)
      console.log('no datas were found')
    }
    else{
      console.log(result)
      res.render("keyhots",{data:result})
    }
  })
})
app.get('/news_keyhots',function(req,res){
    filename = req.query.todo_keyhots;
    keywords_num = req.query.keywords_num;
    exec('python ./mypackage/keyhots.py ' + filename +' ' + keywords_num,function(error,stdout,stderr){
          if(error){
                console.error('error: ' + stderr);
                res.send({data:"error"})
            }else if(stdout.length = 0){
                console.log('error for no results')
                res.send({data:"error"})
            }else{
                var data = JSON.parse(stdout)
                console.log('receive: ' + data.keyhots_batch);
                db.query('SELECT * FROM keyhots WHERE  keyhotsbatch = ? order by hotvalues desc;',[data.keyhots_batch],(err,result) => {//order by categoryid保证类号有序
                      if(err){
                        console.log(err)
                        console.log('no datas were found')
                        res.send({data:"error"})
                      }
                      else{
                        res.send({data:result})
                      }
                    })
          }
      })
})

//var indexRouter = require('./routes/news');
//app.use('/selectdetails',indexRouter)
var server = app.listen(8080, () => {
  var host = server.address().address
  var port = server.address().port
  console.log("应用实例，访问地址为 http://localhost:%s", port)
})
