# coding=gbk

import re


pattern = re.compile(r'\d{2}:\d{2}:\d{2}')
 
match = pattern.search('Wed Dec 31 06:50:00 CST 2014')
 
if match:
    print match.group()


# # ��������ʽ�����Pattern����
# pattern = re.compile(r'world')
#  
# # ʹ��Patternƥ���ı������ƥ�������޷�ƥ��ʱ������None
# # match = pattern.match('hello world')
# 
# print re.findall(r'world', 'hello world world ..fdad world');
# 
# match =  re.search(r'world', 'Wed Dec 31 06:50:00 CST 2014')
# 
# if match:
#     print match.group()
