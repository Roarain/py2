import MySQLdb
import time
from infos import *

global data_cpustat

class cpustat(object):
    def get_cpustat(self):
        conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
        cur = conn.cursor()

        create_cpustat_table = 'create table if not exists t_cpustat (cpustatid int PRIMARY KEY AUTO_INCREMENT, serverid int,user float(5,2),system float(5,2),idle float(5,2),iowait float(5,2),curr_time datetime,foreign key(serverid) references t_systeminfo(serverid))'
        cur.execute(create_cpustat_table)

        try:
            cpustat = dynamicinfo().getcpu()
            insert_cpustat_table = 'insert into t_cpustat(serverid,user,system,idle,iowait,curr_time) values (1,"%s","%s","%s","%s",now())' % (cpustat[0], cpustat[2], cpustat[3], cpustat[4])
            select_cpustat_table = 'select cpustat.* from (select cpustatid,user,system,idle,iowait,curr_time from t_cpustat where serverid = 1 order by cpustatid desc limit 50) cpustat order by cpustatid'

            cur.execute(insert_cpustat_table)
            conn.commit()
            cur.execute(select_cpustat_table)
            data_cpustat = cur.fetchall()
            # for row in data_cpustat:
            #     return row
            return data_cpustat
        except:
            conn.rollback()
        # time.sleep(10)
        conn.close()
if __name__ == '__main__':
    cs = cpustat()
    print cs.get_cpustat()