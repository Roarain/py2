#coding:utf-8

import psutil

class GetTotalDisk(object):
    def get_disk_part(self):
        disk_part = psutil.disk_partitions()
        return disk_part
    def get_mountpoint(self,disk_part):
        mountpoint = []
        for i in disk_part:
            if 'rw' in i.opts:
                mountpoint.append(i.mountpoint)
        return mountpoint
    def get_disk_total(self,mountpoint):
        total = []
        for i in mountpoint:
            total.append(int(psutil.disk_usage(i).total))
        return total
    def get_total(self,total):
        t = 0
        for i in range(len(total)):
            t += total[i]
        return t

if __name__ == '__main__':
    gtd = GetTotalDisk()
    disk_part = gtd.get_disk_part()
    mountpoint = gtd.get_mountpoint(disk_part)
    get_disk_total = gtd.get_disk_total(mountpoint)
    # print get_disk_total
    total = gtd.get_total(get_disk_total)
    # print total
    s_total =  str(total / pow(1000,3)) + 'G'
    print s_total