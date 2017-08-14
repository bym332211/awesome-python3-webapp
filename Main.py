#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Spider

browser_path = 'C:\\Program Files\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
# Uniqlo
url = 'https://uniqlo.tmall.com/category-97377015.htm?orderType=hotsell_desc'
item_style = 'item5line1'

# Gap
# url = 'https://gap.tmall.com/category-1230274519-1303053496.htm?orderType=hotsell_desc'
# item_style = 'item3line1'

spider = Spider.spider(browser_path, url, item_style)
spider.start()