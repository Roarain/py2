#!/usr/local/bin/python
import os
import cgi

form = cgi.FieldStorage()
filename = form.getvalue('filename')
upload_file_path = '/PycharmProjects/code1/cgis/upload/%s' % (filename)

with open(filename,'rb') as f:
    content = f.read()
with open(upload_file_path,'ab+') as f:
    f.write(content)

print 'Content-type:text/html'
print
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>SaveFileCGI</title>'
print '</head>'
print '<body>'
print '<h1>SourthFileNameIS:%s</h1><br>' %(filename)
print '<h1>UploadFileIS:%s</h1><br>' %(upload_file_path)
print '</body>'
print '</html>'
