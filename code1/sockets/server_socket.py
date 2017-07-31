#coding=utf-8

'''
import socket

server_address = ('127.0.0.1',10001)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(5)

print 'Socket Server starting,Waiting for client connection...'

#conn is socket object,addr is client's ip:port
conn,addr = sock.accept()
print conn,addr

# print type(sock.accept())
#recive data from client every 1024 bytes
client_data = conn.recv(1024)
print 'Data from Client is: %s' % (client_data)
#send client The upper
conn.send(client_data.upper())
#close
sock.close()
'''
import socket

server_address = ('127.0.0.1',10001)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(3)

print 'Socket Server starting,Waiting for client connection...'

while True:
    #conn is socket object,addr is client's ip:port
    conn,addr = sock.accept()
    # print conn,addr
    print 'client [%s:%s] connect successful...' % (addr)

    while True:
        client_data = conn.recv(1024)
        if not client_data  or client_data == 'break':
            print '[%s:%s] exit' % addr
            conn.close()
            break
        else:
            print 'data from client [%s:%s] is:' %addr,client_data
            conn.send(client_data.upper())