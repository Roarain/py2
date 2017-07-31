#coding:utf-8
import yaml
import socket
import time
import sys
import os
import json
'''
According to 3 hanshake.
1st:Server send metadata(name,size) to Client,Client save metadata.
2st:Server send file to Client.Client based file size to determine consistency.And client send Ok.
3st:if consistency,close.
'''

server_address = ('192.168.174.142',10086)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(5)
print 'Server Is Running...'

#Read yaml config file .Get the filename/filepath of the file to be transferred.
#Filesize is not defined ,so get the size next step
with open('/PycharmProjects/code1/program2/config/config.yml','rb') as f:
    content_config = f.read()
#cfg is A dict.dict--> dict/list
cfg = yaml.load(content_config)

#yaml include dict key 'file_metadata'
if cfg.get('file_metadata'):
    filename = cfg['file_metadata']['filename']
    filepath = cfg['file_metadata']['filepath']
#According to Filepath to get Filesize .
with open (filepath,'rb') as f:
    content_file = f.read()
    filesize = len(content_file)
cfg['file_metadata']['filesize'] = filesize

send_ack_msg = json.dumps({'filename':filename,'filesize':filesize}).encode()

conn,addr = sock.accept()

#send ack msg to client
print 'Start Send ack msg...'
conn.send(send_ack_msg)
print 'Received Returned Msg Info'
ack_msg = conn.recv(1024)

if 'metadata has received' in ack_msg:
    conn.send(content_file)
    # print 'Start Send File',filename ,' to ',addr
    print 'Start Send  File To [%s:%s] ' % (addr)

ThreeMsg = conn.recv(1024)

if 'Finished' in ThreeMsg:
    print 'Send %s Finished' % (filename)


