# _*_ coding:utf-8 _*_
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.byimport By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import Cookie
import pysql
import pymysql
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)



def scroll_page():

   # 返回滚动高度
   last_height = driver.execute_script("return document.body.scrollHeight")
   time.sleep(5)
   while True:
      # 滑动一次
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      # 等待加载
      time.sleep(5)

      # 计算新的滚动高度并与上一个滚动高度进行比较
      new_height = driver.execute_script("return document.body.scrollHeight")
      print(last_height)
      print(new_height)
      if new_height == last_height:
         break
      last_height = new_height

   html = driver.page_source

   return html

def get_data(html):
   soup = BeautifulSoup(html, 'html.parser')

   trAll = soup.find_all('tr', class_='ivu-table-row')
   items = []
   for trChild in trAll:
      tdAll = trChild.find_all('td')
      rank = tdAll[0].div.span.string
      url = tdAll[1].div.div.a.get('href')
      img = tdAll[1].div.div.a.img.get('src')
      pAll = tdAll[1].div.div.div.find_all('p')
      name = pAll[0].a.string
      desc = pAll[1].string
      price = tdAll[2].div.span.string
      type = tdAll[3].div.span.string
      createTime = tdAll[4].div.span.string
      item = {
         'rank': rank,
         'url': url,
         'img': img,
         'name': name,
         'desc': desc,
         'price': price,
         'type': type,
         'createTime': createTime
      }
      #print(item)
      items.append(item)
   return items

def insertData(items):
   mysql = pysql.MYSQL(host="127.0.0.1",user='root',pwd='root',db='test')
   insertSql = "INSERT INTO `qimai` (`rank`,`url`,`img`,`name`,`desc`,`price`,`type`,`createTime`) VALUES "
   for item in items:
      insertSql += f"({item['rank']},'{pymysql.escape_string(item['url'])}','{item['img']}','{pymysql.escape_string(item['name'])}','{pymysql.escape_string(item['desc'])}','{pymysql.escape_string(item['price'])}','{pymysql.escape_string(item['type'])}','{item['createTime']}'),"

   insertSql = insertSql.strip().strip(',')
   print(insertSql)

   mysql.ExecNonQuery(insertSql)

   print(mysql.ExecQuery("SELECT * FROM qimai"))

if __name__ == "__main__":

   cookiePath = './cookie/qimai.ck'
   loginUrl = 'https://www.qimai.cn/account/signin/r/%2Faccount%2F'
   xpath = {
      0:['//*[@id="app"]/div[2]/div/div/form/div[1]/div/div[1]/input','账号'],
      1:['//*[@id="app"]/div[2]/div/div/form/div[2]/div/div/input','密码']
   }
   xbutton = ['//*[@id="app"]/div[2]/div/div/form/div[4]/div/button']
   flag = 0

   while True:
      cookies = Cookie.get_cookie(flag=flag,driver=driver,path=cookiePath,loginUrl=loginUrl,xpath=xpath,xbutton=xbutton)
      print(cookies)
      time.sleep(3)
      driver.get('https://www.qimai.cn/')
      for cookie in cookies:
         driver.add_cookie(cookie)

      driver.get('https://www.qimai.cn/rank/release/genre/36/date/2018-09-24')

      locator = (By.CLASS_NAME, 'ivu-input')
      WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
      '//*[@id="footer-guide"]'

      try:
         driver.find_element_by_class_name('vip')
         print('登录成功')
         flag = 0
         break
      except Exception as e:
         print('登录失败')
         driver.delete_all_cookies()
         flag = 1

   #print(driver.page_source)
   locator = (By.CLASS_NAME, 'ivu-table-cell')
   WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator))

   html = scroll_page()

   items = get_data(html=html)

   insertData(items=items)

   driver.quit()