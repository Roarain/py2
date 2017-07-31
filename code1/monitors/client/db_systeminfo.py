import MySQLdb
import time
from infos import *

conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
cur = conn.cursor()

create_systeminfo_table = 'create table if not exists t_systeminfo (serverid int PRIMARY KEY AUTO_INCREMENT,ipaddress nvarchar(100),hostname nvarchar(50),osversion nvarchar(100),CPUModel nvarchar(80),curr datetime )'
try:
    cur.execute(create_systeminfo_table)
except Exception as e:
    conn.rollback()

'''
# error only once can be insert
while True:
    try:
        insert_systeminfo_table = 'insert into t_systeminfo(ipaddress,hostname,osversion,CPUModel) values (%s,%s,%s,%s)' % (infos.ips, infos.hostname, infos.osv, infos.cpumodel)
        select_systeminfo_table = 'select * from t_systeminfo'

        cur.execute(insert_systeminfo_table)
        cur.commit()
        cur.execute(select_systeminfo_table)
        # print cur.fetchall()
        time.sleep(5)
    except Exception as e:
        print e
        conn.rollback()

conn.close()
'''

try:
    si = systeminfo()
    ip = si.get_ip_address()
    hostname = si.gethostname()
    osv = si.getos()
    cpumodel = si.get_processor_name()

    insert_systeminfo_table = 'insert into t_systeminfo(ipaddress,hostname,osversion,CPUModel,curr) values ("%s","%s","%s","%s",now())' % (ip, hostname, osv, cpumodel)
    select_systeminfo_table = 'select * from t_systeminfo'

    cur.execute(insert_systeminfo_table)
    conn.commit()
    cur.execute(select_systeminfo_table)
    # print cur.fetchall()
except Exception as e:
    print e
    conn.rollback()

conn.close()


