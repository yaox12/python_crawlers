# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy
from meme.items import MemeItem

class TemplatesSpider(scrapy.Spider):
    name = 'templates'
    allowed_domains = ['doutula.com']
    start_urls = ['http://www.doutula.com/zz/list/?page={}'.format(i)
                  for i in range(1, 13)]

    def parse(self, response):
        for block in response.css('a.col-xs-4'):
            img = MemeItem()
            img['store_path'] = 'templates'
            img['image_urls'] = [block.css('img::attr(data-original)').extract_first()]
            img['image_caption'] = block.css('img::attr(alt)').extract_first()
            img['outfile'] = 'templates_caption.log'
            yield img
