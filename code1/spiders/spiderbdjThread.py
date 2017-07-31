#coding=utf-8
import urllib,urllib2,requests
import os,sys
from bs4 import BeautifulSoup
import time
import threading

# print time.ctime()
#
# domain = 'http://www.budejie.com/'
# main_url = 'http://www.budejie.com/video/1'
# midd_urls = []
# video_urls = []
#
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
#
# req = urllib2.Request(main_url,headers=headers)
# resp = urllib2.urlopen(req).read().decode('utf-8')
# soup = BeautifulSoup(resp,'html.parser')
# a_list = soup.find_all('a')
#
# for a in a_list:
#     try:
#         url = a['href']
#         # print url
#     except Exception as e:
#         pass
#     else:
#         if url.startswith('/detail'):
#             midd_urls.append(domain+url)
#     list(set(midd_urls))
# # print midd_url
# print time.ctime()
# for midd_url in midd_urls:
#     req = urllib2.Request(midd_url, headers=headers)
#     resp = urllib2.urlopen(req).read().decode('utf-8')
#     soup = BeautifulSoup(resp, 'html.parser')
#     a_list = soup.find_all('a')
#     for a in a_list:
#         try:
#             url = a['href']
#         except Exception as e:
#             pass
#         else:
#             if url.endswith('.mp4'):
#                 video_urls.append(url)
#         list(set(video_urls))
# # print len(video_urls)
# # print video_urls
# print time.ctime()
# for video_url in video_urls:
#     filename = video_url.rsplit('/')[-1]
#     filepath = '/PycharmProjects/code1/spiders/budejie_mp4/'+filename
#     urllib.urlretrieve(video_url,filepath)
#
# print time.ctime()

class Spider(object):
    def __init__(self,main_url='http://www.budejie.com/video'):
        self.main_url = 'http://www.budejie.com/video'
        self.domain = 'http://www.budejie.com/'
        self.midd_urls = []
        self.video_urls = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
        self.path = '/PycharmProjects/code1/spiders/budejie_thread_mp4'
    def get_a_list(self):
        req = urllib2.Request(self.main_url,headers=self.headers)
        resp = urllib2.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(resp,'html.parser')
        a_list = soup.find_all('a')
        return a_list
    def get_midd_urls(self):
        self.a_list = self.get_a_list(self.main_url)
        for a in self.a_list:
            try:
                url = a['href']
            except Exception as e:
                pass
            else:
                if url.startswith('/detail'):
                    self.midd_urls.append(self.domain + url)
        return list(set(self.midd_urls))

    def get_video_urls(self):
        for midd_url in self.midd_urls:
            self.a_list = self.get_a_list(midd_url)
            for a in self.a_list:
                try:
                    url = a['href']
                except Exception as e:
                    pass
                else:
                    if url.endswith('.mp4'):
                        self.video_urls.append(url)
        return list(set(self.video_urls))
    def save_path(self):
        'save path exist...' if os.path.exists(self.path) else os.makedirs(self.path)
    def get_mp4(self,video_url):
        filename = video_url.rsplit('/',1)[-1]
        filepath = self.path + '/' + filename
        urllib.urlretrieve(video_url,filepath)
        print '%s download done...' % (filepath)
if __name__ == '__main__':
    s = Spider()
    s.save_path()
    thread = []
    video_urls = s.get_video_urls()
    for video_url in video_urls:
        t = threading.Thread(target=s.get_mp4,args=(video_url,))
        t.start()
        thread.append(t)
    for th in thread:
        th.join()






