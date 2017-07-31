#coding=utf-8
import os
import MySQLdb
import time



conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='test')
cur = conn.cursor()


cur.execute('create table t_test (laid int PRIMARY KEY AUTO_INCREMENT,la1 float(5,2),la5 float(5,2),la15 float(5,2),curr datetime)')


while True:
    try:
        la = os.getloadavg()
        insert_sql = 'insert into t_test(la1,la5,la15,curr) values (%s,%s,%s,now())' % (la)
        select_sql = 'select * from t_test order by laid desc limit 1'
        # print la
        # print insert_sql
        # print type(la[0])
        cur.execute(insert_sql)
        conn.commit()
        cur.execute(select_sql)
        # print cur.fetchall()
        time.sleep(5)
    except Exception as e:
        print e
        conn.rollback()
