# coding=GBK

import urllib
import urllib2
import cookielib
import HTMLParser
import re
from __builtin__ import int
import smtplib, sys
from email.mime.text import MIMEText
from _ast import Sub
from __builtin__ import str

send_email_shreshold = 500.0
ticket_times = ["15:10:00", "18:40:00"] 

def getSimpleTime(str):
    pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
    match = pattern.search(str)
    if match:
        return match.group()
    else:
        return str


class parseInputParam(HTMLParser.HTMLParser):
    
    def __init__(self):
        self.para_dsc = {};
        HTMLParser.HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            key = "";
            data = "";
            for name, value in attrs:
                if name == 'name':
                    key = value
                elif name == 'value':
                    data = value
            if key != "" and data != "":
                self.para_dsc[key] = data
                    

class parsePrice(HTMLParser.HTMLParser):
    def __init__(self):
        self.result = []
        self.isTime = False
        self.isPrice = False
        self.isSpan = False
        self.isEnough = False
        self.currentTime = ""
        self.currentData = ""
        self.isSenEmail = False
        self.exceptionMsg = ""
        self.isRecode = False
        HTMLParser.HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'data-departuredatetime':
                    self.isTime = True
                    self.currentTime = getSimpleTime(value)
        if tag == 'b' and self.isTime:
            for name, value in attrs:
                if name == 'style' and value == 'font-size:1.5em':
                    self.isPrice = True
        if tag == 'span' and self.isTime:
            self.isSpan = True
                            
    def handle_data(self, data):
        if self.isPrice:
            self.currentData += data
            try :
                if float(data) < send_email_shreshold and self.currentTime in ticket_times:
                    self.isSenEmail = True
                if float(data) < 1000.0:
                    self.isRecode = True
            except Exception, e:
                self.isSenEmail = True
                self.exceptionMsg = str(e)
            self.isPrice = False
        if self.isSpan:
            self.currentData += ' , ' + data
            self.isSpan = False
                            
    def handle_endtag(self, tag):
        if self.isTime:
            if tag == 'div':
		if self.isRecode : 
                    self.result.append(self.currentTime + ' : ' + self.currentData)
                self.isTime = False
                self.isPrice = False
                self.isSpan = False
                self.isRecode = False
                self.currentTime = ""
                self.currentData = ""


def init_cookie():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)


def pre_query():
    para_dec = {}
    para_dec['countrytype'] = '0'
    para_dec['travelType'] = '0'
    para_dec['cityNameOrg'] = '北京'
    para_dec['cityCodeOrg'] = 'PEK'
    para_dec['cityNameDes'] = '烟台'
    para_dec['cityCodeDes'] = 'YNT'
    para_dec['takeoffDate'] = '2014-12-31'
    para_dec['returnDate'] = '2014-11-15'
    para_dec['adultNum'] = '1'
    para_dec['childNum'] = '0'
    
    url="""http://sc.travelsky.com/scet/queryAv.do"""
    
    req = urllib2.Request(url,urllib.urlencode(para_dec))
    req.add_header("Referer",url)
    resp = urllib2.urlopen(req)
    
    #print resp.read()
    IInputParser = parseInputParam();
    IInputParser.feed(resp.read());
    return IInputParser


def query(IInputParser):
    url2 = """http://sc.travelsky.com/scet/airAvail.do"""
    req = urllib2.Request(url2, urllib.urlencode(IInputParser.para_dsc));
    req.add_header("Referer", url2)
    content = urllib2.urlopen(req).read()

    # fp = open("test.html", "w")
    # fp.write(content)
    # fp.close

    IPriceParser = parsePrice()
    IPriceParser.feed(content)
    return IPriceParser

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
    
def print_data(isPrint, data):
    if isPrint:
        print data

def main(argv):
    
    printLog = 0
    
    if len(argv) > 1:
        printLog = argv[1]
        
    print_data(printLog, "starting...")        
    init_cookie()
    print_data(printLog,  "init_cookie end")
    IPreParser = pre_query()
    print_data(printLog,  "pre query end")
    query_result = query(IPreParser) 
    print_data(printLog,  "query end")
    if query_result.isSenEmail :
        dest_list = ["keqi24@163.com", "derek_develop@139.com"]
        if send_email(dest_list, u"ticket", "\n".join(query_result.result) + "\n" +  query_result.exceptionMsg):
            print_data(printLog, "send email success")
        else :
            print_data(printLog, "send email fail")
    elif len(query_result.result) == 0:
        send_email(dest_list, u"ticket", u"query result is empty")
    else :
        print_data(printLog, "not send email")
        
    print_data(printLog, "\n".join(query_result.result))
    print_data(printLog, "end...")
    
    return query_result.result

def sae_query():
    return main(["1", "1"])

def query_nolog():
    return main(["1"])
    
if __name__ == "__main__":
    main(sys.argv)
