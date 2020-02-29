#coding:	utf-8
'''
    提取12306网站内对应站台名称
使用:       python get_station_name.py > station.py
'''
import re
import requests
from pprint import pprint


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9081'

#发送get请求，不判断证书
response = requests.get(url, verify=False)

#使用正则表达式提取所有站点 汉字和大写代号
#stations = dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text))
#使用正则表达式提取所有站点 大写代号和拼音 ([\u0041-\u005a]+)
stationsP = dict(re.findall(u'([A-Z]+)\|([a-z]+)', response.text))
stations = dict( (v,k) for k,v in stationsP.items() )

#格式化输出
pprint(stations,indent=4)


