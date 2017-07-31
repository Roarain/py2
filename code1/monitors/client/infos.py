#coding=utf-8

import platform
import psutil
import os
import sys
import socket
import netifaces
import subprocess
import re

class systeminfo(object):
    def get_ip_address(self):
        # ip = []
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == ['lo','virbr0','virbr0-nic']:
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                for j in iface:
                    if '192.168.174' in j['addr']:
                        # ip.append(j['addr'])
                        return j['addr']
    def gethostname(self):
        return socket.gethostname()
    def getos(self):
        return platform.platform()
    def get_processor_name(self):
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
            command = "sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(command).strip()
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub(".*model name.*:", "", line, 1)
        return ""

class dynamicinfo(object):
    def getloadaveage(self):
        # la_1,la_5,la_15 = os.getloadavg()
        # return la_1,la_5,la_15
        la = os.getloadavg()
        return la
    def getcpu(self):
        cpustat = psutil.cpu_times_percent()
        return cpustat
    def getmemory(self):
        mem = psutil.virtual_memory()[0:4]
        return mem
    def getswap(self):
        swapmem = psutil.swap_memory()[0:4]
        return swapmem
    def getdisk(self):
        disksusage = []
        mountpoints = []
        diskparts = psutil.disk_partitions()
        for diskpart in diskparts:
            if 'rw' in diskpart[3]:
                mountpoints.append(diskpart[1])
                disksusage.append(psutil.disk_usage(diskpart[1]))
        return dict(zip(mountpoints,disksusage))
    # def getdisk_io(self):






if __name__ == '__main__':
    si = systeminfo()
    # ips = si.get_ip_address().remove('127.0.0.1')
    ips = si.get_ip_address()
    hostname = si.gethostname()
    osv = si.getos()
    cpumodel = si.get_processor_name()
    print 'IP Address are: %s' % (ips)
    print 'Hostname is: %s' % (hostname)
    print 'OS Version is: %s' % (osv)
    print 'CPU Model is: %s' % (cpumodel)


    di = dynamicinfo()
    la = di.getloadaveage()
    mem = di.getmemory()
    swapmem = di.getswap()
    disks = di.getdisk()
    cpustat = di.getcpu()[:]
    print 'System Load Average are: %s,%s,%s' % (la)
    print 'Mempry Usage are: %d,%d,%s,%d' % (mem)
    print 'Swap Usage are: %d,%d,%d,%d' % (swapmem)
    # print 'Disk Usage are:',disk
    print 'Disk Usage are: %s' % (disks)
    print 'CPU Stat are:' ,cpustat

