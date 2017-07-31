#coding:utf-8

from django.core.paginator import Paginator
itemlist = ['a','b','c','d','e','f','g']
p = Paginator(itemlist,2)
# print p.num_pages
for i in range(1,p.num_pages+1):
    if p.page(i).has_previous():
        print 'Page %d 有上一页,上一页是 %d' % (i,p.page(i).previous_page_number())
    else:
        print 'Page %d 是第一页' % (i)
    if p.page(i).has_next():
        print 'Page %d 有下一页,下一页是 %d' % (i, p.page(i).next_page_number())
    else:
        print 'Page %d 是最后一页' % (i)

    print p.page(i).object_list
    print '----------------'