from bs4 import BeautifulSoup  # 页面解析,获取数据
import re  # 正则表达式
import urllib.request, urllib.error  # 指定URL,获取页面数据
import xlwt  # 进行excel操作
import sqlite3  # 进行sql操作
import time
import os


def main():
    # baseUrl = "http://www.12371.cn/special/xxzd/jh/"
    baseUrl = "http://jhsjk.people.cn/"
    baseUrl_suffix = "result/1?form=706&else=501"
    # 1.爬取网页,并解析数据
    dataList = getIndexPage(baseUrl, baseUrl_suffix)
    # print(dataList)
    savePath = ".\\习近平重要讲话.xls"
    print(len(dataList))
    # 2.保存数据
    saveData(dataList, savePath)


# ---正则表达式---

# 标题
findInfo = re.compile(r'<a href="(.*?)" target="_blank">(.*?)</a>\[(.*?)\]', re.S)
findArticle = re.compile(r'<p style="text-indent: 2em;">(.*?)</p>', re.S)


# 1.爬取网页
# 1.1 爬取索引页面
def getIndexPage(baseUrl, baseUrl_suffix):
    dataList = []
    for i in range(1, 25):
        url_new = baseUrl + baseUrl_suffix[0:7] + str(i) + baseUrl_suffix[8:]
        html = askUrl(url_new)
        # 2.逐一解析数据
        bs = BeautifulSoup(html, "html.parser")
        for li in bs.find_all('ul', class_="list_14 p1_2 clearfix"):
            data = []
            # print("%s" %(li))
            li = str(li)
            info_new = re.findall(findInfo, li)
            for info in info_new:
                info_temp = list(info)
                info_temp[0] = baseUrl + info_temp[0]
                # info_temp.append(getArticlePage(info_temp[0]))
                dataList.append(info_temp)
                # time.sleep(3)
        print("第", str(i), "页面解析完毕")
        time.sleep(3)
    return dataList


# 1.2 爬取文章页面
def getArticlePage(article_url):
    article_data = ""
    article_html = askUrl(article_url)
    # while(article_html != ""):
    #    article_html = askUrl(article_url)
    article_bs = BeautifulSoup(article_html, "html.parser")
    for page in article_bs.find_all("div", class_="d2txt_con clearfix"):
        page = str(page)
        for p in re.findall(findArticle, page):
            p = re.sub(u"\\<.*?\\>", "", p)
            article_data += p
    print(article_data)
    return article_data


# 1.3爬取指定url
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0"}
    request = urllib.request.Request(url=url, headers=head)
    http = ""
    try:
        response = urllib.request.urlopen(request)
        http = response.read().decode("utf-8")
    # except urllib.request.socket.timeout as e:
    #    print(e)
    #    response.close()
    #    http = ""
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reson"):
            print(e.reson)
    return http


# 3.保存数据
def saveData(dataList, savePath):
    wb = xlwt.Workbook("utf-8", style_compression=0)  # 样式的压缩效果
    sheet = wb.add_sheet("习近平主席重要讲话", cell_overwrite_ok=True)  # 覆盖原单元格信息
    col = ("链接", "标题", "日期", "内容")
    for i in range(4):
        sheet.write(0, i, col[i])
    for i in range(int(len(dataList) / 4)):
        for j in range(3):
            sheet.write(i + 1, j, dataList[i][j])
    woke.save(savePath)
    print("保存完毕")


if __name__ == "__main__":
    # 调用函数
    main()
