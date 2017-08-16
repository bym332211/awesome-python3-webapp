#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import requests
import xml.etree.ElementTree as ET
import os


class ReadColor():
    baseFolder = 'pictures\\base'
    depth = 0
    showCnt = 2
    # resultSet = {}

    def __init__(self, depth = 0, baseFolder = '', showCnt = 0, backGround = '白'):
        if depth:
            self.depth = depth
        if baseFolder:
            self.baseFolder = baseFolder
        if showCnt:
            self.showCnt = showCnt
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
        print(resultStr)
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
        # print(pixels)
        # pixels = [(width * 0.25, hight * 0.25), (width * 0.5, hight * 0.25), (width * 0.75, hight * 0.25),
        #           (width * 0.25, hight * 0.5), (width * 0.5, hight * 0.5), (width * 0.75, hight * 0.5),
        #           (width * 0.25, hight * 0.75), (width * 0.5, hight * 0.75), (width * 0.75, hight * 0.75)]
        i = 0
        result = ''

        basePathList = os.listdir(self.baseFolder)
        bathXml = self.baseFolder + '\\base.xml'
        tree = ET.parse(bathXml)
        root = tree.getroot()
        # parser = ET.XMLParser(recover=True)
        # ET.fromstring(xmlstring, parser=parser)

        for pixel in pixels:
            pic_color = im.getpixel(pixel)
            tmpMin = -1
            pixelClr = ''
            for color_eles in root.findall('color'):
                key = color_eles.find('key').text
                valueList = color_eles.find('valueList')
                for value in valueList.findall('value'):
                    bath_color = [int(value.find('R').text), int(value.find('G').text), int(value.find('B').text)]
                    tmpClr, tmpMin = self.pixelColor(bath_color, pic_color, key, tmpMin)
                    if tmpClr:
                        pixelClr = tmpClr
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
            result += pixelClr
            try:
                tmpCnt = self.resultSet[pixelClr]
            except KeyError:
                tmpCnt = 0
            tmpCnt = tmpCnt + 1
            self.resultSet[pixelClr] = tmpCnt
            self.saveTmp(pic_color, i)
            i = i + 1

    def pixelColor(self, bath_color, pic_color, key, tmpMin):
        # bath_color = bathIm.getpixel((1, 1))
        tmpDiff = self.colorDiff(pic_color, bath_color)
        if tmpMin < 0 or tmpDiff < tmpMin:
            return key, tmpDiff
        else:
            return '', tmpMin

    def colorDiff(self, picColor, baseColor):
        r = picColor[0]
        g = picColor[1]
        b = picColor[2]
        R = baseColor[0]
        G = baseColor[1]
        B = baseColor[2]
        diff = (r - R) * (r - R) + (g - G) * (g - G) + (b - B) * (b - B)
        return diff

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
# rc = ReadColor(depth=75,showCnt=10)
# rc.transBaseToXML()
# # uri = 'https://img.alicdn.com/bao/uploaded/i4/196993935/TB1DNc2OVXXXXa7aVXXXXXXXXXX_!!0-item_pic.jpg_180x180.jpg'
# # # rc = rc.readColor(uri=uri)
# # path = 'https://img.alicdn.com/imgextra/i4/TB1bBGBQpXXXXabaFXXXXXXXXXX_!!0-item_pic.jpg_430x430q90.jpg'
# path = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures'
# # path = 'D:\\WorkSpace_Python\\awesome-python3-webapp\\pictures\\tmp5'
# rc.readColor(path=path)


