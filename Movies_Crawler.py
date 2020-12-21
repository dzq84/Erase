'''
import urllib.request,urllib.error #指定URL,获取页面数据
#爬取指定url
def askUrl(url):
  #请求头伪装成浏览器(字典)
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3776.400 \
    QQBrowser/10.6.4212.400"}
    #进一步包装请求
    request = urllib.request.Request(url = url,headers=head)
    #存储页面源代码
    html = ""
    try:
      #页面请求,获取内容
        response = urllib.request.urlopen(request)
        #读取返回的内容,用"utf-8"编码解析
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reson)
    #返回页面源代码
    return html

from bs4 import BeautifulSoup #页面解析,获取数据
#构建了一个BeautifulSoup类型的对象soup
#参数为网页源代码和”html.parser”，表明是解析html的
bs = BeautifulSoup(html,"html.parser")
#找到所有class叫做item的div,注意class_有个下划线
bs.find_all('div',class_="item")

#Python正则表达式前的 r 表示原生字符串（rawstring）
#该字符串声明了引号中的内容表示该内容的原始含义，避免了多次转义造成的反斜杠困扰
#re.S它表示"."的作用扩展到整个字符串，包括“\n”
#re.compile()编译后生成Regular Expression对象，由于该对象自己包含了正则表达式
#所以调用对应的方法时不用给出正则字符串。
#链接
findLink = re.compile(r'<a href="(.*?)">',re.S)

#找到所有匹配的
#参数(正则表达式,内容)
#[0]返回匹配的数组的第一个元素
link = re.findall(findLink,item)[0]

import xlwt #进行excel操作
def saveData(dataList,savePath):
  #创建一个工程,参数("编码","样式的压缩效果")
    woke = xlwt.Workbook("utf-8",style_compression=0)
    #创建一个表,参数("表名","覆盖原单元格信息")
    sheet = woke.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    #列明
    col = ("链接","中文名字","英文名字","评分","标题","评分人数","概况")
    #遍历列名,并写入
    for i in range (7):
        sheet.write(0,i,col[i])
    #开始遍历数据,并写入
    for i in range (0,250):
        for j in range (7):
            sheet.write(i+1,j,dataList[i][j])
            print("第%d条数据"%(i+1))
    #保存数据到保存路径
    woke.save(savePath)
    print("保存完毕")

'''

from bs4 import BeautifulSoup #页面解析,获取数据
import re #正则表达式
import urllib.request,urllib.error #指定URL,获取页面数据
import xlwt #进行excel操作
import sqlite3 #进行sql操作
def main():
    baseUrl = "https://movie.douban.com/top250?start="
    #1.爬取网页,并解析数据
    dataList = getData(baseUrl)
    savePath=".\\豆瓣电影Top250.xls"
    #savePath = "movies.db"
    #2.保存数据
    saveData(dataList,savePath)
    #savedb(dataList,savePath)

#---正则表达式---
#链接
findLink = re.compile(r'<a href="(.*?)">',re.S)
#电影名字
findName = re.compile(r'<span class="title">(.*?)</span>',re.S)
#评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#标题
findInq = re.compile(r'<span class="inq">(.*?)</span>',re.S)
#评分人数
findCount = re.compile(r'<span>(.*?)人评价</span>')
#电影信息
findInf = re.compile(r'<p class="">(.*?)</p>',re.S)
#1.爬取网页
def getData(baseUrl):
    dataList = []
    for i in range(10):
        html = askUrl(baseUrl + str(i * 25))
        # 2.逐一解析数据
        bs = BeautifulSoup(html,"html.parser")
        for item in bs.find_all('div',class_="item"):
            data = []
            item = str(item)
            #链接
            link = re.findall(findLink,item)[0]
            #名字
            name = re.findall(findName,item)
            if len(name) == 1:
                cName = name[0]
                fName = " "
            else:
                name[1] = name[1].replace(" / ","")
                cName = name[0]
                fName = name[1]
            #评分
            rating = re.findall(findRating,item)[0]
            #标题
            inq = re.findall(findInq,item)
            if len(inq) < 1:
                inq = " "
            else:
                 inq= inq[0]
            #评分人数
            racount = re.findall(findCount,item)[0]
            #电影信息
            inf = re.findall(findInf,item)[0]
            inf = re.sub("...<br(\s+)?/>(\s?)"," ",inf)
            inf = re.sub("/"," ",inf)
            inf  = inf.strip()
            #添加一部电影的信息进data
            data.append(link)
            data.append(cName)
            data.append(fName)
            data.append(rating)
            data.append(inq)
            data.append(racount)
            data.append(inf)
            dataList.append(data)
    return dataList
#爬取指定url
def askUrl(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3776.400 QQBrowser/10.6.4212.400"}
    request = urllib.request.Request(url = url,headers=head)
    http = ""
    try:
        response = urllib.request.urlopen(request)
        http = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reson"):
            print(e.reson)
    return http
# 3.保存数据
def saveData(dataList,savePath):
    woke = xlwt.Workbook("utf-8",style_compression=0)#样式的压缩效果
    sheet = woke.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)#覆盖原单元格信息
    col = ("链接","中文名字","英文名字","评分","标题","评分人数","概况")
    for i in range (7):
        sheet.write(0,i,col[i])
    for i in range (0,250):
        for j in range (7):
            sheet.write(i+1,j,dataList[i][j])
            print("第%d条数据"%(i+1))
    woke.save(savePath)
    print("保存完毕")
#3.保存到数据库
def savedb(dataList,dataPath):
    initdb(dataPath)
    conn = sqlite3.connect(dataPath)
    cur = conn.cursor()
    #开始保存数据
    for data in dataList:
        for index in range(len(data)):
            data[index] = str('"'+data[index]+'"')
        newstr = ",".join(data)
        sql ="insert into movie(info_link,cname,fname,rating,inq,racount,inf)values(%s)"%(newstr)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("保存完毕")
#3-1新建表
def initdb(dataPath):
    conn = sqlite3.connect(dataPath)
    cur = conn.cursor()
    sql = '''
        create table movie(
        id Integer primary key autoincrement,
        info_link text,
        cname varchar ,
        fname varchar ,
        rating varchar ,
        inq text,
        racount varchar ,
        inf text
        )
    '''
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
if __name__ == "__main__":
    #调用函数
    main()