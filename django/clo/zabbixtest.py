#coding:utf-8

import urllib2
import urllib
import json

url = "http://192.168.174.144/zabbix/api_jsonrpc.php"

headers = {
    "Content-Type":"application/json",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix",
        # "userData":True,
    },
    "id": 1
}
data_json = json.dumps(data)

request = urllib2.Request(url=url,headers=headers,data=data_json)
response = urllib2.urlopen(request)
html_json = response.read()
html = json.loads(html_json)
print html
token = html["result"]
print token

data = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": "extend",
        # "output": ["host","hostid","name"],
        "filter": {
            "host": [
                # "Zabbix server",
                # "Linux server"
                "192.168.174.144",
                "192.168.174.146",
                "192.168.174.147",
                "192.168.174.148",
            ]
        }
    },
    "auth": token,
    "id": 1
}

data_json = json.dumps(data)
request = urllib2.Request(url=url,headers=headers,data=data_json)
response = urllib2.urlopen(request)
html_json = response.read()
html = json.loads(html_json)
results = html["result"]

print html
print results
print 'host.get 获取到的数据类型是: %s' %(type(results))
host_hostid = []

for i in results:
    d = {}
    d["host"] = i["host"]
    d["hostid"] = i["hostid"]
    d["name"] = i["name"]
    host_hostid.append(d)
    # print "host: %s,hostid: %s,name: %s" % (i["host"],i["hostid"],i["name"])
print host_hostid

'''
'''
data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": { "selectGraphs": ["graphid","name"],
                    "filter": {"host": '192.168.174.147'}},
        "auth": token,
        "id": 1
}

data_json = json.dumps(data)
request = urllib2.Request(url=url,headers=headers,data=data_json)
response = urllib2.urlopen(request)
html_json = response.read()
html = json.loads(html_json)
results = html["result"]
graphs = html["result"][0]["graphs"]
print "host.get.graphs获取到的数据是(111)" , graphs


'''
'''
data = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": "extend",
        "hostids": "10114",
        "search": {
            "key_": "system"
        },
        "sortfield": "name"
    },
    "auth": token,
    "id": 1
}
data_json = json.dumps(data)
request = urllib2.Request(url=url,headers=headers,data=data_json)
response = urllib2.urlopen(request)
html_json = response.read()
html = json.loads(html_json)
results = html["result"]
print 'item.get 获取到的数据类型是:' , type(results)
print 'item.get 获取到的数据是:',results
