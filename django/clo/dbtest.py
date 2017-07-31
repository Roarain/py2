#coding:utf-8

import MySQLdb

def execute_select_one_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0]
    conn.commit()
    conn.close()

def service_list(server_id):
    ip_from_server_id_sql = "select s.ip ,s.port from clocmdb_server s ,clocmdb_serverdetail sd where s.id =  sd.server_id  and sd.server_id ='%s' " % (server_id)
    ip,port = execute_select_one_sql(ip_from_server_id_sql)
    # print 'ip is: ', ip
    return ip

sl = service_list(9)
print sl