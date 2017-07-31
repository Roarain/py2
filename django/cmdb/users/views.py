# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib import auth
from . import models
import hashlib
import time
import datetime
from django.http import JsonResponse
import MySQLdb
import platform
import cpuinfo
import psutil
from gettotaldisk import GetTotalDisk
from serverdetail import ServerDetail
from genrandom import GenerateRandom
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import cStringIO, string, os, random
import gencaptcha


# Create your views here.


'''
Through the parameter  <autojump>  to determine the jump page.
'''
def autojump(request):
    return render(request,'autojump.html',locals())

def hash_password(password):
    hash_md5 = hashlib.md5()
    hash_md5.update(password)
    password = hash_md5.hexdigest()
    return password


def valid_login(func):
    def inner(request,*args,**kwargs):
        try:
            request.session.get('session_username')
        except Exception as e:
            print 'Session Error,Please Login.'
            return render(request, 'signin.html', locals())
        else:
            session_username = request.session.get('session_username')
            if models.User.objects.filter(username=session_username):
                return func(request,*args,**kwargs)
            else:
                return render(request,'signin.html',locals())
    return inner


'''
Use Decorator to verify login
'''
@valid_login
def index(request):
    session_username = request.session.get('session_username')
    return render(request,'index.html',locals())


'''
Did not Use Decorator
'''
# def index(request):
#     print '%s Cookie is: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'),request.COOKIES['username'])
#     if request.session.get('username'):
#         username = request.session.get('username')
#         print '%s Session is: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'),username)
#         return render(request,'index.html',locals())
#     else:
#         return HttpResponseRedirect('/users/login')


'''
set cookie cookie_username
set session session_username
'''
def login(request):
    if request.method == 'POST' and request.POST:
        print request.POST
        username = request.POST.get('username')
        password = hash_password(request.POST.get('password'))
        code = request.POST.get('code')
        if code == request.session['captcha']:

            if models.User.objects.filter(username=username,password=password):
                response = HttpResponseRedirect('/users/index')
                response.set_cookie('cookie_username',username)

                request.session['session_username'] = username
                return response
            else:
                autojump = 'login_faild'
                print 'User or Password error,Please reLogin.'
                return render(request,'autojump.html',{'autojump':autojump})

    return render(request,'signin.html',locals())



def captcha(request):
    gc = gencaptcha.GenCaptcha()
    img,img_char = gc.save_to_mem()
    request.session['captcha'] = img_char.replace(' ','')
    return HttpResponse(img, 'image/jpeg')



