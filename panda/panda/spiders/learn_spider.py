#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import six.moves
import scrapy


class PandaSpider(scrapy.Spider):
    name = "learn"

    def start_requests(self):
        # use existing cookies
        '''
        urls = [
            'http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=2',
        ]
        cookie = {'THNSV2COOKIE': 'MDY0MzczNjg3YmMyNTQ0MjgzODc3ODZjZjBlOTM2NDBgMjAxNjMxMDYyM2DSpvbOYFNgNTguMjAwLjEyOS4xMzBgMzc3MDk1NDYxYDE1MDM5MDUzNDk1NDRgMDFLNDdGTTRLRE43VVY4RkdKOUdSTUdOYA--',
                  'JSESSIONID': 'abcIFjv0YwAzK53bVPN4v',
        }
        
        for url in urls:
            yield scrapy.Request(url, cookies=cookie, callback=self.parse)
        '''
        return [scrapy.FormRequest(url='https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp',
                                  formdata={'userid': 'yaox16', 'userpass': 'xy2011010044'},
                                  callback=self.parse)]

    def parse(self, response):  
        cookie = response.headers.getlist('Set-Cookie')
        # print(cookie)
        return scrapy.Request(url='http://learn.tsinghua.edu.cn/MultiLanguage/lesson/student/MyCourse.jsp?typepage=2',
                            #   cookies=cookie,
                              callback=self.after_login)

    def after_login(self, response):
        with open('result/learn_body.html', 'wb') as bodyfile:
            bodyfile.write(response.body)
            bodyfile.close()
        
        with open('result/learn_lessons.json', 'w') as jsonfile:
            for lesson in response.css('tr[class*=info_tr]'):
                json.dump({
                    '课程名称': lesson.css('a::text').extract_first().strip(),
                    'url': lesson.css('a::attr(href)').extract_first(),
                }, jsonfile, indent=4, ensure_ascii=False)
                jsonfile.write('\n')
            jsonfile.close()
