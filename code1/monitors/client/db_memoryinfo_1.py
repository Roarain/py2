import MySQLdb
import time
import infos

conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='dbtest')
cur = conn.cursor()

create_memoryinfo_table = 'create table t_memoryinfo (total int,available int,used int,used_percent float(5,2),curr_time datetime)'
insert_memoryinfo_table = 'insert into t_memoryinfo values (%d,%d,%d,%d,now())' % (infos.mem)
select_memoryinfo_table = 'select max(curr_time) from t_memoryinfo'

create_swapinfo_table = 'create table t_swapinfo (total int,available int,used int,used_percent float(5,2),curr_time datetime)'
insert_swapinfo_table = 'insert into t_swapinfo values (%d,%d,%d,%d,now())' % (infos.swapmem)
select_swapinfo_table = 'select max(curr_time) from t_swapinfo'

cur.execute(create_memoryinfo_table)

while True:
    try:
        cur.execute(insert_memoryinfo_table)
        memoryinfo = cur.execute(select_swapinfo_table)
        print cur.fetchall()
        cur.commit()
    except:
        conn.rollback()
    try:
        cur.execute(insert_swapinfo_table)
        swapinfo = cur.execute(select_swapinfo_table)
        print cur.fetchall()
        cur.commit()
    except:
        conn.rollback()
    time.sleep(10)

conn.close()