'''
Determin whether user is duplicate when regist new user.
'''
def check_duplicate_user(username):
    resp_data = {'data':'','status':'','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    try:
        userinfo = models.User.objects.get(username=username)
        resp_data['data'] = username
        resp_data['status'] = 'success'
    except Exception as e:
        print e
        resp_data['status'] = 'error'
    return resp_data


def check_regist_duplicate_user(request):
    if request.method == 'POST' and request.POST:
        # username = request.POST.get('username')
        username = request.POST['username']
        return JsonResponse(check_duplicate_user(username))
    else:
        return JsonResponse({'data':'','status':'','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def register(request):
    if request.method == 'POST' and request.POST:
        print request.POST
        username = request.POST.get('username')
        password_ori = request.POST.get('password')
        password = hash_password(password_ori)
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not models.User.objects.filter(username=username):
            models.User.objects.create(username=username, password=password, email=email, phone=phone)
            autojump = 'regist_success'
            return render(request, 'autojump.html', {'autojump': autojump, 'username': username})
        elif models.User.objects.filter(username=username):
            print 'Username: %s is already exist...' % (username)
            autojump = 'regist_faild'
            return render(request,'autojump.html',{'autojump':autojump,'username':username})

    return render(request,'signup.html',locals())

@valid_login
def server_register(request):
    session_username = request.session.get('session_username')
    if request.method == 'POST' and request.POST:
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        print 'variable ip is: %s' %(type(ip))
        if not models.Server.objects.filter(ip=ip,port=port):

            username = request.POST.get('username')
            password_ori = request.POST.get('password')
            password = hash_password(password_ori)
            protocal = request.POST.get('protocal')
            isActive = 'N'

            models.Server.objects.create(ip=ip, port=port, username=username, password=password, protocal=protocal,isActive=isActive)

            try:
                server_id_sql = "select base_ptr_id from users_server where ip = '%s' " % (ip)
                server_id = execute_select_sql(server_id_sql)
                print 'server_id type is: %s' % (type(server_id))
                user_id_sql = "select base_ptr_id from users_user where username = '%s' " % (session_username)
                user_id = execute_select_sql(user_id_sql)
                print 'user_id type is: %s' % (type(user_id))
            except Exception as e:
                print e
            else:
                models.UserServer.objects.create(user_id=user_id,server_id=server_id)

                try:
                    sd = ServerDetail(ip=ip,port=int(port),username=username,password=password_ori)
                    # sd = ServerDetail(ip=ip,port=22,username=username,password=password_ori)

                    shell_cpu_info = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}'| uniq"
                    shell_cpu_count = "grep 'model name' /proc/cpuinfo |awk -F ':' '{print $2}' | wc -l"
                    shell_os_info = "uname -a"
                    shell_mem_info = "free -m | grep Mem |awk '{print $2}'"

                    shell_disk_info = "fdisk -l | grep 'Disk /dev/' | egrep 'vd|hd|sd' |awk -F ':|,| ' '{print $4}'"

                    cpu_info = sd.get_info(shell_cpu_info)
                    cpu_count = sd.get_info(shell_cpu_count)
                    os_info = sd.get_info(shell_os_info)
                    mem_info = sd.get_info(shell_mem_info) + 'M'

                    disk_info = sd.get_disk_info(shell_disk_info) + 'G'
                except Exception as e:
                    print e
                else:
                    models.ServerDetail.objects.create(server_id=server_id,os_info=os_info,cpu_info=cpu_info,cpu_count=cpu_count,mem_info=mem_info,disk_info=disk_info)

            return HttpResponseRedirect('/users/server_list/')

        elif models.Server.objects.filter(ip=ip,port=port):
            print 'Server %s:%s has been register...' % (ip,port)
            return HttpResponse('Server %s has been register...' % (ip))
            # return render(request,'server_register.html',locals())
    return render(request,'server_register.html',locals())
    # return HttpResponseRedirect('/users/server_register/')

@valid_login
def server_list(request):
    session_username = request.session.get('session_username')
    servers_sql = "select * from users_server where base_ptr_id in (select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s'))" % (session_username)
    servers = execute_select_all_sql(servers_sql)
    # server_id_sql = "select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s')" % (session_username)
    # server_id = execute_select_sql(server_id_sql)
    print 'servers type is: %s' % (type(servers))
    print servers
    return render(request,'server_list.html',locals())


@valid_login
def server_list_page(request,pageid):
    session_username = request.session.get('session_username')
    pageid = int(pageid)
    numid = 2
    from_num = (pageid - 1) * 2

    servers_sql = "select * from users_server where base_ptr_id in (select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s')) limit %d,%d " % (session_username,from_num,numid)
    servers = execute_select_all_sql(servers_sql)

    servercount_sql = "select count(*) from users_server where base_ptr_id in (select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s'))" % (session_username)
    servercount = int(execute_select_all_sql(servercount_sql)[0][0])

    # server_id_sql = "select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s')" % (session_username)
    # server_id = execute_select_sql(server_id_sql)
    print 'servers type is: %s' % (type(servers))
    print servers
    print servercount
    return render(request,'server_list.html',locals())

@valid_login
def server_search(request):
    session_username = request.session.get('session_username')
    if request.method == 'POST' and request.POST:
        ip = request.POST.get('ip','')
        port = request.POST.get('port','')

        search_sql = "select * from users_server where base_ptr_id in (select server_id from users_userserver where user_id = (select base_ptr_id from users_user where username = '%s')) " % (session_username)
        ip_sql = "and ip like '%%%s%%' " % (ip)
        port_sql = "and port like '%%%s%%' " % (port)
        if len(ip) > 0 and len(port) > 0:
            search_sql =  search_sql + ip_sql + port_sql
        elif len(ip) > 0 and len(port) == 0:
            search_sql = search_sql + ip_sql
        elif len(ip) == 0 and len(port) > 0:
            search_sql = search_sql + port_sql
        else:
            search_sql = search_sql + ip_sql + port_sql
        servers = execute_select_all_sql(search_sql)
    return render(request, 'server_search.html', locals())
    # return JsonResponse({'data':'','status':'','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})



def sqltest(request):
    sql = "select base_ptr_id from users_server where ip = '192.168.1.1' "
    return HttpResponse(execute_select_sql(sql))

def execute_select_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0][0]
    conn.close()

def execute_insert_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def execute_select_all_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    conn.close()

def execute_select_one_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0]
    conn.commit()
    conn.close()

