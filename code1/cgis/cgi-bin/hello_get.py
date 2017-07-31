#!/usr/local/bin/python
import os
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')
age = form.getvalue('age')

print 'Content-type:text/html'
print
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>SaveFileCGI</title>'
print '</head>'
print '<body>'
print '<h1>Name Is:%s</h1><br>' %(name.title())
print '<h1>Age Is:%s</h1><br>' %(age)
print '</body>'
print '</html>'
