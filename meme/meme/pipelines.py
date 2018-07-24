# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings

class MemePipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')
    cnt = 0

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        """
        results:
            [(True,
              {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
               'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
               'url': 'http://www.example.com/files/product1.pdf'}),
             (False,
              Failure(...))]
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        if image_paths[0].split('.')[-1] != 'jpg':
            raise DropItem('Image is not JPG format')

        # the filename may conflict, add a number prefix
        src_file = os.path.join(self.IMAGES_STORE, image_paths[0])
        new_file = os.path.join(self.IMAGES_STORE, item['store_path'],
                                '{}.jpg'.format(self.cnt))
        try:
            shutil.copy(src_file, new_file)
        except:
            os.mkdir(os.path.join(self.IMAGES_STORE, item['store_path']))
            shutil.copy(src_file, new_file)
        with open(item['outfile'], 'a', encoding='utf-8') as outfile:
            outfile.write('{}\t{}\n'.format(self.cnt, item['image_caption']))

        self.cnt += 1
        if self.cnt % 100 == 0:
            print('Done {}'.format(self.cnt))

        return item
