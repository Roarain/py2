#coding:utf-8

import urllib
import urllib2
import json
import cookielib

# cj = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# urllib2.install_opener(opener)
#
# login_url = "http://192.168.174.144/zabbix/index.php"
# login_url = "http://192.168.174.144/zabbix/zabbix.php?action=dashboard.view"
# network_url = "http://192.168.174.144/zabbix/charts.php?fullscreen=0&groupid=2&hostid=10113&graphid=581"
#
#
# headers = {
#     "Content-Type":"application/json",
#     "Referer" : "http://192.168.174.144/zabbix/index.php",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
# }
#
# login_data = {
#     "name":"Admin",
#     "password":"zabbix",
#     "autologin":"1",
#     "enter":"Sign in",
# }
#
# login_json_data = json.dumps(login_data)
#
# request = urllib2.Request(login_url,login_json_data,headers)
# response = urllib2.urlopen(request)
# html = response.read()
#
# print urllib.urlopen(network_url).read()


class ZabbixLogin(object):
    def __init__(self):
        self.login_url = "http://192.168.174.144/zabbix/zabbix.php?action=dashboard.view"
        # self.network_url = "http://192.168.174.144/zabbix/charts.php?fullscreen=0&groupid=2&hostid=10113&graphid=581"
        self.headers = {
            "Content-Type":"application/json",
            "Referer" : "http://192.168.174.144/zabbix/index.php",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        }
        self.login_data = {
            "name":"Admin",
            "password":"zabbix",
            "autologin":"1",
            "enter":"Sign in",
        }
        cj = self.cj_manage()
        self.loginzabbix()
        for index,cookie in enumerate(cj):
            print "[",index,"]",cookie
    def cj_manage(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        return cj
    def get_html(self):
        url = self.login_url
        data = self.login_data
        data_json = json.dumps(data)
        request = urllib2.Request(url=url, headers=self.headers, data=data_json)
        response = urllib2.urlopen(request)
        # html_json = response.read()
        # html = json.loads(html_json)
        html = response.read()
        return html
    def loginzabbix(self):
        html = self.get_html()
        if 'Monitoring' in html:
            login_zabbix_status = 'Success'
        else:
            login_zabbix_status = 'Faild'
        return (login_zabbix_status,self.cj_manage())
    def postrequest(self):
        network_url = "http://192.168.174.144/zabbix/charts.php?fullscreen=0&groupid=2&hostid=10113&graphid=581"
        postresult = urllib.urlopen(network_url).read()
        return postresult


if __name__ == '__main__':
    lz = ZabbixLogin()
    login_zabbix_status = lz.loginzabbix()
    print login_zabbix_status