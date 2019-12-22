#coding utf-8
import smtplib
import pymysql
from email.mime.text import MIMEText


def connect_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='xxx',
                           database='timehot',
                           charset="utf8")
def get_timehot(tb_name):
    con = connect_db()
    cursor = con.cursor()
    sql = "select Date,title,href from "+tb_name+" order by Date desc limit 50"
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    contens = ''
    for row in res:
        time = row[0]
        title = row[1]
        link = row[2]
        contens = contens + str(time)[:10] + ' ' + title +'\n'+link+'\n'
    # print(contens)
    return contens
    
# if __name__ == '__main__':
#     get_timehot('timehot')
    





mail_user="srat1999@126.com"    #发送邮件的邮箱
mail_pass="xxxxxxxxxxx"   #密码，口令
mailto_list="xxxxxxxxxx@qq.com"   #接受邮件的邮箱
mail_host="smtp.126.com"  #设置服务器 例：smtp.126.com




strstr=get_timehot('timehot') #内容
msg = MIMEText(strstr,'plain','utf-8')  #邮件类型设置为plain
msg['Subject'] = "每日热搜" #主题
msg['From'] = mail_user
msg['To'] = mailto_list
#邮件中文如果显示乱码，可以加上下面两句
msg["Accept-Language"]="zh-CN"
msg["Accept-Charset"]="ISO-8859-1,utf-8"

print('sending...')
server = smtplib.SMTP()
server.set_debuglevel(1)
server.connect(mail_host)   #连接smtp邮件服务器
server.login(mail_user,mail_pass)   #登录
server.sendmail(mail_user, mailto_list, msg.as_string())      #发送
server.close()   #关闭
print('success!')