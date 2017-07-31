#coding=utf-8
import re
string = '675671au7856vchhijf'
sub_string = 'roarain love you,rhehehe love you'
split_string = 'roarain,love,you,niehong,nh'

result1 = re.match('\d+',string).group()
result2 = re.search('\d+',string).group()
result3 = re.findall('\d+',string)
print result1
print result2
print result3
print '_'.join(result3)

# re_result1 = re.sub('roarain','wxy',sub_string)
# print re_result1
re_result2 = re.sub('r.{6}','wxy',sub_string)
print re_result2

split_result1 = re.split(',',split_string,2)
print split_result1

compile = re.compile('\d+')
result4 = re.findall(compile,string)
print result4