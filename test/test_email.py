#coding=gbk

import smtplib, sys
from email.mime.text import MIMEText
from _ast import Sub
from __builtin__ import str


def send_email(dest_list, sub, content):
    #设置发送服务器信息
    mail_host = "smtp.126.com"
    mail_user = "derek_develop@126.com"
    mail_pass = "derek1986"
    
    me = mail_user + "<" + mail_user +  ">"
    msg = MIMEText(content, _charset="gbk")
    msg["Subject"] = sub
    msg["From"] = me
    msg["To"] = ";".join(dest_list)
    
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, dest_list, msg.as_string())
        s.close()
        
        return True
    except Exception, e:
        print str(e)
        return False
    

dest_list = ["keqi24@163.com", "xiaolin.qxl@alibaba-inc.com"]
if send_email(dest_list, u"", u"测试内容"):
    print u"发送成功"
else :
    print u"发送失败"
    