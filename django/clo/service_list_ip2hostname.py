#coding:utf-8
import salt.client

client = salt.client.LocalClient()
#列出要检测的系统yum安装的服务名称
services = ['nginx','salt-master','salt-minion','httpd','redis']

#由于saltstack操作是根据主机名区分，故:
#根据传递来的ip获取saltstack的主机名,再通过saltstack自带api接口获取服务是否安装以及服务的状态
#将以上信息以2级字典形式保存并传递回views.py相应函数
#结果如下
#{'salt-minion': {'status': 'active', 'installed': 'Y'}, 'nginx': {'status': '', 'installed': 'N'}, 'redis': {'status': 'inactive', 'installed': 'Y'}, 'salt-master': {'status': 'active', 'installed': 'Y'}, 'httpd': {'status': 'inactive', 'installed': 'Y'}}
def service_status(ip):
    services_info = {}
    network_ipaddrs = client.cmd('*','network.ipaddrs')
    for hostname in network_ipaddrs:
        if ip in network_ipaddrs[hostname]:
            for service in services:
                services_info[service] = {}
                pkg_installed = client.cmd(hostname, 'pkg.info_installed', [service])[hostname]
                if isinstance(pkg_installed,dict) is True:
                    services_info[service]['installed'] = 'Y'
                    pkg_status = client.cmd(hostname,'service.show',[service])[hostname]['ActiveState']
                    services_info[service]['status'] = pkg_status
                elif isinstance(pkg_installed,str) is True:
                    services_info[service]['installed'] = 'N'
                    services_info[service]['status'] = ''
    return services_info

# ss = service_status('192.168.174.144')
# # for info in ss:
# #     print ss[info]
# print ss
#
# result = []
#
# for i in ss:
#     dicts = ss[i]
#     dicts['service'] = i
#     result.append(dicts)
# print result



