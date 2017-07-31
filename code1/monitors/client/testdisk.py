#coding=utf-8
import psutil

disksusage = []
mountpoints = []
diskparts = psutil.disk_partitions()
for diskpart in diskparts:
    if 'rw' in diskpart[3]:
        mountpoints.append(diskpart[1])
        disksusage.append(psutil.disk_usage(diskpart[1]))
disks = dict(zip(mountpoints,disksusage))


