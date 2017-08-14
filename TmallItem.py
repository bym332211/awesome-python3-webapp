#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import re
import ReadColor
import requests
import os

class MyItem:
    __item_type_const = {'男装', '女装', 'T恤', '衬衫', '牛仔', '短袖', '长袖', '短裤', '长裤', '内衣', '内裤'}
    def __init__(self, l_brand, l_item_info, l_price, l_color, l_saled, l_index, l_update_date):
        self.item_id = ''
        self.item_name = ''
        self.item_type = ''
        self.price = l_price
        self.saled = l_saled
        self.index = l_index
        self.color = self.readColor(l_color)
        self.update_date = l_update_date
        self.brand = l_brand

        if('GAP' == l_brand):
            # GAP
            self.setGap(l_item_info)
        elif('Uniqlo' == l_brand):
            self.setUniqlo(l_item_info)

        self.setType()
        # print(self.item_id, '|', self.item_name,'|',  self.item_type)

    def readColor(self, imgTagHtml):
        print(imgTagHtml)
        # '[<img alt="男装 弹力运动长裤 183508 优衣库UNIQLO" data-ks-lazyload="//img.alicdn.com/bao/uploaded/i1/TB1GFRwKFXXXXcoXXXXXXXXXXXX_!!0-item_pic.jpg_180x180.jpg" src="//assets.alicdn.com/s.gif"/>]'
        tmp = re.search('img\..*jpg_.*jpg', imgTagHtml).span()
        # end = re.search('jpg', imgTagHtml)
        # src = imgTagHtml[start:end]
        # print(imgTagHtml[int(tmp[0]):int(tmp[1])])
        uri = "http://" + imgTagHtml[int(tmp[0]):int(tmp[1])]
        tmppath = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures\\tmp' + str(self.index)
        if not os.path.exists(tmppath):
            os.mkdir(tmppath)
        # tmppath = tmppath + '\\tmp.jpg'
        self.saveImg(uri, tmppath)
        readColor = ReadColor.ReadColor()
        color = readColor.readColor(path=tmppath)
        return color

    def saveImg(self, uri, tmppath):
        pic = requests.get(uri, timeout=10)
        fp = open(tmppath + '\\tmp.jpg', 'wb')
        fp.write(pic.content)
        fp.close

    def setUniqlo(self, l_item_info):
        # Uniqlo
        tmp = re.search('\d{3,}', l_item_info).span()
        self.item_id = l_item_info[int(tmp[0]): int(tmp[1])]
        self.item_name = l_item_info[0: int(tmp[0])]


    def setGap(self, l_item_info):
        # GAP
        tmp = re.search('\d', l_item_info).span()
        self.item_id = l_item_info[int(tmp[0]):]
        self.item_name = l_item_info[0: int(tmp[0])]

    def setType(self):
        # global item_name
        tmp_name = self.item_name
        self.item_type = ''
        for type in tmp_name.split(' '):
            for type_const in self.__item_type_const:
                if str(type).__contains__(type_const):
                    self.item_type += '|' + type_const
        self.item_type = self.item_type[1:]
