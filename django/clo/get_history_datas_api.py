#coding:utf-8

import json
import urllib2
import urllib


class ZabbixAPI(object):
    def __init__(self,ip):
        self.url = "http://192.168.174.144/zabbix/api_jsonrpc.php"
        self.username = "Admin"
        self.password = "zabbix"
        self.headers = {
            "Content-Type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            }
        self.token = self.get_token()
        self.memory_keys = ["vm.memory.size[total]","vm.memory.size[available]"]
        self.cpu_keys = ["system.cpu.load[percpu,avg1]","system.cpu.load[percpu,avg5]","system.cpu.load[percpu,avg15]"]
        self.fs_keys = ["vfs.fs.size[/,pfree]","vfs.fs.size[/home,pfree]"]
        self.swap_keys = ["system.swap.size[,pfree]"]
        self.net_keys = ["net.if.in[eno16777736]","net.if.out[eno16777736]"]
        self.keys = self.memory_keys + self.cpu_keys + self.fs_keys + self.swap_keys + self.net_keys
        self.host = ip
        self.limit_number = 10
        self.historyids = (0,3)
    def get_html(self,data):
        data_json = json.dumps(data)
        request = urllib2.Request(url=self.url, headers=self.headers, data=data_json)
        response = urllib2.urlopen(request)
        html_json = response.read()
        html = json.loads(html_json)
        return html
    def get_token(self):
        data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": "Admin",
                    "password": "zabbix",
                    "userData": True,
                    },
                "id": 1
            }
        html = self.get_html(data)
        token = html["result"]["sessionid"]
        return token
    def get_hostid(self):
        data = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    # "output": "extend",
                    "output": ["host","hostid","name"],
                    "filter": {
                        "host": self.host,
                    }
                },
                "auth": self.token,
                "id": 1
            }
        html = self.get_html(data)
        hosts_infos = html["result"]
        hostid = hosts_infos[0]["hostid"]
        return hostid
    def get_itemid(self,key):
        hostid = self.get_hostid()
        data = {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": "extend",
                    "hostids": hostid,
                    "search": {
                        "key_": key,
                    },
                    "sortfield": "name"
                },
                "auth": self.token,
                "id": 1
            }
        items = self.get_html(data)
        if items["result"]:
            if items["result"][0]:
                itemid = items["result"][0]["itemid"]
        else:
            itemid = ''
        return itemid

    def get_historys(self,itemid,historyid):
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": historyid,
                "itemids": itemid,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 60,
            },
            "auth": self.token,
            "id": 1
        }
        historys = self.get_html(data)["result"]
        return historys


#
# if __name__ == '__main__':
#
#     zapi = ZabbixAPI('192.168.174.144')
#     keys = zapi.keys
#     historyids = zapi.historyids
#     # hostid = zapi.get_hostid()
#     # print hostid
#     # html = zapi.get_itemid()
#     # print html
#     # historys = zapi.get_historys()
#     # print historys
#     # '''
#     key_historys_dict = {}
#
#     for key in keys:
#         itemid = zapi.get_itemid(key)
#         for historyid in historyids:
#             historys = zapi.get_historys(itemid,historyid)
#             if historys != []:
#                 if 'vfs.fs.size' in key or 'swap' in key or 'vm.memory.size[total]' in key:
#                 # if 'vfs.fs.size' in key or 'swap' in key:
#                     historys = historys[0:1]
#                 else:
#                     pass
#                 for history in historys:
#                     history.pop('itemid')
#                     history.pop('ns')
#                 key_historys_dict[key] = historys
#             else:
#                 pass
#     print key_historys_dict
#     # '''

