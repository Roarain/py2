#coding=utf-8

import time
import thread
import threading
'''
#serial exec
def say(name):
    print 'func say start time:',time.ctime()
    time.sleep(2)
    print 'Hello,%s' % name
    print 'func say end time:',time.ctime()
def hi(name):
    print 'func say start time:',time.ctime()
    time.sleep(3)
    print 'Hello,%s' % name
    print 'func say end time:',time.ctime()
def main():
    say('roarain')
    say('wangxiaoyu')

if __name__ == '__main__':
    main()
'''
'''
#parallel exec
def say(name):
    print 'func say start time:',time.ctime()
    time.sleep(2)
    print 'Hello,%s' % name
    print 'func say end time:',time.ctime()
def hi(name):
    print 'func say start time:',time.ctime()
    time.sleep(3)
    print 'Hello,%s' % name
    print 'func say end time:',time.ctime()

if __name__ == '__main__':
    thread.start_new_thread(say,('roarain',))
    thread.start_new_thread(hi,('wxy',))
    time.sleep(5)
'''
'''
class MyThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print 'hello,%s' % (self.name)

if __name__ == '__main__':
    t1 = MyThread('roarain')
    t2 = MyThread('wxy')
    t1.start()
    t2.start()
'''

def say(name):
    print 'say start time:',time.ctime()
    time.sleep(2)
    print 'Hello,%s' % name
    print 'say end time:',time.ctime()
def hi(name):
    print 'hi start time:',time.ctime()
    time.sleep(3)
    print 'Hello,%s' % name
    print 'hi end time:',time.ctime()
def main():
    print 'main start time:', time.ctime()
    print 'Hello,main'
    print 'main end time:', time.ctime()
if __name__ == '__main__':
    t1 = threading.Thread(target=say,args=('roarain',))
    t2 = threading.Thread(target=hi,args=('wxy',))
    t3 = threading.Thread(target=main)
    t1.setName('say')
    t1.start()
    # t1.join()
    print t1.getName()
    t2.setName('hi')
    t2.start()
    # t2.join()
    print t2.getName()
    t3.setName('main')
    # t3.join()
    t3.start()
    print t3.getName()
    t1.join()
    t2.join()
    t3.join()


