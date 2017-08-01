# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse,HttpResponseRedirect,render_to_response
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import auth
from . import models
import hashlib
import time
import datetime
from django.http import JsonResponse
import gencaptcha
from serverdetail import ServerDetail
import MySQLdb
from genrandom import GenerateRandom
from django.core.mail import send_mail
from service_list import service_status
from service_control import service_controls
from get_history_datas_api import ZabbixAPI
import datetime
from zabbixlogin import ZabbixLogin


# Create your views here.



def test(request):
    print request.method
    name = request.GET.get('name')
    age = request.GET.get('age')
    return HttpResponse('<h3>Your name: %s. Your age: %s.' % (name,age))

#注册页面,signup.html会先做ajax用户名和密码的校验，通过后传递给register方法，并保存到数据库中
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

#临时跳转页
def autojump(request):
    return render(request,'autojump.html',locals())

#将密码字符串进行md5加密
def hash_password(password):
    hash_md5 = hashlib.md5()
    hash_md5.update(password)
    password = hash_md5.hexdigest()
    return password

#方法check_regist_duplicate_user传递username给check_duplicate_user,用来校验用户是否合法，并返回json串
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

#注册页面的ajax传递用户输入框的username给check_regist_duplicate_user来校验用户是否合法
def check_regist_duplicate_user(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        if len(username) > 0:
            return JsonResponse(check_duplicate_user(username))
        else:
            return JsonResponse({'data': '', 'status': 'empty', 'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    else:
        return JsonResponse({'data':'','status':'','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

#登陆方法,包含用户名，密码，验证码。登陆成功后会生成session和cookie，后期使用sessiob来验证用户是否登陆，确定操作权限
def login(request):
    if request.method == 'POST' and request.POST:
        print request.POST
        username = request.POST.get('username')
        password = hash_password(request.POST.get('password'))
        code = request.POST.get('code')
        if code == request.session['captcha']:

            if models.User.objects.filter(username=username,password=password):
                response = HttpResponseRedirect('/clocmdb/server_register/')
                # response = HttpResponseRedirect('/clocmdb/server_list/')
                response.set_cookie('cookie_username',username)

                request.session['session_username'] = username
                return response
            else:
                autojump = 'login_faild'
                print 'User or Password error,Please reLogin.'
                return render(request,'autojump.html',{'autojump':autojump})

    return render(request,'signin.html',locals())

#使用gencaptcha方法生成用户登陆的验证码，并画图在前台展现，并将生成的验证码字符串保存到session中
def captcha(request):
    gc = gencaptcha.GenCaptcha()
    img,img_char = gc.save_to_mem()
    request.session['captcha'] = img_char.replace(' ','')
    return HttpResponse(img, 'image/jpeg')

#装饰器，判断用户是否登陆，且session是否正确
def valid_login(func):
    def inner(request,*args,**kwargs):
        try:
            request.session.get('session_username')
        except Exception as e:
            print 'Session Error,Please Login.'
            # return render(request, 'signin.html', locals())
            return HttpResponseRedirect('/clocmdb/login/')
        else:
            session_username = request.session.get('session_username')
            if models.User.objects.filter(username=session_username):
                return func(request,*args,**kwargs)
            else:
                # return render(request,'signin.html',locals())
                return HttpResponseRedirect('/clocmdb/login/')
    return inner

#设置session为空，退出用户登陆
@valid_login
def logout(request):
    request.session['session_username'] = ''
    return HttpResponseRedirect('/clocmdb/login/')



# @valid_login
# def index(request):
#     session_username = request.session.get('session_username')
#     return render(request,'index.html',locals())


@valid_login
def server_register(request):
    session_username = request.session.get('session_username')
    if request.method == 'POST' and request.POST:
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        print 'Register Server ip: %s' %(ip)
        print 'Register Server ip_type: %s' %(type(ip))
        if not models.Server.objects.filter(ip=ip,port=port):
            username = request.POST.get('username')
            password_ori = request.POST.get('password')
            password = hash_password(password_ori)
            protocal = request.POST.get('protocal')

            models.Server.objects.create(ip=ip, port=port, username=username, password=password, protocal=protocal)

            try:
                server_id_sql = "select id from clocmdb_server where ip = '%s' and port = '%s' " % (ip,port)
                server_id = execute_select_sql(server_id_sql)
                print 'server_id: %s' % (server_id)
                print 'server_id type: %s' % (type(server_id))
                
                user_id_sql = "select id from clocmdb_user where username = '%s' " % (session_username)
                user_id = execute_select_sql(user_id_sql)
                print 'user_id is: %s' % (user_id)
                print 'user_id type: %s' % (type(user_id))

            except Exception as e:
                print
                print e
            else:
                models.UserServer.objects.create(user_id=user_id,username=session_username,server_id=server_id,server_ip=ip)

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
                    models.ServerDetail.objects.create(server_id=server_id,ip=ip,port=port,os_info=os_info,cpu_info=cpu_info,cpu_count=cpu_count,mem_info=mem_info,disk_info=disk_info)

            return HttpResponseRedirect('/clocmdb/server_list/')

        elif models.Server.objects.filter(ip=ip,port=port):
            print 'Server %s:%s has been register...' % (ip,port)
            return HttpResponse('Server %s has been register...' % (ip))
            # return render(request,'server_register.html',locals())
    return render(request,'server_register.html',locals())

#根据session_name查找用户username所属的的所有服务器的基本信息
#查询结果如下，以tuple形式展现
#servers value: (3L, '192.168.174.144', 22L, 'root', 'c4ca4238a0b923820dcc509a6f75849b', 'SSH', 'N', datetime.datetime(2017, 7, 12, 17, 44, 48))
#servers type: <type 'tuple'>
@valid_login
def server_list(request):
    session_username = request.session.get('session_username')

    servers_sql = "select * from clocmdb_server where id in (select server_id from clocmdb_userserver where user_id = (select id from clocmdb_user where username = '%s'))" % (session_username)
    servers = execute_select_all_sql(servers_sql)

    print 'servers type: %s' % (type(servers))
    print servers
    return render(request,'server_list.html',locals())



#测试分页
# @valid_login
# def server_list(request,pageid):
#     session_username = request.session.get('session_username')
#
#     servers_sql = "select * from clocmdb_server where id in (select server_id from clocmdb_userserver where user_id = (select id from clocmdb_user where username = '%s'))" % (session_username)
#     servers = execute_select_all_sql(servers_sql)
#     if not pageid:
#         pageid = 1
#
#     paginator = Paginator(servers,2)
#     try:
#         servers_view = paginator.page(pageid).object_list
#     except PageNotAnInteger:
#         servers_view = paginator.page(1).object_list
#     except EmptyPage:
#         servers_view = paginator.page(paginator.num_pages).object_list
#
#     print 'servers type: %s' % (type(servers))
#     print 'servers data: ',servers
#
#     print 'servers_view type: %s' % (type(servers_view))
#     print 'servers_view data: ' ,servers_view
#
#     return render(request,'server_list.html',locals())

#django测试分页pagination
# @valid_login
# def ajax_page(request,pageid):
#     session_username = request.session.get('session_username')
#
#     servers_sql = "select * from clocmdb_server where id in (select server_id from clocmdb_userserver where user_id = (select id from clocmdb_user where username = '%s'))" % (session_username)
#     servers = execute_select_all_sql(servers_sql)
#     if not pageid:
#         pageid = 1
#
#     paginator = Paginator(servers,2)
#     try:
#         servers_view = paginator.page(pageid).object_list
#     except PageNotAnInteger:
#         servers_view = paginator.page(1).object_list
#     except EmptyPage:
#         servers_view = paginator.page(paginator.num_pages).object_list
#
#     print 'servers type: %s' % (type(servers))
#     print 'servers data: ',servers
#
#     print 'servers_view type: %s' % (type(servers_view))
#     print 'servers_view data: ' ,servers_view
#
#     return render(request,'ajax_page.html',locals())




#根据服务器的的server_id，server和serverdetail多表联合查询，获取服务器的具体信息
@valid_login
def server_detail(request,server_id):
    session_username = request.session.get('session_username')
    # server_detail_sql = "select s.ip ,s.port,s.username,s.protocal,s.isActive,sd.os_info,sd.cpu_info,sd.cpu_count,sd.mem_info,sd.disk_info from users_server s ,users_serverdetail sd where s.base_ptr_id = sd.server_id and sd.server_id = (select base_ptr_id from users_server where ip = '%s')" % (ip)
    server_detail_sql = "select s.ip ,s.port,s.username,s.protocal,s.current_time,sd.os_info,sd.cpu_info,sd.cpu_count,sd.mem_info,sd.disk_info from clocmdb_server s ,clocmdb_serverdetail sd where s.id =  sd.server_id  and sd.server_id = '%s' " % (server_id)
    server_details = execute_select_one_sql(server_detail_sql)
    print 'server_details data is: ', server_details
    return render(request,'server_detail.html',locals())

#根据server_id获取ip和port
def get_ipport_from_server_id(server_id):
    ipport_from_server_id_sql = "select s.ip ,s.port from clocmdb_server s ,clocmdb_serverdetail sd where s.id =  sd.server_id  and sd.server_id ='%s' " % (server_id)
    ip, port = execute_select_one_sql(ipport_from_server_id_sql)
    return ip


#前台传递过来的参数为http://ip:port/clocmdb/service_list/server_id/
#根据server_id获取主机的ip:port，再传递给函数service_list.service_status
@valid_login
def service_list(request,server_id):
    session_username = request.session.get('session_username')
    username = session_username
    # ip_from_server_id_sql = "select s.ip ,s.port from clocmdb_server s ,clocmdb_serverdetail sd where s.id =  sd.server_id  and sd.server_id ='%s' " % (server_id)
    # ip,port = execute_select_one_sql(ip_from_server_id_sql)
    ip = get_ipport_from_server_id(server_id)
    # print ip
    ss = service_status(ip)
    #将二级字典转换为以一级字典组成的列表，从而再交给django前台做for循环，否则django不能识别二级for循环
    #获取结果如下：
    #[{'status': 'active', u'service': 'salt-minion', 'installed': 'Y'}, {'status': '', u'service': 'nginx', 'installed': 'N'}, {'status': 'inactive', u'service': 'redis', 'installed': 'Y'}, {'status': 'active', u'service': 'salt-master', 'installed': 'Y'}, {'status': 'inactive', u'service': 'httpd', 'installed': 'Y'}]
    result = []
    for i in ss:
        dicts = ss[i]
        dicts['service'] = i
        result.append(dicts)
    print result
    # for service in ss:
    #     for info in ss[service]:
    #         installed = info['installed']
    #         status = info['status']
    return render(request,'service_list.html',locals())


#前台传递过来的参数为http://ip:port/clocmdb/service_control/server_id/service_name/control,代表主机id,服务名称,对服务的动作.
@valid_login
def service_control(request,server_id,service_name,control):
    session_username = request.session.get('session_username')
    username = session_username
    ip_from_server_id_sql = "select s.ip ,s.port from clocmdb_server s ,clocmdb_serverdetail sd where s.id =  sd.server_id  and sd.server_id ='%s' " % (
    server_id)
    ip, port = execute_select_one_sql(ip_from_server_id_sql)
    sc = service_controls(ip,service_name,control)
    print sc
    # return render(request,'server_list.html',locals())
    url = '/clocmdb/service_list/' + str(server_id) + '/'
    return HttpResponseRedirect(url)


def dict2list(listdatas):
    values = []
    clocks = []
    for dictdatas in listdatas:
        values.append(float(dictdatas["value"]))
        clocks.append(str(unixts2nowtime(float(dictdatas["clock"]))))
    values.reverse()
    clocks.reverse()
    return (values,clocks)

def unixts2nowtime(unixts):
    # nowtime = datetime.datetime.fromtimestamp(unixts).strftime('%Y-%m-%d %H:%M:%S')
    nowtime = datetime.datetime.fromtimestamp(unixts).strftime('%H:%M:%S')
    return nowtime

@valid_login
def server_monitor(request,server_id):
    ip = get_ipport_from_server_id(server_id)
    zapi = ZabbixAPI(ip)
    keys = zapi.keys
    historyids = zapi.historyids
    key_historys_dict = {}

    for key in keys:
        itemid = zapi.get_itemid(key)
        for historyid in historyids:
            historys = zapi.get_historys(itemid, historyid)
            if historys != []:
                if 'vfs.fs.size' in key or 'swap' in key or 'vm.memory.size[total]' in key:
                    historys = historys[0:1]
                else:
                    pass
                for history in historys:
                    history.pop('itemid')
                    history.pop('ns')
                key_historys_dict[key] = historys
            else:
                pass

    mem_total = int(key_historys_dict["vm.memory.size[total]"][0]["value"]) / pow(1024,2)

    mem_available = key_historys_dict["vm.memory.size[available]"]

    mem_available_values_ori,mem_available_clocks = dict2list(mem_available)
    mem_available_values = []
    for i in mem_available_values_ori:
        mem_available_values.append(i / pow(1024,2))

    cpu_avg1 = key_historys_dict["system.cpu.load[percpu,avg1]"]
    cpu_avg1_values,cpu_avg1_clocks = dict2list(cpu_avg1)

    cpu_avg5 = key_historys_dict["system.cpu.load[percpu,avg5]"]
    cpu_avg5_values, cpu_avg5_clocks = dict2list(cpu_avg5)

    cpu_avg15 = key_historys_dict["system.cpu.load[percpu,avg15]"]
    cpu_avg15_values, cpu_avg15_clocks = dict2list(cpu_avg15)

    net_in = key_historys_dict["net.if.in[eno16777736]"]
    net_in_values, net_in_clocks = dict2list(net_in)

    net_out = key_historys_dict["net.if.out[eno16777736]"]
    net_out_values, net_out_clocks = dict2list(net_out)

    vfs_base = key_historys_dict["vfs.fs.size[/,pfree]"][0]["value"]

    try:
        vfs_home = key_historys_dict["vfs.fs.size[/home,pfree]"]
    except Exception as e:
        print e
    else:
        vfs_home = ''

    # if key_historys_dict["vfs.fs.size[/home,pfree]"]:
    # vfs_home = key_historys_dict["vfs.fs.size[/home,pfree]"][0]["value"]
    # else:
    #     vfs_home = ''

    swap_pfree = key_historys_dict["system.swap.size[,pfree]"][0]["value"]

    return render(request,'server_monitor.html',locals())

@valid_login
def monitor_zabbix(request,server_id):
    url = "http://192.168.174.144/zabbix/charts.php?fullscreen=0&groupid=2&hostid=10113&graphid=557"
    zl = ZabbixLogin()
    return HttpResponseRedirect(url)


def get_info_from_minitor_id(server_id,monitor_id):
    ip = get_ipport_from_server_id(server_id)
    monitor_id_name = {'111111':'Available memory','111112':'CPU $2 time','111113':'Incoming network traffic on $1','111114':'Free disk space on $1'}
    minitor_name = monitor_id_name[monitor_id]
    sql = "select h.host,h.hostid,hg.groupid,i.itemid,i.name,g.graphid from hosts h ,items i ,graphs_items g ,hosts_groups hg where h.host = '%s' and h.hostid = i.hostid and i.itemid = g.itemid and i.name = '%s' limit 1" % (ip,minitor_name)
    host,hostid,groupid,itemid,name,graphid = execute_select_one_sql_zabbix(sql)
    return (hostid,graphid)

@valid_login
def zabbix_monitor(request,server_id,monitor_id):
    hostid, graphid = get_info_from_minitor_id(server_id,monitor_id)
    groupid = 2
    zl = ZabbixLogin()
    url = "http://192.168.174.144/zabbix/charts.php?fullscreen=0&groupid=%s&hostid=%s&graphid=%s" % (groupid,hostid,graphid)
    return HttpResponseRedirect(url)


#根据注册时的用户名和邮箱重置密码
def findpassword(request):
    return render(request,'findpassword.html',locals())

#方法sendemail用来执行执行send mail的整个事务，包括生成验证码，组合消息内容，将组合后的邮件内容发送给收件人。
#GenerateRandom().gen_random()是生成验证码并保存到数据库中
#send_mail是django自带的sendmail，需要配置settings.py文件。
def sendemail(request):
    emailcode = GenerateRandom().gen_random()
    msg='您通过邮箱找回密码的验证码是:%s,五分钟内有效.' % (emailcode)
    send_mail('密码找回',
            '?',
            'sysalarm@clo.com.cn',
            ['wangxiaoyu@clo.com.cn',],
            html_message=msg)
    return HttpResponse('Send Email OK')

#此方法是从校验用户和邮箱是否匹配，发送邮件，返回前台邮件是否发送成功的json串等的整个事务
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

#校验用户输入的邮箱验证码是否匹配。
def password_emailcode_verify(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        emailcode = request.POST.get('emailcode','')

        if models.SendCodes.objects.filter(username=username, email=email,emailcode=emailcode):
            return JsonResponse({'verifyemailstatus':'Success','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    return JsonResponse({'verifyemailstatus':'Error','time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

#更新密码。将前端输入的密码加密后更新到数据库，并将结果以json格式返回给前端
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
    return HttpResponseRedirect('/clocmdb/password_emailcode_verify/')





#以下是执行原生sql
def execute_select_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0][0]
    conn.close()

def execute_insert_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def execute_select_all_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    conn.close()

def execute_select_one_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0]
    conn.commit()
    conn.close()
def execute_select_one_sql_zabbix(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='zabbix')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()[0]
    conn.commit()
    conn.close()

def execute_delete_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def execute_update_sql(sql):
    conn = MySQLdb.connect(user='root', passwd='abcd1234', host='192.168.174.144', port=3306, db='clocmdb')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


def name_list(request):
    per_page_num = 10
    '''
    1       (0,10)
    2       (10,20)
    3       (20,30)
    [(n-1)*10,n*10]
    '''
    all_ids_names = models.IdName.objects.all()
    all_nums = len(all_ids_names)

    if not request.GET.get('page'):
        current_page = 1
    elif request.GET.get('page'):
        current_page = int(request.GET.get('page'))

    if all_nums % per_page_num == 0:
        all_pages = all_nums / per_page_num
        last_num = per_page_num
    elif all_nums % per_page_num > 0:
        all_pages = all_nums // per_page_num + 1
        last_num = all_nums % per_page_num

    if current_page > all_pages:
        current_page = 1
        url = 'http://192.168.174.144:9000/clocmdb/name_list/?page=1'
        return HttpResponseRedirect(url)

    pre_page = current_page - 1
    next_page = current_page + 1

    if current_page <= 1:
        pre_page = all_pages
    elif current_page >= all_pages:
        next_page = 1

    start_num = (current_page - 1) * per_page_num
    end_num = current_page * per_page_num

    ids_names = models.IdName.objects.all()[start_num:end_num]

    if start_num >= all_nums:
        ids_names = models.IdName.objects.all()
    elif end_num >= all_nums:
        ids_names = models.IdName.objects.all()[all_nums-last_num:]
    else:
        ids_names = models.IdName.objects.all()[start_num:end_num]

    return render(request,'name_list.html',locals())

def name_list_go(request):
    if request.method == 'POST' and request.POST:
        topagenum = request.POST.get('topagenum')
        if topagenum == '':
            url = 'http://192.168.174.144:9000/clocmdb/name_list/'
        elif topagenum:
            url = 'http://192.168.174.144:9000/clocmdb/name_list/?page=' + str(topagenum)
        print url
        return HttpResponseRedirect(url)