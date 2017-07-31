import salt.client

client = salt.client.LocalClient()

nodes = ['py2','node0','node1','node2']


# ret = client.cmd('*','service.status',['httpd'])
#
# print ret
# print ret['node1']
#
# ret = client.cmd('*','service.status',['nginx'])
#
# print ret
# print type(ret)
# print ret['node1']


# ret = client.cmd('*','service.show',['nginx'])
#
# print ret['py2']['ActiveState']
# for node in nodes:
#     for i in client.cmd(node,'network.ip_addrs'):
#         print i

ret = client.cmd('*','network.ipaddrs')
# print ret
for i in ret:
    if '192.168.174.144'  in ret[i]:
        hostname = i

ret = client.cmd(hostname,)


result =  client.cmd('py2','pkg.info_installed',['nginx'])['py2']
isinstance(result,dict)
False

isinstance(result,str)
True