def execute_delete_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def execute_update_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='cmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

# def add(*args):
#     sum = ''
#     for i in args:
#         sum += i
#     return sum


# def get_disk_info():
#     gtd = GetTotalDisk()
#     disk_part = gtd.get_disk_part()
#     mountpoint = gtd.get_mountpoint(disk_part)
#     get_disk_total = gtd.get_disk_total(mountpoint)
#     # print get_disk_total
#     total = gtd.get_total(get_disk_total)
#     # print total
#     disk_info = str(total / pow(1000, 3)) + 'G'
#     return  disk_info

# def server_detail(request):
#     dist = platform.dist()
#     os_info = dist[0].capitalize()+dist[1].capitalize()+dist[2].capitalize()
#     cpu_info = cpuinfo.get_cpu_info().get('brand')
#     cpu_count = cpuinfo.get_cpu_info().get('count')
#     mem = psutil.virtual_memory().total / pow(1024,2)
#     mem_info = str(mem)+'M'
#     disk_info = get_disk_info()
#     # return render(request,'server_detail.html',locals())

# @valid_login
def server_detail(request,ip):
    session_username = request.session.get('session_username')
    ip = str(ip)
    server_detail_sql = "select s.ip ,s.port,s.username,s.protocal,s.isActive,sd.os_info,sd.cpu_info,sd.cpu_count,sd.mem_info,sd.disk_info from users_server s ,users_serverdetail sd where s.base_ptr_id = sd.server_id and sd.server_id = (select base_ptr_id from users_server where ip = '%s')" % (ip)
    server_details = execute_select_one_sql(server_detail_sql)
    print 'server_details data is: ' ,server_details
    return render(request,'server_detail.html',locals())

# @valid_login
def server_delete(request,ip):
    session_username = request.session.get('session_username')
    # if ip:
    ip = str(ip)
    server_delete_sql_1 = "delete from users_serverdetail where server_id = (select base_ptr_id from users_server where ip = '%s')" % (ip)
    server_delete_sql_2 = "delete from users_server where ip = '%s'" % (ip)
    execute_delete_sql(server_delete_sql_1)
    execute_delete_sql(server_delete_sql_2)
    return HttpResponseRedirect('/users/server_list/')
    # return render(request,'server_list.html',locals())



# def check_regist_duplicate_user(request):
#     if request.method == 'POST' and request.POST:
#         # username = request.POST.get('username')
#         username = request.POST['username']
#         return JsonResponse(check_duplicate_user(username))
#     else:
#         return JsonResponse({'data':'','status':'','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def check_isActive(request):
    if request.method == 'POST' and request.POST:
        ip = request.POST.get['ip']
        isActive = request.POST.get['isActive']
        try:
            isActive_update_sql = "update users_server set isActive = '%s' where ip = '%s'" % (isActive,ip)
            execute_update_sql(isActive_update_sql)
        except Exception as e:
            print e
            isActive = 1
            return JsonResponse({'data':''})
        else:
            return
    pass


def server_monitor(request):
    # return HttpResponseRedirect('/users/server_monitor/')
    return render(request,'server_monitor.html',locals())


