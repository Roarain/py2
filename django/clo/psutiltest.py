#coding:utf-8

import psutil
import datetime

pids = psutil.pids()
# print pid
# print len(pid)
# print type(pid)

# if 104225 in pids:
#     p = psutil.Process(104225)
#     print p.name()
#     print p.pid
#     print p.ppid()
#     print p.memory_full_info()
#     print p.cwd()
#     print p.exe()
result = []
for pid in pids:
    p = psutil.Process(pid)
    # if p.name().startswith('nginx') or p.name().startswith('salt'):
    if p.name().startswith('nginx') or p.name().startswith('redis'):
        (name,cmdline) = p.name(),p.cmdline()
        print p.create_time()

        print datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        result.append((name,cmdline))

func = lambda x,y:x if y in x else x + [y]

print reduce(func, [[], ] + result)