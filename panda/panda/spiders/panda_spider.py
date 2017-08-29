#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import six.moves
import scrapy

BASE_URL = 'https://www.panda.tv'

class PandaSpider(scrapy.Spider):
    name = "panda"
    
    def start_requests(self):
        urls = [
            BASE_URL + '/cate/hearthstone',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        cookie = response.headers.getlist('Cookie')
        print(cookie)
        with open('panda_body.html', 'wb') as bodyfile:
            bodyfile.write(response.body)
            bodyfile.close()
        with open('panda_videos.json', 'w') as jsonfile:
            for video in response.css('li.video-list-item'):
                json.dump({
                    '直播链接': BASE_URL + video.css('a.video-list-item-wrap::attr(href)').extract_first(),
                    '直播标题': video.css('span.video-title::text').extract_first(),
                    '主播': ''.join(video.css('span[class*=nickname]::text').extract()).strip(),
                    '观看人数': video.css('span.video-number::text').extract_first(),
                }, jsonfile, indent=4, ensure_ascii=False)
            jsonfile.close()
