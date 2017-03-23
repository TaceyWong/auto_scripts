# coding:utf-8

import time
import random
import sys
from datetime import datetime
import requests
import smtplib
from email.mime.text import MIMEText
import re

province = "xx省"
school = "xx大学"
name = "xxx"
id_num = "身份证号"

local_re = re.compile(r'<option value="(\d+)">%s</option>' % province)
sc_num_re = re.compile(r'CDATA\[(\d+)\]\]></dm><mc><!\[CDATA\[%s' % school)
score_re = re.compile(r'<table .*?>.*?</table>', re.S)
html_clean_re = re.compile(r'<.*?>')


def get_result():
    index = "https://yz.chsi.com.cn/apply/cjcx/"
    content = requests.get(index).content
    local = local_re.findall(content)
    print local
    if local:
        local_num = local[0]
    else:
        return False
    url = "https://yz.chsi.com.cn/apply/cjcx/getSch.jsp?ssdm={num}&ts={ts}"  # 1487144912989"1487145595.72
    ts = int(time.time() * 1000)
    url = url.format(num=local_num, ts=ts)
    print url
    request = requests.get(url)
    result = request.content
    print result
    flag = False
    if "[%s]" % school not in result:
        return False
    sc_num = sc_num_re.findall(result)
    print sc_num
    sc_num = sc_num[0]
    score = "https://yz.chsi.com.cn/apply/cjcx/cjcxAction.do"
    data = {
        "ssdm": local_num,
        "bkdwdm": sc_num,
        "xm": name,
        "zjhm": id_num,
        "ksbh": None
    }
    score_result = requests.post(score, data=data).content

    score = score_re.findall(score_result)
    print score
    return html_clean_re.sub("", score[0]).replace("\r\n\r\n\r\n", "\n").replace("\r\n", "")


def send_email(to_list=None, title=None, content=None):
    """
    发送邮件方法
    :param to_list: 收件人列表
    :param title: 邮件题目
    :param content: 邮件内容
    :return: 成功True 失败False
    """
    MSG = MIMEText(content, 'plain', 'utf-8')
    MSG['Subject'] = title
    MSG['From'] = "wangxy@lieying.cn"
    MSG['To'] = ",".join(to_list)
    FROM = "wangxy@lieying.cn"
    PW = "WangXinyong123"
    SMTP_SERVER = "smtp.exmail.qq.com."

    flag = True
    count = 0
    while flag and count < 3:
        try:
            server = smtplib.SMTP(SMTP_SERVER, 25)  # 谷歌的是587
            server.starttls()
            # server.set_debuglevel(1)
            server.login(FROM, PW)
            server.sendmail(FROM, to_list, MSG.as_string())
            server.quit()
            flag = False
        except Exception as e:
            print "------"
            print str(e)
            print "------"
            count += 1


if __name__ == "__main__":
    while True:
        c_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print c_time
        print "-" * 100
        try:
            flag = get_result()
        except:
            flag = False
        if flag:
            if "无查询结果，返回重新查询" in flag:
                time.sleep(random.randint(30, 90))
                continue
            print flag
            to_list = ["285289578@qq.com", "1294495049@qq.com"]
            title = '%s%s考研成绩' % (name, school)
            print title
            content = c_time + "自动查询结果如下：\n" + flag
            send_email(to_list=to_list, title=title, content=content)
            sys.exit(0)
        else:
            print province,school,"成绩未出"
        print "-" * 100
        time.sleep(random.randint(30, 90))

