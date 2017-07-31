#coding=utf-8
with open('monitor.html', 'wb+') as f:
    ipaddress = '192.168.174.142'
    f.write('<html>\n')
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
    f.write('<meta http-equiv="refresh" content="5">\n')
    f.write('<body style="background-color:yellow">\n')
    f.write('<h1 style="background-color:red;font-family:verdana;text-align:center">This is Roarains Monitor Console!</h1>\n')
    f.write('<hr></hr>\n')

    f.write('<h2>IP :%s</h2>\n' % (ipaddress))
    # f.write('<h2>hosname :%s</h2>' % (hostname))
    # f.write('<h2>OS :%s</h2>' % (osversion))
    # f.write('<h2>CPU:%s</h2>' % (CPUModel))

    f.write('<h5>This is Load Average Image. Refresh every 5 seconds. </h5>\n')
    f.write('<img src="img_loadaverage.png">\n')
    f.write('<h5>This is CPU Stat. Refresh every 5 seconds. </h5>\n')
    f.write('<img src="img_cpustat.png">\n')
    f.write('<h5>This is Swap Image. Refresh every 5 seconds. </h5>\n')
    f.write('<img src="img_swap.png">\n')
    f.write('</body>\n')
    f.write('</html>\n')
    f.close()