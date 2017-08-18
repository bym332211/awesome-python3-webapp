#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import requests
import xml.etree.ElementTree as ET
import os
import numpy as np
import scipy.spatial.distance
import cv2
from scipy.spatial import distance


class ReadColor():
    baseFolder = 'pictures\\base'
    depth = 0
    showCnt = 2
    # resultSet = {}

    def __init__(self, depth = 0, baseFolder = '', showCnt = 0, backGround = '白', method = '0'):
        if depth:
            self.depth = depth
        if baseFolder:
            self.baseFolder = baseFolder
        if showCnt:
            self.showCnt = showCnt
        self.method = method
        self.resultSet = {}
        self.backGround = backGround

    def readColor(self, uri = '', path = ''):
        if uri:
            pic = requests.get(uri, timeout=10)
            self.tmppath = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures\\tmp\\tmp.jpg'
            tmpFile = self.tmppath + '\\tmp.jpg'
            fp = open(tmpFile, 'wb')
            fp.write(pic.content)
            fp.close
        elif path:
            self.tmppath = path
            tmpFile = self.tmppath + '\\tmp.jpg'
        else:
            print('error')
            return 'error'
        self.pixelsColor(tmpFile)
        resultList = sorted(self.resultSet.items(), key=lambda d: int(d[1]), reverse=True)
        resultStr = ''
        backGroundCount = 0
        for i in range(0, resultList.__len__()):
            if resultList[i][0] == self.backGround:
                backGroundCount = backGroundCount + 1
                continue
            if i < self.showCnt:
                resultStr = resultStr + resultList[i][0]
        if not resultStr and backGroundCount:
            resultStr = self.backGround
        # print(resultStr)
        fp = open(self.tmppath + '\\' + resultStr + '.txt', 'w')
        fp.write('')
        return resultStr

    def pixelsColor(self, imgPath):
        im = Image.open(imgPath)
        width, hight = im.size
        # 取像素
        pixels = []
        if self.depth:
            step = 100 - self.depth
        else:
            step = 25
        rateList = []
        for rate in range(0, 100, step):
            rateList.append(rate/100)
        for x in rateList:
            for y in rateList:
                pixels.append((width * x, hight * y))
        i = 0
        result0 = ''
        result1 = ''
        result2 = ''

        basePathList = os.listdir(self.baseFolder)
        bathXml = self.baseFolder + '\\base.xml'
        tree = ET.parse(bathXml)
        root = tree.getroot()
        # parser = ET.XMLParser(recover=True)
        # ET.fromstring(xmlstring, parser=parser)

        for pixel in pixels:
            pic_color = im.getpixel(pixel)
            tmpMin0 = -1
            tmpMin1 = -1
            tmpMin2 = -1
            pixelClr0 = ''
            pixelClr1 = ''
            pixelClr2 = ''
            if self.method == 0: #HSV颜色空间
                pixelClr0 = self.readColorByHSV(pic_color)

            # else:
                for color_eles in root.findall('color'):
                    key = color_eles.find('key').text
                    valueList = color_eles.find('valueList')
                    bath_color_list = []
                    for value in valueList.findall('value'):
                        bath_color = [int(value.find('R').text), int(value.find('G').text), int(value.find('B').text)]
                        bath_color_list.append(bath_color)
                        tmpClr, tmpMin1 = self.pixelColor(bath_color, pic_color, key, tmpMin1)
                        if tmpClr:
                            pixelClr1 = tmpClr

                    tmpClr2, tmpMin2 =self.colorDiffMahala(key, pic_color, bath_color_list, tmpMin2)
                    if tmpClr2:
                        pixelClr2 = tmpClr2

            print('HSV pixelClr:', pixelClr0)
            print('欧氏 pixelClr:', pixelClr1)
            print('马氏 pixelClr:', pixelClr2)
            # for basePath in basePathList:
            #     key = basePath
            #     basePath = self.baseFolder + '\\' + basePath
            #     pixelImgList = os.listdir(basePath)
            #     # 循环比较base color与各像素
            #     for pixeImglPath in pixelImgList:
            #         bathIm = Image.open(basePath + "\\" + os.path.basename(pixeImglPath))
            #         tmpClr, tmpMin = self.pixelColor(bathIm, pic_color, key, tmpMin)
            #         if tmpClr :
            #             pixelClr = tmpClr
            result0 += pixelClr0
            result1 += pixelClr1
            result2 += pixelClr2
            try:
                tmpCnt = self.resultSet[pixelClr0]
            except KeyError:
                tmpCnt = 0
            tmpCnt = tmpCnt + 1
            self.resultSet[pixelClr0] = tmpCnt
            self.saveTmp(pic_color, i)
            i = i + 1

    def pixelColor(self, bath_color, pic_color, key, tmpMin):
        tmpDiff = self.colorDiff(pic_color, bath_color)
        if tmpMin < 0 or tmpDiff < tmpMin:
            return key, tmpDiff
        else:
            return '', tmpMin

    def colorDiffMahala(self, key, picColor, baseColorList, tmpMin):
        if self.method == 0:  # 马氏距离
            X = np.vstack((picColor, np.array(baseColorList)))
            XT = X.T
            D = np.cov(XT)
            invD = np.linalg.inv(D)
            tp = X[0] - X[1]
            diff = np.sqrt(np.dot(np.dot(tp, invD), tp.T))
            if tmpMin < 0 or diff < tmpMin:
                return key, diff
            else:
                return '', tmpMin

    def colorDiff(self, picColor, baseColor):
        zero = (0, 0, 0)
        vec1 = np.array(picColor)
        vec2 = np.array(baseColor)
        diff = np.linalg.norm(vec1 - vec2)
        # if self.method == 0: # 欧氏距离
            # X = np.vstack((picColor, baseColor))
            # Y = distance.pdist(X, 'euclidean')
        return diff
        # elif self.method == 2: # 向量夹角正弦
        #     d1 = np.linalg.norm(vec1)
        #     d2 = np.linalg.norm(vec2)
        #     cos = (vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2])/(d1 * d2)
        #     diff = 1 - cos
        # return diff

    def readColorByHSV(self, picColor):
        r = picColor[0]
        g = picColor[1]
        b = picColor[2]
        h, s, v = self.rgb2hsv(r, g, b)
        result = ''
        if v in range(0, 45):
            result = '黑'
        elif s in range(0, 43) and v in range(46, 220):
            result = '灰'
        elif s in range(0, 30) and v in range(221, 255):
            result = '白'
        elif h in range(0, 20) or h in range(310, 360):
            if s in range(43, 255) and v in range(46, 255):
                result = '红'
            elif s in range(0, 43) and v in range(221, 255):
                result = '粉'
        elif h in range(21, 50):
            if s in range(43, 255) and v in range(46, 255):
                result = '橙'
            elif s in range(0, 43) and v in range(221, 255):
                result = '橙'
        elif h in range(51, 70):
            if s in range(43, 255) and v in range(46, 255):
                result = '黄'
            elif s in range(0, 43) and v in range(221, 255):
                    result = '黄'
        elif h in range(71, 150):
            if s in range(43, 255) and v in range(46, 255):
                result = '绿'
            elif s in range(0, 43) and v in range(221, 255):
                result = '绿'
        elif h in range(151, 200):
            if s in range(43, 255) and v in range(46, 255):
                result = '青'
            elif s in range(0, 43) and v in range(221, 255):
                result = '青'
        elif h in range(201, 250):
            if s in range(43, 255) and v in range(46, 255):
                result = '蓝'
            elif s in range(0, 43) and v in range(221, 255):
                result = '蓝'
        elif h in range(251, 309):
            if s in range(43, 255) and v in range(46, 255):
                result = '紫'
            elif s in range(0, 43) and v in range(221, 255):
                result = '紫'

        return result

    def rgb2hsv2(self, image = ''):
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def rgb2hsv(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx * 255
        s = s * 255
        # h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        return round(h), round(s), round(v)

    def saveTmp(self, pic_color, i):
        tmpImg = Image.new('RGB', (30, 30), pic_color)
        tmpImg.save(self.tmppath + '\\tmp_new' + str(i) + '.jpg')

    def transBaseToXML(self):
        basePathList = os.listdir(self.baseFolder)
        string = '<colorList>\r\n'
        for basePath in basePathList:
            if basePath.endswith('.xml'):
                continue
            string += '\t<color>\r\n'
            string += '\t\t<key>' + basePath + '</key>\r\n'
            string += '\t\t<valueList>\r\n'
            basePath = self.baseFolder + '\\' + basePath
            pixelImgList = os.listdir(basePath)
            # 循环比较base color与各像素
            for pixeImglPath in pixelImgList:
                bathIm = Image.open(basePath + "\\" + os.path.basename(pixeImglPath))
                bathColor = bathIm.getpixel((1, 1))
                string += '\t\t\t<value>\r\n'
                string += '\t\t\t\t<R>' + str(bathColor[0]) + '</R>\r\n'
                string += '\t\t\t\t<G>' + str(bathColor[1]) + '</G>\r\n'
                string += '\t\t\t\t<B>' + str(bathColor[2]) + '</B>\r\n'
                string += '\t\t\t</value>\r\n'
            string += '\t\t</valueList>\r\n'
            string += '\t</color>\r\n'
        string += '</colorList>'
        tmpFile = self.baseFolder + '\\base.xml'
        if os.path.exists(tmpFile):
            os.remove(tmpFile)
        fp = open(tmpFile, 'w',encoding='UTF-8')
        fp.write(string)
        fp.close()
    #
    # def defColorBase(self):
    #     R = 51
    #     G = 51
    #     B = 51
    #     rate = [0, 1 , 2, 3, 4, 5]
    #     i = 1
    #     baseColor = []
    #     for x in rate:
    #         r = R * x
    #         for y in rate:
    #             g = G * y
    #             for z in rate:
    #                 b = B * z
    #                 baseColor.append((r, g, b))
    #
    #     for color in baseColor:
    #         imnew = Image.new('RGB', (30, 30), color)
    #         imnew.save('pictures\\base\\' + str(color[0]) + "-" + str(color[1]) + "-" + str(color[2]) +'.jpg')
    #         i = i + 1
#
#
rc = ReadColor(depth=75,showCnt=100,method=0)
# rc.transBaseToXML()
# # uri = 'https://img.alicdn.com/bao/uploaded/i4/196993935/TB1DNc2OVXXXXa7aVXXXXXXXXXX_!!0-item_pic.jpg_180x180.jpg'
# # # rc = rc.readColor(uri=uri)
# # path = 'https://img.alicdn.com/imgextra/i4/TB1bBGBQpXXXXabaFXXXXXXXXXX_!!0-item_pic.jpg_430x430q90.jpg'
# path = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures'
# rc.readColor(path=path)
#
path = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures'
rc.readColor(path=path)
# image =cv2.imread(path)
# rc.rgb2hsv2(image)


