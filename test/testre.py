# coding=gbk

import re


pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
 
match = pattern.search('Wed Dec 31 06:50:00 CST 2014')
 
if match:
    print match.group()


# # 将正则表达式编译成Pattern对象
# pattern = re.compile(r'world')
#  
# # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
# # match = pattern.match('hello world')
# 
# print re.findall(r'world', 'hello world world ..fdad world');
# 
# match =  re.search(r'world', 'Wed Dec 31 06:50:00 CST 2014')
# 
# if match:
#     print match.group()
