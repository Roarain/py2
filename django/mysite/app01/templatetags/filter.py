from django import template
import psutil

register = template.Library()

def transfer(data):
    data = data
    if data.isupper():
        return 'Data is: %s . Data Type is %s' %(data.lower(),type(data))
    elif data.islower():
        return 'Data is: %s . Data Type is %s' %(data.upper(),type(data))


def mem(arg):
    arg = arg
    mem = float(psutil.virtual_memory().total)
    if arg in 'g,G':
        return round(mem/pow(1024,3),2)
    elif arg in 'm,M':
        return round(mem / pow(1024, 2), 2)
    elif arg in 'k,K':
        return round(mem / pow(1024, 1), 2)
    else:
        return mem

register.filter('transfer',transfer)
register.filter('mem',mem)