#coding=utf-8
'''
import socket

server_addr = ('127.0.0.1',10001)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server_addr)

client_data = raw_input('Please Input your data: ')
sock.send(client_data)

server_data = sock.recv(1024)

print 'Data recived from server is: %s' % (server_data)

sock.close()
'''

import socket,sys,time

server_addr = ('127.0.0.1',10001)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
for i in range(5):
    try:
        sock.connect(server_addr)
        print 'connet to server success...'
        break
    except Exception as e:
        print 'conn to server faild,3s retry...'
        time.sleep(3)
else:
    print 'server is dead...'
    sys.exit(10)
while True:
    client_data = raw_input('Please Input your data: ')
    sock.send(client_data)
    if not client_data or client_data == 'break':
        sock.send('break')
        sock.close()
        sys.exit(10)
    else:
        server_data = sock.recv(1024)
        print 'Data recived from server is: %s' % (server_data)
