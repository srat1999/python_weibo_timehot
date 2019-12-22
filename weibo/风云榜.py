 #coding=utf-8
from bs4 import BeautifulSoup
import os
import requests
import xlwt
import time
from xlrd import open_workbook#用于读取excel
from xlutils.copy import copy
import traceback

def get_requests_content(url):#获取目标网页信息
     r=requests.get(url)
     return r.content


def set_xls_font():#设置excel字体
    style = xlwt.XFStyle()
    font=xlwt.Font()
    font.height = 18
    style.font=font
    return style

def write_sheet():#写入文件
    try:
        rexcel = open_workbook("C:\\Users\\24046\Desktop\\风云榜.xls")#打开指定文件，如果没有文件则创建新文件
        rows = rexcel.sheets()[0].nrows#获取已有文件已经写入的行数
        excel = copy(rexcel)#对源文件进行拷贝
        table = excel.get_sheet(0)#获取表格
        list,search,hrefs = get_time_hot()#从网页获取热搜数据：list-->热搜标题，search-->搜索量，href->热搜链接
        events,href = get_social_event()#从网页获取时代数据，与热搜数据原理相同
        table.write(rows+2, 8, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))#写入数据write（行，列，值）
        table.write(rows+3,1,"热搜榜")
        table.write(rows+3,10,"时代榜")
        for i in range(len(list)):
            table.write(i+4+rows,0,str(i+1))
            formula = 'HYPERLINK("{}", "{}")'.format(hrefs[i], list[i]) #这里应用excel公式，在写入text同时写入链接，链接隐藏于文字下方
            table.write(i+4+rows,1,xlwt.Formula(formula))
            table.write(i+4+rows,6,search[i])
        for ii in range(len(events)):
            formula = 'HYPERLINK("{}", "{}")'.format(href[ii], events[ii])
            table.write(ii+4+rows,10,xlwt.Formula(formula))
        
        excel.save('C:\\Users\\24046\Desktop\\风云榜.xls')
    except Exception as e :#创建文件
        print(str(e))
        list,search,hrefs = get_time_hot()
        f=xlwt.Workbook(encoding='utf-8')
        table=f.add_sheet("风云榜",cell_overwrite_ok=True)
        events,href = get_social_event()
        rows=0
        table.write(rows+2, 8, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        table.write(rows+3,1,"热搜榜")
        table.write(rows+3,10,"时代榜")
        for i in range(len(list)):
            table.write(i+4+rows,0,str(i+1))
            formula = 'HYPERLINK("{}", "{}")'.format(hrefs[i], list[i]) 
            table.write(i+4+rows,1,xlwt.Formula(formula))
            table.write(i+4+rows,6,search[i])
        for ii in range(len(events)):
            formula = 'HYPERLINK("{}", "{}")'.format(href[ii], events[ii])
            table.write(ii+4+rows,10,xlwt.Formula(formula))
        f.save('C:\\Users\\24046\Desktop\\风云榜.xls')


def get_time_hot():#获取热点信息
    url="https://s.weibo.com/top/summary?cate=realtimehot"
    r=get_requests_content(url)#获取网页html
    soup = BeautifulSoup(r,"lxml")#Beautifulsoup解析
    # print(soup.prettify())
    tb=soup.find("div",class_="data")#分析网页html找到div class=data
    data=tb.find_all("a")#找到a标签
    hrefs=[]
    for item in data:#遍历获得链接
        # print("https://s.weibo.com"+item.get("href"))
        hrefs.append("https://s.weibo.com"+item.get("href"))
    search_num=tb.find_all("span")#找到span标签
    list = []
    search=["置顶"]
    for title in data:#遍历获得title
        # num=num+1
        # print (title)
        list.append(title.string)
    for n in search_num:#遍历获取搜索量
        search.append(n.string)
    return list,search,hrefs

def get_social_event():#获取时代信息，原理相同
    url="https://s.weibo.com/top/summary?cate=socialevent"
    r=get_requests_content(url)
    soup = BeautifulSoup(r,"lxml")
    # print(soup.prettify())
    tb=soup.find("div",class_="data")
    data=tb.find_all("a")
    hrefs=[]
    for item in data:
        hrefs.append("https://s.weibo.com"+item.get("href"))
    events=[]
    for event in data:
        events.append(event.string)
    # print(events)
    return events,hrefs
write_sheet()#主函数
# get_data()
# get_social_event()
#
#最后本程序由于加入excel公式导致xlutils工具copy方法无法copy公式的值，具体表现为前面应用公式的单元格在追加内容后为空值
#google后了解到这是excel本身的原因，如果公式不执行就没有值
#后将存储容器改为mysql数据库
