import time

while True:
    try:
        print 'a'
    except:
        print 'aa'
    try:
        print 'b'
    except:
        print 'bb'
    time.sleep(5)