# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import scrapy
from meme.items import MemeItem

class PhotosSpider(scrapy.Spider):
    name = 'photos'
    allowed_domains = ['doutula.com']
    start_urls = ['http://www.doutula.com/photo/list/?page={}'.format(i)
                  for i in range(1, 1706)]

    def parse(self, response):
        for block in response.css('a.col-xs-6'):
            img = MemeItem()
            img['store_path'] = 'photos'
            img['image_urls'] = [block.css('img::attr(data-original)').extract_first()]
            img['image_caption'] = block.css('img::attr(alt)').extract_first()
            img['outfile'] = 'photos_caption.log'
            yield img
