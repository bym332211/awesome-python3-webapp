from bs4 import BeautifulSoup
import time
from selenium import webdriver
import MySQL
import re
import datetime
import TmallItem

class spider:
    global db
    global browser_path
    global baseUrl
    global item_style
    global startTime
    global brand
    def __init__(self, l_browser, l_targetUrl, l_style):
        global db
        global browser_path
        global baseUrl
        global item_style
        global  startTime
        global brand
        browser_path = l_browser
        baseUrl = l_targetUrl
        db = MySQL.MyDB()
        item_style = l_style
        startTime = datetime.date.today().strftime("%Y/%m/%d")
        if(re.search('uniqlo', l_targetUrl, re.I)):
            brand = 'Uniqlo'
        elif (re.search('Gap', l_targetUrl, re.I)):
            brand = 'GAP'

    def getHtml(self, url):
        driver = webdriver.PhantomJS(browser_path)
        driver.get("http://www.tmall.com")
        # 获得cookie信息
        cookie = driver.get_cookies()
        driver.get(url)
        time.sleep(3)
        html = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def parseItemList(self, soup):
        L = soup.find_all('div', attrs={'class': item_style})
        return L

    def parseItem(self, itemList):
        for item in itemList:
            soup = BeautifulSoup(str(item), 'html.parser')
            L = soup.find_all('a',attrs={'class': 'item-name J_TGoldData'})
            P = soup.find_all('span', attrs={'class': 'c-price'})
            S = soup.find_all('span', attrs={'class': 'sale-num'})
            # 获取图片
            I = []
            for j in range(0,5):
                tmp = str(L[j].text).rstrip()
                img = soup.find_all('img', attrs={'alt': tmp})
                I.append(str(img))
            i = 0
            for itemName in L:
                if(str(L[i].text).startswith("   ")):
                    break;
                # l_brand, l_item_info, l_price, l_color, l_saled, l_update_date
                self.idx = self.idx + 1
                myitem = TmallItem.MyItem(brand, L[i].text, P[i].text.rstrip(), I[i], S[i].text.rstrip(), self.idx, startTime)
                s = str("item[" + str(i) + "]:" + "name:" + L[i].text + " price:" + P[i].text + " saled:" + S[i].text + " color:" + myitem.color)
                sql = """
                    insert into tmall.item(
                        item_id,
                        item_name,
                        item_type,
                        price,
                        color,
                        brand,
                        saled,
                        update_date
                    ) values (
                        '%s','%s','%s',%s,'%s','%s',%s,'%s')
                        """ % \
                      (myitem.item_id, myitem.item_name, myitem.item_type, myitem.price, myitem.color, myitem.brand, myitem.saled, myitem.update_date)
                db.insert(sql)
                i = i + 1
                print(s)

    def start(self):
        self.idx = 0
        for i in range(1, 6):
            print(str(i))
            url = baseUrl + '&pageNo='+str(i)
            html = self.getHtml(url)
            itemList = self.parseItemList(html)
            self.parseItem(itemList)
        db.__close__()
