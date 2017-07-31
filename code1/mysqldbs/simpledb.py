#coding=utf-8
'''
mysql -uroot -pabcd1234 -h 192.168.174.142 -P 3306
create table ,insert values,select tabel
'''
import MySQLdb

conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='dbtest')
cur = conn.cursor()

droptable = "drop table if EXISTS t1 "
ct = "create table t1 (id int,name nvarchar(20))"
it1 = "insert into t1 values (1,'cat')"
it2 = "insert into t1 values (2,'dog')"
st = "select id,name from t1"
dt = "delete from t1 where id = 1"

try:
    cur.execute(ct)
    cur.execute(st)
    print cur.fetchall()
    cur.execute(it1)
    cur.execute(it2)
    cur.execute(st)
    print cur.fetchall()
    cur.execute(dt)
    cur.execute(st)
    print cur.fetchall()
    conn.commit()
except:
    conn.rollback()
conn.close()
