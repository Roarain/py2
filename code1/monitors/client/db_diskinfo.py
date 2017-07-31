import MySQLdb
import time
import infos

conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
cur = conn.cursor()

create_diskusage_table = 'create table IF NOT EXISTS t_diskusage (serverid int ,mountpoint nvarchar(50),total int,used int,free INT ,percent FLOAT(5,2),FOREIGN KEY serverid REFERENCES t_systeminfo(serverid))'
cur.execute(create_diskusage_table)

while True:
    try:
        disks = infos.disks
        insert_diskusage_table = 'insert into t_diskusage(la1,la5,la15,curr) values (%s,%s,%s,now())' % (la)
        select_diskusage_table = 'select * from t_diskusage order by laid desc limit 1'
        cur.execute(insert_diskusage_table)
        conn.commit()
        cur.execute(select_diskusage_table)
        time.sleep(5)
    except Exception as e:
        print e
        conn.rollback()

conn.close()