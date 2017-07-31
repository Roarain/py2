#coding:utf-8
import yaml
import socket
import time
import sys
import os
import json

server_address = ('192.168.174.142',10086)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

for i in range(5):
    try:
        sock.connect(server_address)
        print 'Connect to [%s:%s] Success...' % (server_address)
        break
    except Exception as e:
        print 'Connect Faild.Will Tried 3s...'
        time.sleep(3)
else:
    print 'Connect Faild.Leave...'
    sys.exit(10)

FirstMsg = sock.recv(1024)

get_ack_msg = json.loads(FirstMsg.decode())

if get_ack_msg.get('filesize'):
    filename = get_ack_msg['filename']
    filesize = get_ack_msg['filesize']
print 'Filename is: %s' % (filename)
print 'Filesize is: %s' % (filesize)
sock.send('File metadata has received...')

received_content = ''
received_size = 0
received_path = '/home/roarain/tnkpdev_received.bz2'
received_name = os.path.basename(received_path)

while received_size < filesize:
    received_part_content = sock.recv(1024)
    received_content += received_part_content
    received_size += 1024
    # print '%s has reveived %s' % (received_name,received_size)
if received_size >= filesize:
    with open(received_path,'wb+') as f:
        f.write(received_content)

sock.send('Received %s Finished' % (received_name))

print '%s has reveived %s' % (received_name,filesize)
print 'Received %s Finished' % (received_name)
