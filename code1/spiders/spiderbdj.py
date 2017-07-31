#coding=utf-8
import urllib,urllib2,requests
import os,sys
from bs4 import BeautifulSoup
import time

print time.ctime()

domain = 'http://www.budejie.com/'
main_url = 'http://www.budejie.com/video/1'
midd_urls = []
video_urls = []

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

req = urllib2.Request(main_url,headers=headers)
resp = urllib2.urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(resp,'html.parser')
a_list = soup.find_all('a')

for a in a_list:
    try:
        url = a['href']
        # print url
    except Exception as e:
        pass
    else:
        if url.startswith('/detail'):
            midd_urls.append(domain+url)
    list(set(midd_urls))
# print midd_url
print time.ctime()
for midd_url in midd_urls:
    req = urllib2.Request(midd_url, headers=headers)
    resp = urllib2.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(resp, 'html.parser')
    a_list = soup.find_all('a')
    for a in a_list:
        try:
            url = a['href']
        except Exception as e:
            pass
        else:
            if url.endswith('.mp4'):
                video_urls.append(url)
        list(set(video_urls))
# print len(video_urls)
# print video_urls
print time.ctime()
for video_url in video_urls:
    filename = video_url.rsplit('/')[-1]
    filepath = '/PycharmProjects/code1/spiders/budejie_mp4/'+filename
    urllib.urlretrieve(video_url,filepath)

print time.ctime()