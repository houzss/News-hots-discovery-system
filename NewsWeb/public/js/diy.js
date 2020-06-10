$(document).ready(function() {
    var trigger = $('.hamburger'),
        overlay = $('.overlay'),
        isClosed = false;
    trigger.click(function() {
        hamburger_cross();
    });

    function hamburger_cross() {
        if (isClosed == true) {
            overlay.hide();
            trigger.removeClass('is-open');
            trigger.addClass('is-closed');
            isClosed = false;
        } else {
            overlay.show();
            trigger.removeClass('is-closed');
            trigger.addClass('is-open');
            isClosed = true;
        }
    }
    $('[data-toggle="offcanvas"]').click(function() {
        $('#wrapper').toggleClass('toggled');
    });
    $("#batchdetails").click(function () {
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/selectdatas",
            data: $("#batchdetailsOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert("error");
                }
                else
                {
                    getDetails(result.data, "tabDetails");
                }
                alert("查询成功!");
            },
            error: function () {
                alert("error");
            }
        });
     });
    $("#cbatchdetails").click(function () {
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/selectclusters",
            data: $("#cbatchdetailsOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert("error");
                }
                else
                {
                    getDetails2(result.data, "tabDetails");
                }
                alert("查询成功!");
            },
            error: function () {
                alert("error");
            }
        });
     });
    $("#news_scrapy_pp").click(function () {
        document.getElementById("news_scrapy_pp").innerHTML = '抽取中...',
        document.getElementById("news_scrapy_pp").disabled = true,
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/newsscrapy_pp",
            data: $("#scrapynameOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert("error");
                    document.getElementById("news_scrapy_pp").innerHTML = '抽取';
                    document.getElementById("news_scrapy_pp").disabled = false;
                }
                else
                {
                    alert("抽取成功!结果在以下查询表格中显示（未同步更新历史抽取任务列表,如有需要请及时刷新页面）");
                    getDetails(result.data, "tabDetails");
                    document.getElementById("news_scrapy_pp").innerHTML = '抽取';
                    document.getElementById("news_scrapy_pp").disabled = false;
                }
            },
            error: function () {
                alert("error");
                document.getElementById("news_scrapy_pp").innerHTML = '抽取';
                document.getElementById("news_scrapy_pp").disabled = false;
            }

        });
     });
    $("#news_scrapy_bj").click(function () {
        document.getElementById("news_scrapy_bj").innerHTML = '抽取中...',
        document.getElementById("news_scrapy_bj").disabled = true,
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/newsscrapy_bj",
            data: $("#scrapynameOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert("error");
                    document.getElementById("news_scrapy_bj").innerHTML = '抽取';
                    document.getElementById("news_scrapy_bj").disabled = false;
                }
                else
                {
                    alert("抽取成功!结果在以下查询表格中显示（未同步更新历史抽取任务列表,如有需要请及时刷新页面）");
                    getDetails(result.data, "tabDetails");
                    document.getElementById("news_scrapy_bj").innerHTML = '抽取';
                    document.getElementById("news_scrapy_bj").disabled = false;
                }
            },
            error: function () {
                alert("error");
                document.getElementById("news_scrapy_bj").innerHTML = '抽取';
                document.getElementById("news_scrapy_bj").disabled = false;
            }
        });
     });
    $("#news_scrapy_nf").click(function () {
        document.getElementById("news_scrapy_nf").innerHTML = '抽取中...',
        document.getElementById("news_scrapy_nf").disabled = true,
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/newsscrapy_nf",
            data: $("#scrapynameOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert('error');
                    document.getElementById("news_scrapy_nf").innerHTML = '抽取';
                    document.getElementById("news_scrapy_nf").disabled = false;
                }
                else
                {
                    alert("抽取成功!结果在以下查询表格中显示（未同步更新历史抽取任务列表,如有需要请及时刷新页面）");
                    getDetails(result.data, "tabDetails");
                    document.getElementById("news_scrapy_nf").innerHTML = '抽取';
                    document.getElementById("news_scrapy_nf").disabled = false;
                }
            },
            error: function () {
                alert("error");
                document.getElementById("news_scrapy_nf").innerHTML = '抽取';
                document.getElementById("news_scrapy_nf").disabled = false;
            }
        });
     });
    $("#news_cluster").click(function () {
        document.getElementById("news_cluster").innerHTML = '聚类中...',
        document.getElementById("news_cluster").disabled = true,
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/news_cluster",
            data: $("#clusternameOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert('error');
                    document.getElementById("news_cluster").innerHTML = '聚类';
                    document.getElementById("news_cluster").disabled = false;
                }
                else
                {
                    alert("聚类成功!结果在以下查询表格中显示");
                    getDetails2(result.data, "tabDetails");
                    document.getElementById("news_cluster").innerHTML = '聚类';
                    document.getElementById("news_cluster").disabled = false;
                }
            },
            error: function () {
                alert("error");
                document.getElementById("news_cluster").innerHTML = '聚类';
                document.getElementById("news_cluster").disabled = false;
            }
        });
     });
    $("#news_keyhots").click(function () {
        document.getElementById("news_keyhots").innerHTML = '抽取/计算中...',
        document.getElementById("news_keyhots").disabled = true,
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/news_keyhots",
            data: $("#keyhotsnameOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert('error');
                    document.getElementById("news_keyhots").innerHTML = '抽取/计算';
                    document.getElementById("news_keyhots").disabled = false;
                }
                else
                {
                    alert("话题抽取成功!结果在以下查询表格中显示");
                    getDetails3(result.data, "tabDetails");
                    document.getElementById("news_keyhots").innerHTML = '抽取/计算';
                    document.getElementById("news_keyhots").disabled = false;
                }
            },
            error: function () {
                alert("error");
                document.getElementById("news_keyhots").innerHTML = '抽取/计算';
                document.getElementById("news_keyhots").disabled = false;
            }
        });
     });
    $("#kbatchdetails").click(function () {
        $.ajax({
            type: "GET",
            dataType:"json",
            url: "/selectkeyhots",
            data: $("#kbatchdetailsOrder").serialize(),
            contentType:false,
            processData:false,
            success: function (result) {
                console.log(result)
                if(result.data=="error")
                {
                    alert("error");
                }
                else
                {
                    getDetails3(result.data, "tabDetails");
                }
                alert("查询成功!");
            },
            error: function () {
                alert("error");
            }
        });
     });




    function getDetails (json, eleId) {
        //默认的每页最多记录数
        var num1 = 10;
        //每页真实的记录数
        var num2;
        //默认展示第一页
        var page = 1;
        //切换前后页面和页码的按钮
        var page_box =document.getElementById("page_box");
        page_box.style= "visibility:visible";
        var prev = document.getElementById("prev");
        var pages = document.getElementById("pages");
        var next = document.getElementById("next");


        //计算总页数
        var count = Object.keys(json).length;
        //生成页码按钮
        function creatPages(){
            pages.innerHTML = "";
            for(var i = 0; i < Math.ceil(count / 10); i++){
                pages.innerHTML += `<button json-page="${i+1}">\xa0${i+1}\xa0</button>`;
                //pages.innerHTML += " <button json-page='${i+1}'>"+(i+1)+" <button>";
            }
        }
        creatPages();

        //渲染每一页的数据内容
        function renderPage(){
            //设置表头
            var str = "<tr><th>序号</th><th>新闻标题</th><th>新闻内容</th><th>新闻发布时间</th><th>作者</th></tr>"
            document.getElementById(eleId).innerHTML = str;

            //判断当前选择的页码对应的记录数
            if(count - num1 * (page - 1) >= 10){
                num2 = 10;
            }
            else{
                num2 = count - num1 * (page - 1);
            }

            //渲染该页对应的数据
            var str1 = "";
            for(var i = num1 * (page - 1); i < num2 + num1 * (page - 1); i++){
                str1 += "<tr>";
                str1 += "<td>" + (parseInt(i)+1) + "</td>";
                str1 += "<td>" + json[i].title + "</td>";
                str1 += "<td>" + json[i].txt + "</td>";
                str1 += "<td>" + json[i].datetime + "</td>";
                str1 += "<td>" + json[i].source + "</td>";
                str1 += "</tr>";
            }
            document.getElementById(eleId).innerHTML += str1;
        }
        //默认渲染第一页
        renderPage();

        //点击前翻按钮
        prev.onclick = function(){
            if(page > 1){
                page--;
                renderPage();
            }
        }
        //点击后翻按钮
        next.onclick = function(){
            if(page < Math.ceil(count / 10)){
                page++;
                renderPage();
            }
        }
        //点击任意页码按钮
        pages.addEventListener('click', function (e) {
            page = e.target.getAttribute('json-page');
            renderPage();
        });
    };
    function getDetails2(json, eleId) {
        //默认的每页最多记录数
        var num1 = 10;
        //每页真实的记录数
        var num2;
        //默认展示第一页
        var page = 1;
        //切换前后页面和页码的按钮
        var page_box =document.getElementById("page_box");
        page_box.style= "visibility:visible";
        var prev = document.getElementById("prev");
        var pages = document.getElementById("pages");
        var next = document.getElementById("next");


        //计算总页数
        var count = Object.keys(json).length;
        //生成页码按钮
        function creatPages(){
            pages.innerHTML = "";
            for(var i = 0; i < Math.ceil(count / 10); i++){
                pages.innerHTML += `<button json-page="${i+1}">\xa0${i+1}\xa0</button>`;
                //pages.innerHTML += " <button json-page='${i+1}'>"+(i+1)+" <button>";
            }
        }
        creatPages();

        //渲染每一页的数据内容
        function renderPage(){
            //设置表头
            var str = "<tr><th>聚类批次</th><th>聚类编号</th><th>新闻向量</th><th>聚类批次</th><th>所属批次</th><th>该类新闻数</th><th>操作</th></tr>"
            document.getElementById(eleId).innerHTML = str;

            //判断当前选择的页码对应的记录数
            if(count - num1 * (page - 1) >= 10){
                num2 = 10;
            }
            else{
                num2 = count - num1 * (page - 1);
            }

            //渲染该页对应的数据
            var str1 = "";
            for(var i = num1 * (page - 1); i < num2 + num1 * (page - 1); i++){
                str1 += "<tr>";
                str1 += "<td>" + json[i].clusterid.slice(0,14) + "</td>";
                str1 += "<td>" + json[i].categoryid + "</td>";
                str1 += "<td>" + json[i].vectors + "</td>";
                str1 += "<td>" + json[i].clusterbatch + "</td>";
                str1 += "<td>" + json[i].batch + "</td>";
                str1 += "<td>" + json[i].clusternum + "</td>";
                str1 += "<td><form id=\"clusternameOrder\" role=\"form\"><select id=\"test\" style=\"visibility: hidden;\"><option value=\"" + json[i].clusterid + "\"></option></select><input class=\"btn btn-default btn-sm btn-block\" type=\"button\" id=\"clusterdetails\"  value=\"查询\"></form></td>";
                str1 += "</tr>";
            }
            document.getElementById(eleId).innerHTML += str1;
        }
        //默认渲染第一页
        renderPage();

        //点击前翻按钮
        prev.onclick = function(){
            if(page > 1){
                page--;
                renderPage();
            }
        }
        //点击后翻按钮
        next.onclick = function(){
            if(page < Math.ceil(count / 10)){
                page++;
                renderPage();
            }
        }
        //点击任意页码按钮
        pages.addEventListener('click', function (e) {
            page = e.target.getAttribute('json-page');
            renderPage();
        });
    };
    function getDetails3(json, eleId) {
        //默认的每页最多记录数
        var num1 = 10;
        //每页真实的记录数
        var num2;
        //默认展示第一页
        var page = 1;
        //切换前后页面和页码的按钮
        var page_box =document.getElementById("page_box");
        page_box.style= "visibility:visible";
        var prev = document.getElementById("prev");
        var pages = document.getElementById("pages");
        var next = document.getElementById("next");


        //计算总页数
        var count = Object.keys(json).length;
        //生成页码按钮
        function creatPages(){
            pages.innerHTML = "";
            for(var i = 0; i < Math.ceil(count / 10); i++){
                pages.innerHTML += `<button json-page="${i+1}">\xa0${i+1}\xa0</button>`;
                //pages.innerHTML += " <button json-page='${i+1}'>"+(i+1)+" <button>";
            }
        }
        creatPages();

        //渲染每一页的数据内容
        function renderPage(){
            //设置表头
            var str = "<tr><th>抽取批次</th><th>类序号</th><th>关键词</th><th>关键词数</th><th>热力值</th><th>抽取时间</th><th>所属批次</th><th>来源网站</th></tr>"
            document.getElementById(eleId).innerHTML = str;

            //判断当前选择的页码对应的记录数
            if(count - num1 * (page - 1) >= 10){
                num2 = 10;
            }
            else{
                num2 = count - num1 * (page - 1);
            }

            //渲染该页对应的数据
            var str1 = "";
            for(var i = num1 * (page - 1); i < num2 + num1 * (page - 1); i++){
                str1 += "<tr>";
                str1 += "<td>" + json[i].keyhotsbatch + "</td>";
                str1 += "<td>" + json[i].categoryid + "</td>";
                str1 += "<td>" + json[i].keywords + "</td>";
                str1 += "<td>" + json[i].keywords_num + "</td>";
                str1 += "<td>" + json[i].hotvalues + "</td>";
                str1 += "<td>" + json[i].keyhotsbatch.slice(0,4) + '-' + json[i].keyhotsbatch.slice(5,6) +'-' + json[i].keyhotsbatch.slice(7,8) + "</td>";
                str1 += "<td>" + json[i].batch + "</td>";
                str1 += "<td>" + json[i].web + "</td>";
                str1 += "</tr>";
            }
            document.getElementById(eleId).innerHTML += str1;
        }
        //默认渲染第一页
        renderPage();

        //点击前翻按钮
        prev.onclick = function(){
            if(page > 1){
                page--;
                renderPage();
            }
        }
        //点击后翻按钮
        next.onclick = function(){
            if(page < Math.ceil(count / 10)){
                page++;
                renderPage();
            }
        }
        //点击任意页码按钮
        pages.addEventListener('click', function (e) {
            page = e.target.getAttribute('json-page');
            renderPage();
        });
    }
});
