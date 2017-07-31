#coding:utf-8
import MySQLdb
import time

global data_basicinfo
conn = MySQLdb.connect(user='root',passwd='abcd1234',host='192.168.174.142',port=3306,db='monitordb')
cur = conn.cursor()

select_basicinfo_sql = 'select ipaddress,hostname,osversion,CPUModel from t_systeminfo where serverid = 1'
try:
    cur.execute(select_basicinfo_sql)
    data_basicinfo = cur.fetchall()[0]
except Exception as e:
    conn.rollback()
with open('monitor.html', 'wb+') as f:
        f.write('<html>\n')
        f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        f.write('<meta http-equiv="refresh" content="5">\n')
        f.write('<body style="background-color:yellow">\n')
        f.write(
            '<h1 style="background-color:red;font-family:verdana;text-align:center">This is Roarains Monitor Console!</h1>\n')
        f.write('<hr></hr>\n')

        f.write('<h4>IP :%s</h4>\n' % (data_basicinfo[0]))
        f.write('<h4>hosname :%s</h4>\n' % (data_basicinfo[1]))
        f.write('<h4>OS :%s</h4>\n' % (data_basicinfo[2]))
        f.write('<h4>CPU:%s</h4>\n' % (data_basicinfo[3]))

        # f.write('<h5>This is Load Average Image. Refresh every 5 seconds. </h5>\n')
        # f.write('<img src="img_loadaverage.png">\n')
        # f.write('<h5>This is CPU Stat. Refresh every 5 seconds. </h5>\n')
        # f.write('<img src="img_cpustat.png">\n')
        f.write('<table border="1">')
        f.write('<tr>')
        f.write('  <th>This is Load Average Image. Refresh every 5 seconds. </th>')
        f.write('  <th>This is CPU Stat. Refresh every 5 seconds. </th>')
        f.write('</tr>')
        f.write('<tr>')
        f.write('  <td><img src="img_loadaverage.png"></td>')
        f.write('  <td><img src="img_cpustat.png"></th></td>')
        f.write('</tr>')
        f.write('</table>')

        f.write('<h5>This is Swap Image. Refresh every 5 seconds. </h5>\n')
        f.write('<img src="img_swap.png">\n')
        f.write('</body>\n')
        f.write('</html>\n')
        f.close()
conn.close()
