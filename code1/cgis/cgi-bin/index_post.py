#!/usr/local/bin/python
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')
age = form.getvalue('age')

print 'Content-type:text/html'
print
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>PostCGI</title>'
print '</head>'
print '<body>'
print '<h1>post Request name is:%s</h1>' %(name.title())
print '<h1>post Request age is:%s</h1>' %(age)
print '</body>'
print '</html>'
