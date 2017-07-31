#coding:utf-8

import paramiko

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(
#     hostname='192.168.174.144',
#     username='root',
#     password='1'
#
# )
# shell_cpu_model = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}'| uniq"
# stdin,stdout,stderr = ssh.exec_command(shell_cpu_model)
# cpu_info = stdout.readlines()[0]
#
# shell_cpu_count = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}' | wc -l"
# stdin,stdout,stderr = ssh.exec_command(shell_cpu_count)
# cpu_count = stdout.readlines()[0]
#
# print 'cpu_info type is:%s,data is: %s' % (type(cpu_info),cpu_info)
# print 'cpu_count type is:%s,data is: %s' % (type(cpu_count),cpu_count)


class ServerDetail(object):
    def __init__(self,ip,port,username,password):
        self.hostname = ip
        self.port = port
        self.username = str(username)
        self.password = str(password)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
    def get_info(self,shell_cmd):
        stdin, stdout, stderr = self.ssh.exec_command(shell_cmd)
        info = stdout.readlines()[0]
        return info
    def get_disk_info(self,shell_cmd):
        stdin, stdout, stderr = self.ssh.exec_command(shell_cmd)
        infos = stdout.readlines()
        sum = 0
        for i in range(len(infos)):
            sum += float(infos[i])
        return str(sum)


if __name__ == '__main__':
    sd = ServerDetail(ip='192.168.174.144',port=22,username='root',password='1')
    shell_cpu_model = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}'| uniq"
    shell_cpu_count = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}' | wc -l"
    shell_disk_info = "fdisk -l | grep 'Disk /dev/' | egrep 'vd|hd|sd' |awk -F ':|,| ' '{print $4}'"

    cpu_info = sd.get_info(shell_cpu_model)
    cpu_count = sd.get_info(shell_cpu_count)
    disk_info = sd.get_disk_info(shell_disk_info)

    print 'cpu_info type is:%s,data is: %s' % (type(cpu_info),cpu_info)
    print 'cpu_count type is:%s,data is: %s' % (type(cpu_count),cpu_count)
    print 'disk_info type is:%s,data is: %s' % (type(disk_info), disk_info)





