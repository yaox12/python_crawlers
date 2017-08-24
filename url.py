#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import queue
import six.moves
import threading
import re

from six.moves.urllib.request import build_opener, HTTPCookieProcessor, Request, install_opener, urlopen
from six.moves.urllib.parse import urlencode


BASE_URL = 'https://www.panda.tv/'
HS_URL = BASE_URL + 'cate/hearthstone'

headers = {
    'Accept': '*/*',
    'Referer': BASE_URL,
    'X-Requested-With': 'XMLHttpRequest',
}

def get_content(url, data=None):
    response = urlopen(Request(url, data, headers))
    return response.read()

res = get_content(HS_URL).decode()

with open('./url/hs.html', 'w') as outfile:
    # outfile.write(str(res, encoding='utf-8'))
    # outfile.write(bytes.decode(res))
    # outfile.write(res.decode())
    outfile.write(res)

video_list = re.compile(r'<li class="video-list-item[^>]*>(.+?)</li>', re.DOTALL)
video_it = video_list.finditer(res)

with open('./url/video_list.txt', 'w') as outfile:
    get_id = re.compile(r'data-id="(\d+)"')
    get_title = re.compile(r'title="([^"]+)"')
    get_number = re.compile(r'<span class="video-number">(.+?)</span>')
    get_nickname = re.compile(r'<span class="[^>]*nickname">[\s]*(?:<i [^>]*></i>)*(.+?)[\s]*(?:<i [^>]*></i>)*[\s]*</span>', re.DOTALL)
    for match in video_it:
        video = match.group()
        id = get_id.findall(video)[0]
        outfile.write('直播链接: ' + BASE_URL + id + '\n')
        title = get_title.findall(video)[0]
        outfile.write('直播标题: %s\n' % title)
        nickname = get_nickname.findall(video)[0].strip()
        outfile.write('主播: %s\n' % nickname)
        number = get_number.findall(video)[0]
        outfile.write('观看人数: %s\n\n' % number)
    outfile.close()
