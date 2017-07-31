#coding:utf-8

import sys
import os
import commands

def nginxgrains():
    grains = {}
    mof = 60000
    try:
        getulimit = commands.getstatusoutput('source /etc/profile ; ulimit -n')
    except Exception as e:
        print e
    else:
        if getulimit[0] == 0 :
            mof = int(getulimit[1])
            grains['mof'] = mof
    return grains

# ng = nginxgrains()
# print ng