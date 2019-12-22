
import smtplib
from email.mime.text import MIMEText
import pymysql 
# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "xxxxxxxx"  # 用户名
mail_pass = "xxxxxxxx"  # 密码


def connect_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='xxxxxxxx',
                           database='secWiki',
                           charset="utf8")


def get_timehot(tb_name):
    con = connect_db()
    cursor = con.cursor()
    sql = "select Date,title,href from "+tb_name+" order by Date desc limit 13"
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


sender = 'xxxxxxxx'  # 发件人邮箱
receivers = ['2404629130@qq.com','xingg051@163.com','ahu2mama@163.com']  # 接收人邮箱

 
content = get_timehot('secWiki')
title = '每日secWiki'  # 邮件主题
message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title
 
try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)
