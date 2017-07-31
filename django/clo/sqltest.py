import MySQLdb

#mysql -uroot -pabcd1234 -h 192.168.174.144 -P 3306 -D zabbix

conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='zabbix')
cur = conn.cursor()
sql = "select h.host,h.hostid,hg.groupid,i.itemid,i.name,g.graphid from hosts h ,items i ,graphs_items g ,hosts_groups hg where h.host = '%s' and h.hostid = i.hostid and i.itemid = g.itemid and i.name = '%s' limit 1" % ('192.168.174.144','Incoming network traffic on $1')
cur.execute(sql)
print cur.fetchall()