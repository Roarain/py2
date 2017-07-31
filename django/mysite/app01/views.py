#coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.template import Context,Template

from app01 import models

from app01 import forms

# Create your views here.

def test(request):
    t = Template('My name is {{ name }},age is {{ age }}')
    c = Context({'name':'nh','age':18})
    return HttpResponse(t.render(c))

def index(request):
    html_content = 'This is First Django template language Test'
    # hostname = '<h1 style="color: yellow"> host1-linux </h1>'
    # hostname = 'host1-linux'
    host_lists = [{'hostname':'node1'},{'hostname':'node2'},{'hostname':'node3'},{'hostname':'node4'},{'hostname':'node5'},{'hostname':'node6'}]
    # return render(request,'index.html',{'html1':html_content,'hostname':hostname})
    return render(request, 'index.html', {'html1': html_content,'host_list': host_lists})

    # return HttpResponse("<h1>Index Of Roarain's First Django App</h1>")
def articles_year(request,year):
    print 'year:%s' %year
    return HttpResponse('<h1> articles is %s' % year)
def articles_year_month(request,year,month):
    print 'year is %s month is %s' % (year,month)
    return HttpResponse('<h1> article ')
def article_find(request,month,year):
    print 'year is %s month is %s' % (year, month)
    return HttpResponse('<h1> article year:%s month:%s' % (year,month))
def host(request):
    hostname = request.GET.get('hostname')
    # id = request.GET.get('id')
    id = request.GET['id']
    print request.GET['id'],request.GET['hostname']
    return HttpResponse('<h1> hostname:%s id:%s' % (hostname,id))

def register(request):
    if request.POST and request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print 'User is %s. Passwd is %s.'
        resp_html = 'User %s Register Success...' % (username)
        return HttpResponse(resp_html)
    return render(request,'Register.html')

def add_book(request):
    book_list = models.Book.objects.all()
    publisher_list = models.Publisher.objects.all()
    author_list = models.Author.objects.all()
    if request.method == 'POST' and request.POST:
        book_name = request.POST.get('book_name')
        print '书名: %s' % (book_name)
        publisher = request.POST.get('publisher')
        print '出版社ID: %s' % (publisher)
        publish_date = request.POST.get('date')
        print '出版日期: %s' % (publish_date)
        author = request.POST.getlist('author')
        print '作者ID: %s' % (author)

        new_book = models.Book(
            name = book_name,
            publisher_id = publisher,
            publish_date = publish_date
        )
        new_book.save()
        new_book.author.add(*author)
        return HttpResponse('New Book %s Add Success...' % (book_name))

    return render(request,'add_book.html',{'book_list':book_list,'publisher_list':publisher_list,'author_list':author_list})

def book_form(request):
    form = forms.BookForm()
    publisher_list = models.Publisher.objects.all()
    if request.method == 'POST':
        print request.POST
        form = forms.BookForm(request.POST)
        if form.is_valid():
            # print 'BookForm data is: ',form.cleaned_data
            print form.cleaned_data
            models.Book.objects.create(**form.cleaned_data)
            return HttpResponse('BookForm Add Book success...')
        else:
            print form.errors
            return HttpResponse(form.errors)
    return render(request,'book_form.html',{'book_form':form,'publisher_list':publisher_list})


def book_model_form(request):
    form = forms.BookModelForm()
    if request.method == 'POST':
        print 'Request Post Data is: ',request.POST
        form = forms.BookModelForm(request.POST)
        if form.is_valid():
            print 'BookForm data is: ',form.cleaned_data
            form.save()
            return HttpResponse('BookModelForm Add Book %s success...' % (form.cleaned_data.get('name')) )
        else:
            print 'Form Error is: ',form.errors
            return HttpResponse(form.errors)

    return render(request,'book_model_form.html',{'form':form})


def filter(request,data):
    filter_html = '<h1> This is Filter Test Page ...</h1>'
    transfer_data = data
    print 'transfer_data is %s' % (transfer_data)
    return render(request,'filter.html',{'filter_html':filter_html,'transfer_data':transfer_data})

def mem(request,arg):
    arg = arg
    print 'Arg is: %s' % (arg)
    return render(request,'mem.html',{'arg':arg})