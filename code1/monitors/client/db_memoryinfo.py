import MySQLdb
import time
from infos import *

class memoryinfo(object):
    def __init__(self):
        pass

    def sql_mem(self):
        conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='dbtest')
        cur = conn.cursor()

        create_memoryinfo_table = 'create table if not exists t_memoryinfo (meminfoid int PRIMARY KEY AUTO_INCREMENT, serverid int,total int,available int,used int,used_percent float(5,2),curr_time datetime,foreign key(serverid) references t_systeminfo(serverid))'
        create_swapinfo_table = 'create table if not exists t_swapinfo (swapinfoid int PRIMARY KEY AUTO_INCREMENT, serverid int,total int,available int,used int,used_percent float(5,2),curr_time datetime,foreign key(serverid) references t_systeminfo(serverid))'

        cur.execute(create_memoryinfo_table)
        cur.execute(create_swapinfo_table)


        # insert_memoryinfo_table = 'insert into t_memoryinfo(serverid,total,available,used_percent,used,curr_time) values (1,"%s","%s","%s","%s",now())' % (mem)
        # select_memoryinfo_table = 'select memoryinfo.* from (select meminfoid,,total,available,used,used_percent,curr_time from t_memoryinfo where serverid = 1 order by meminfoid desc limit 50) memoryinfo order by meminfoid'
        #
        # insert_swapinfo_table = 'insert into t_swapinfo(serverid,total,used,available,used_percent,curr_time) values (1,"%s","%s","%s","%s",now())' % (swapmem)
        # select_swapinfo_table = 'select swapinfo.* from (select swapinfoid,,total,available,used,used_percent,curr_time from t_swapinfo where serverid = 1 order by swapinfoid desc limit 50) swapinfo order by swapinfoid'

        while True:
            try:
                mem = dynamicinfo().getmemory()
                insert_memoryinfo_table = 'insert into t_memoryinfo(serverid,total,available,used_percent,used,curr_time) values (1,"%s","%s","%s","%s",now())' % (mem)
                select_memoryinfo_table = 'select memoryinfo.* from (select meminfoid,,total,available,used,used_percent,curr_time from t_memoryinfo where serverid = 1 order by meminfoid desc limit 50) memoryinfo order by meminfoid'

                cur.execute(insert_memoryinfo_table)
                conn.commit()
                cur.execute(select_swapinfo_table)
                data_mem = cur.fetchall()
            except:
                conn.rollback()
            try:
                swapmem = dynamicinfo.getswap()
                insert_swapinfo_table = 'insert into t_swapinfo(serverid,total,used,available,used_percent,curr_time) values (1,"%s","%s","%s","%s",now())' % (swapmem)
                select_swapinfo_table = 'select swapinfo.* from (select swapinfoid,,total,available,used,used_percent,curr_time from t_swapinfo where serverid = 1 order by swapinfoid desc limit 50) swapinfo order by swapinfoid'

                cur.execute(insert_swapinfo_table)
                conn.commit()
                cur.execute(select_swapinfo_table)
                data_swap = cur.fetchall()
            except:
                conn.rollback()
            time.sleep(10)
        return data_mem
        return data_swap
        conn.close()
