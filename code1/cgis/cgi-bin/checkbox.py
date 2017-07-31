#!/usr/local/bin/python
import cgi

form = cgi.FieldStorage()
'''
#Stupid Method
if form.getvalue('cat'):
    choice_cat = form.getvalue('cat')
else:
    choice_cat = 'No Choice Cat'
if form.getvalue('pig'):
    choice_pig = form.getvalue('pig')
else:
    choice_pig = 'No Choice Pig'
'''

#clever   method
keys = form.keys()

print 'Content-type:text/html'
print
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<title>CheckBoxCGI</title>'
print '</head>'
print '<body>'
if keys:
    for key in keys:
        print '<h1>CheckBox choice is:%s</h1>' %(form.getvalue(key))
else:
    print '<h1>CheckBox has No Choice</h1>'
print '</body>'
print '</html>'
