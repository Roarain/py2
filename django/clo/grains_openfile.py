#coding:utf-8

import os
import sys
import commands
import salt.client


def grains_openfile():
    grains = {}
    _open_files = 65536
    try:
        getulimit = commands.getstatusoutput('source /etc/profile ; ulimit -n')
    except Exception as e:
        print e
    else:
        if getulimit[0] == 0:
            _open_files = getulimit[1]
            grains['max_open_file'] = _open_files
    return grains

# go = grains_openfile()
# print go