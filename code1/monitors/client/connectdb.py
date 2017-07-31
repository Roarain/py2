#coding=utf-8
import MySQLdb
import time

def conndb():
    conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
    cur = conn.cursor()