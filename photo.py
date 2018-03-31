#!/usr/bin/env python
# encoding: utf-8
# author: zhangli  time:2018/3/31

from bs4 import BeautifulSoup
import requests
import os
import time

url='http://www.mzitu.com/all/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
url_get=requests.get(url,headers=headers)
url_soup=BeautifulSoup(url_get.content,'lxml')
soup_list=url_soup.find('div',class_="all").find_all('a')[1:]
title=0
for soup in soup_list:
    time.sleep(0.05)
    title+=1
    if not os.path.exists(os.path.join('E:\meizitu\\',str(title))):
        os.makedirs(os.path.join('E:\meizitu\\',str(title)))
    os.chdir(os.path.join('E:\meizitu\\')+str(title))
    href=soup.get('href')#总页面链接
    page_get=requests.get(href)
    page_soup=BeautifulSoup(page_get.content,'lxml')
    max_page_list=page_soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
    for max_page in range(1,int(max_page_list)):
        time.sleep(0.05)
        page_url = href + '/' + str(max_page)#每页链接

        page_header={'Referer':href,
                     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        img_get = requests.get(page_url,headers=page_header)
        img_soup=BeautifulSoup(img_get.content,'lxml')
        img_url=img_soup.find('div',class_="main-image").find_all('img')#图片标签列表
        for img in img_url:
            time.sleep(0.05)
            src=img.get('src')
            jpg=requests.get(src,headers=page_header)
            name=src[-6:-4]
            f=open(name+'.jpg','wb')
            f.write(jpg.content)
            f.close
            print(name+' 下载完成')