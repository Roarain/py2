import psutil
import MySQLdb
import datetime
import time



conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
cur = conn.cursor()

while True:
    sql = "insert into users_cpustat2(cpu_percent,curr_time) VALUES ('%s',now())" % (str(psutil.cpu_percent()))
    cur.execute(sql)
    time.sleep(2)
    conn.commit()

conn.close()


# class dynamicinfo(object):
#     def __init__(self,host,port,user,passwd,db):
#         self.host = host
#         self.port = port
#         self.user = user
#         self.passwd = passwd
#         self.db = db
#
#     def conndb(self,sql):
#         conn = MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db)
#         cur = conn.cursor()
#         data = cur.execute(sql)
#         conn.close()
#         return data
#
#     def getcpu(self):
#         cpu_percent = psutil.cpu_percent()
#         nowtime = 1
#         cpu_dict = 1
#         pass
