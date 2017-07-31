import re
import cookielib
import urllib
import urllib2
from lxml import etree
from bs4 import BeautifulSoup




cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

url1 = 'http://passport.ewt360.com/login/prelogin?callback=jQuery1112012606466430024965_1499218112181&sid=2&username=18538861839&password=lxy999977&fromurl=%2Fhome&isremember=1&_=1499218112182'
url2 = 'http://www.ewt360.com/login?tk=6212979-1-25baa3493a47281a&fromurl=/home'
# url3 = 'http://www.ewt360.com/Apply'
# url3 = 'http://www.ewt360.com/applynation/toudangweici'

req_url1 = urllib2.Request(url1)
resp_url1 = urllib2.urlopen(req_url1)
html_url1 = resp_url1.read()
print html_url1

print '1111111111111111111'
for index,cookie in enumerate(cj):
    print "[",index,"]",cookie
print '22222222222222222'

req_url2 = urllib2.Request(url2)
resp_url2 = urllib2.urlopen(req_url2)
html_url2 = resp_url2.read()
# print html_url2
print '33333333333333333'
for index,cookie in enumerate(cj):
    print "[",index,"]",cookie
print '444444444444444444'

# req_url3 = urllib2.Request(url3)
# resp_url3 = urllib2.urlopen(req_url3)
# html_url3 = resp_url3.read()
# # print html_url3
# print '55555555555'
# for index,cookie in enumerate(cj):
#     print "[",index,"]",cookie
# print '666666666666'


url4 = 'http://www.ewt360.com/ApplyNation/WeiCiRange?year=2016&bz=b&pici=3&querycontent=100000%2C120000&querytype=9&type=1'
# url4 = 'http://www.ewt360.com/ApplyNation/WeiCiRange?year=2016&bz=b&pici=3&querycontent=100000%2C120000&querytype=9&type=2'
req_url4 = urllib2.Request(url4)
resp_url4 = urllib2.urlopen(req_url4)
html_url4 = resp_url4.read()

# a = etree.HTML(html_url4)
# b = etree.tostring(a)

# print html_url4
# print '77777777777777'
# for index,cookie in enumerate(cj):
#     print "[",index,"]",cookie
# print '8888888888888888'

# html4 = etree.HTML(html_url4)
# with open('test.html','w') as f:
#     for i in html_url4:
#         f.write(i)
#     f.close()

selector = etree.HTML(html_url4)

result = selector.xpath("//td")


for i in result:
    print i.text
# obj = BeautifulSoup(html_url4,'html.parser')
#
# index = 0
# # urls = re.findall(r'''objURL":"(.*?)''',str(obj))
# titles = obj.findAll('a')
# print '555555555'
# print titles
# print '66666666'
# for i in titles:
#     if i.get('title'):
#         print i.get('title')



