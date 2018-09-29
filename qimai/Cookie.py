# _*_ coding:utf-8 _*_
import os
import time
import pickle

def make_path(p):
   if not os.path.exists(p):  # 判断文件夹是否存在
      os.mkdir(p)  # 创建文件夹

#请求获取cookie
def get_cookie_from_network(driver,path,loginUrl,xpath,xbutton):
   make_path(path)
   driver.get(loginUrl)
   time.sleep(2)

   for key in xpath:
      driver.find_element_by_xpath(xpath[key][0]).send_keys(xpath[key][1])

   driver.find_element_by_xpath(xbutton[0]).click()
   cookie_list = driver.get_cookies()

   #写入文件
   set_cookie(path,cookie_list)

#从缓存文件中读取cookie
def get_cookie_from_cache(path):
   with open(path, 'rb') as f:
      cookie_list = pickle.load(f)
      return cookie_list

#持久化cookie
def set_cookie(path,cookie_list):
    f = open(path, 'wb')
    pickle.dump(cookie_list, f)
    f.close()



#获取cookie
def get_cookie(flag,driver,path,loginUrl,xpath,xbutton):
   if flag:
      print('cookie过期')
      get_cookie_from_network(driver,path,loginUrl,xpath,xbutton)

   return get_cookie_from_cache(path)