def password_forget(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        if models.User.objects.filter(username=username,email=email):
            pfs = password_forget_sendmail()

    return render(request,'password_forget.html',locals())

def sendemail(request):
    emailcode = GenerateRandom().gen_random()
    msg='您通过邮箱找回密码的验证码是:%s,五分钟内有效.' % (emailcode)
    send_mail('密码找回',
            '?',
            'sysalarm@clo.com.cn',
            ['wangxiaoyu@clo.com.cn',],
            html_message=msg)
    return HttpResponse('Send Email OK')

def password_forget_sendmail(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        if models.User.objects.filter(username=username, email=email):
            # generate email code
            emailcode = GenerateRandom().gen_random()
            # save email code to Mysql
            try:
                models.SendCodes.objects.create(username=username, email=email, emailcode=emailcode)
            except Exception as e:
                print e
                print 'email code save to mysql faild'
                return HttpResponse('email code save to mysql faild')
            else:
                # send email
                msg = '您通过邮箱找回密码的验证码是:%s,五分钟内有效.' % (emailcode)
                subject = '密码找回'
                from_email = 'sysalarm@clo.com.cn'
                to_email = [email,]
                try:
                    send_mail(subject,msg,from_email,to_email)
                except Exception as e:
                    print 'Send Email Faild'
                    print e
                    return JsonResponse({'sendemailstatus':'Error','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                else:
                    return JsonResponse({'sendemailstatus':'Success','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    return JsonResponse({'sendemailstatus': 'Error', 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

def password_emailcode_verify(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        emailcode = request.POST.get('emailcode','')

        if models.SendCodes.objects.filter(username=username, email=email,emailcode=emailcode):
            return JsonResponse({'verifyemailstatus':'Success','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    return JsonResponse({'verifyemailstatus':'Error','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

# def password_update(request):
#     if request.method == 'POST' and request.POST:
#         username = request.POST.get('username','')
#         email = request.POST.get('email','')
#         password_ori = request.POST.get('password','')
#         password = hash_password(password_ori)
#         try:
#             models.User.objects.filter(username=username,email=email).update(password=password)
#         except Exception as e:
#             print 'Update Password error'
#             print e
#             return HttpResponseRedirect('/users/password_emailcode_verify/')
#         else:
#             return HttpResponseRedirect('/users/login/')
#     return HttpResponseRedirect('/users/password_emailcode_verify/')


def password_update(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        password_ori = request.POST.get('password','')
        password = hash_password(password_ori)
        try:
            models.User.objects.filter(username=username,email=email).update(password=password)
        except Exception as e:
            print 'Update Password error'
            print e
            return JsonResponse({'passwordupdatestatus':'Error','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        else:
            return JsonResponse({'passwordupdatestatus':'Success','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    return HttpResponseRedirect('/users/password_emailcode_verify/')



def jqtest(request):
    # return HttpResponseRedirect('/users/jqtest/',locals())
    return render(request,'jqtest.html',locals())


# @valid_login
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect('/users/login')

@valid_login
def logout(request):
    request.session['session_username'] = ''
    return HttpResponseRedirect('/users/login')


#
# def captcha(request):
#     '''Captcha'''
#     image = Image.new('RGB', (147, 49), color = (255, 255, 255)) # model, size, background color
#     # font_file = os.path.join(BASE_DIR, 'static/fonts/ARIAL.TTF') # choose a font file
#     font_file = '/PycharmProjects/django/cmdb/Lato-Regular.ttf'
#     font = ImageFont.truetype(font_file, 47) # the font object
#     draw = ImageDraw.Draw(image)
#     rand_str = ''.join(random.sample(string.letters + string.digits, 4)) # The random string
#     draw.text((7, 0), rand_str, fill=(0, 0, 0), font=font) # position, content, color, font
#     del draw
#     request.session['captcha'] = rand_str.lower() # store the content in Django's session store
#     print request.session['captcha']
#     buf = cStringIO.StringIO() # a memory buffer used to store the generated image
#     image.save(buf, 'jpeg')
#     return HttpResponse(buf.getvalue(), 'image/jpeg') # return the image data stream as image/jpeg format, browser will treat it as an image
#


