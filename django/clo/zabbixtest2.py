#coding:utf-8
import urllib2
import urllib
import json
import cookielib

url = "http://192.168.174.144/zabbix/api_jsonrpc.php"
login_url = "http://192.168.174.144/zabbix"
sid_url = "http://192.168.174.144/zabbix/zabbix.php?action=dashboard.view"


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#
#
headers = {
    "Content-Type":"application/json",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}
#
login_data = {
    "name" : "Admin",
    "password" : "zabbix",
    "autologin" : 1,
    "enter" : "Sign in",
}
#
login_json_data = json.dumps(login_data)

request = urllib2.Request(url=login_url,headers=headers,data=login_json_data)
response = urllib2.urlopen(request)
html_json = response.read()

# html = json.loads(html_json)

print "返回的html的内容是:" , html_json
#
# cookies = []
print "以下是cookie内容"
for index,cookie in enumerate(cj):
    print "[",index,"]",cookie
#     # cookies.append(cookie)
#     # print cookie.name,cookie.value,cookie.path
#     if "zbx_sessionid" == cookie.name:
#         sid = cookie.value[16:]
#         print cookie.value
# print sid

# data = {
#     "jsonrpc": "2.0",
#     "method": "user.login",
#     "params": {
#         "user": "Admin",
#         "password": "zabbix",
#         # "userData":True,
#     },
#     "id": 1,
# }
#
# data_json = json.dumps(data)
#
# request = urllib2.Request(url=url,headers=headers,data=data_json)
# response = urllib2.urlopen(request)
# html_json = response.read()
# html = json.loads(html_json)
# print html
# token = html["result"]
# print token
# sid = token[16:]
# print sid


# print cookies[0].value
# print type(cookies[0])
# print cookies
# print type(cookies)
# print len(cookies)
#
# request = urllib2.Request(url=sid_url,headers=headers)
# response = urllib2.urlopen(request)
# html_json = response.read()
# print html_json
# print "以下是cookie内容"
# for index,cookie in enumerate(cj):
#     print "[",index,"]",cookie
#
