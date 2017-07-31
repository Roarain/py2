#coding:utf-8
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.174.146',port=22,username='root',password='1')

channel = ssh.invoke_shell()
channel.settimeout(1)

while True:
    command = raw_input('>>>')
    channel.send('%s\n' % (command))
    while True:
        try:
            resp = channel.recv(9999)
            if len(resp) > 0:
                print resp
            else:
                break
        except Exception as e:
            print e
            break
    if command == 'exit':
        break

ssh.close()