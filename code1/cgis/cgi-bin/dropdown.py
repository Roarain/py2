#!/usr/local/bin/python
import cgi

form = cgi.FieldStorage()

#clever   method
keys = form.keys()

print 'Content-type:text/html'
print
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>DropDownCGI</title>'
print '</head>'
print '<body>'
if keys:
    for key in keys:
        print '<h1>DropDown choice is:%s</h1>' %(form.getvalue(key))
else:
    print '<h1>DropDown has No Choice</h1>'
print '</body>'
print '</html>'
