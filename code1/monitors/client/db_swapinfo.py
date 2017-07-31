import MySQLdb
import time
from infos import *

global data_swap

'''
swapmem = dynamicinfo().getswap()
print swapmem

'''

class swapinfo(object):
    def get_swap(self):
        conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
        cur = conn.cursor()

        create_swapinfo_table = 'create table if not exists t_swapinfo (swapinfoid int PRIMARY KEY AUTO_INCREMENT, serverid int,total int,available int,used int,used_percent float(5,2),curr_time datetime,foreign key(serverid) references t_systeminfo(serverid))'
        cur.execute(create_swapinfo_table)

        try:
            swapmem = dynamicinfo().getswap()
            insert_swapinfo_table = 'insert into t_swapinfo(serverid,total,used,available,used_percent,curr_time) values (1,"%s","%s","%s","%s",now())' % (swapmem)
            # select_swapinfo_table = 'select swapinfo.* from (select swapinfoid,total,available,used,used_percent,curr_time from t_swapinfo where serverid = 1 order by swapinfoid desc limit 50) swapinfo order by swapinfoid'
            select_swapinfo_table = 'select swapinfoid,total,available,used,used_percent,curr_time from t_swapinfo order by swapinfoid desc limit 1'

            cur.execute(insert_swapinfo_table)
            conn.commit()
            cur.execute(select_swapinfo_table)
            data_swap = cur.fetchall()
            return data_swap
            # for row in data_swap:
            #     return row
        except:
            conn.rollback()
        # time.sleep(10)
        conn.close()
if __name__ == '__main__':
    ss = swapinfo()
    print ss.get_swap()