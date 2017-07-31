#coding:utf-8
import salt.client

client = salt.client.LocalClient()

def service_controls(ip,service_name,control):
    cmd = 'service.' + control
    network_ipaddrs = client.cmd('*','network.ipaddrs')
    for hostname in network_ipaddrs:
        if ip in network_ipaddrs[hostname]:
            service_controler = client.cmd(hostname,cmd,[service_name])
    return service_controler

# sc = service_control('192.168.174.144','httpd','start')
# print sc




