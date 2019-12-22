 #coding=utf-8
import pymysql
import time
import requests
import os
from bs4 import BeautifulSoup

def get_requests_content(url):#获取目标网页信息
     r=requests.get(url)
     return r.content

def get_time_hot():#获取热点信息
    url="https://s.weibo.com/top/summary?cate=realtimehot"
    r=get_requests_content(url)
    soup = BeautifulSoup(r,"lxml")
    # print(soup.prettify())
    tb=soup.find("div",class_="data")
    data=tb.find_all("a")
    hrefs=[]
    for item in data:
        # print("https://s.weibo.com"+item.get("href"))
        hrefs.append("https://s.weibo.com"+item.get("href"))
    search_num=tb.find_all("span")
    list = []
    search=["置顶"]
    for title in data:
        # num=num+1
        # print (title)
        list.append(title.string)
    for n in search_num:
        search.append(n.string)
    return list,search,hrefs



def connect_wxremit_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='',
                           database='timehot',
                           charset="utf8")
def writeToMysql():
    db=connect_wxremit_db()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    list,search,hrefs=get_time_hot()
    print(len(list))
    for i in range(len(list)):
        sql = "INSERT INTO timehot(ID,Title,Href,Search) \
            VALUES (%s,'%s', '%s', '%s')" % \
            (0,list[i], hrefs[i], str(search[i]))
        try:
    # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except Exception as e:
        # 发生错误时回滚
            print(str(e))
            db.rollback()
        
    # 关闭数据库连接
    db.close()
writeToMysql()