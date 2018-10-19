#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from http.cookiejar import CookieJar

import settings

# pylint: disable=C0103

def look_up_ele():
    BASE_URL = 'http://m.myhome.tsinghua.edu.cn/'
    LOGIN_URL = BASE_URL + 'Loginwindow.aspx'
    LOOKUP_URL = BASE_URL + 'weixin/weixin_student_electricity_search.aspx'

    data = {'__VIEWSTATE': '/wEPDwUJMzUxODM3OTcwZGSzjX6gFtY6tdAxR1DJThQLsW0mqCd9bss+APDYXmKA8g==',
            '__VIEWSTATEGENERATOR': '4B45C1AF',
            'LoginCtrl1$txtUserName': settings.username,
            'LoginCtrl1$txtPassword': settings.password,
            'LoginCtrl1$btnLogin': '登录'}
    cookie = CookieJar()
    handler = HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    data = urlencode(data).encode('GBK')
    res = opener.open(Request(LOGIN_URL, data)).read().decode('GBK')

    res = opener.open(Request(LOOKUP_URL, data)).read().decode('GBK')
    # with open('res.html', 'w') as f:
    #     f.write(res)

    ele = -1
    for line in res.split('\n'):
        if 'lblele' in line:
            line = line.strip()
            get_ele = re.compile(r'>(\d+)')
            ele = int(get_ele.findall(line)[0])

    return ele

def send_email(ele):
    receivers = [settings.email]

    message = MIMEText('剩余电量：{}度'.format(ele), 'plain', 'utf-8')
    message['From'] = Header('Robot', 'utf-8')
    message['To'] = Header('我', 'utf-8')

    subject = '剩余电量自动查询'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(settings.mail_host, 465)
        smtpObj.login(settings.mail_usr, settings.mail_pass)
        smtpObj.sendmail(settings.mail_usr, receivers, message.as_string())
        print('Email succeed')
    except smtplib.SMTPException:
        print('Email failed')

def main():
    print(datetime.datetime.now())
    ele = look_up_ele()
    print('剩余电量：{}度\n'.format(ele))
    if ele < 50:
        send_email(ele)

if __name__ == '__main__':
    main()
