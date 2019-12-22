import requests
import pymysql
import re


def get_timehot(tb_name):
    con = connect_db()
    cursor = con.cursor()
    sql = "select Date,title,href from "+tb_name+" order by Date desc limit 30"
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    contens = ''
    for row in res:
        time = row[0]
        title = row[1]
        link = row[2]
        contens = contens + str(time)[:10] + ' ' + title +'\n'+link+'\n'

    return contens 

    
def getTitleAndLink():
    conlist = []
    hreflist = []
    r = requests.session()
    content = r.get("https://www.sec-wiki.com/news").text
    conlist = re.findall(r'.*">(.*)</a></td><td><a target=".*',content,re.M)
    hreflist = re.findall(r'.*class="links" href=\"((https|http)://.*?)\">.*',content,re.M)
    linklist = []
    for href in hreflist:
        linklist.append(href[0])
    return conlist,linklist


def connect_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='Flzx3000c$',
                           database='secWiki',
                           charset="utf8")


def writeToMysql():
    con = connect_db()
    cursor = con.cursor()
    conlist,linklist = getTitleAndLink()
    yesterday_content = get_timehot('secWiki')
    
    for i in range(len(conlist)):
        if linklist[i] not in yesterday_content:
            sql = "INSERT INTO secWiki(Title,Href) \
                VALUES ('%s', '%s')" % \
                (conlist[i], linklist[i])
            try:
        # 执行sql语句
                cursor.execute(sql)
                # 执行sql语句
                con.commit()
            except Exception as e:
            # 发生错误时回滚
                print(str(e))
                con.rollback()
        
    # 关闭数据库连接
    con.close()
if __name__ == '__main__':
    writeToMysql()
    # getTitleAndLink()
    


