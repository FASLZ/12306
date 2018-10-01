import requests
import json
import time
import re
from prettytable import PrettyTable
from colorama import Fore,init

title = '车次 出发/到达站 历时 软卧 硬卧 硬座 状态'
nowTime = time.strftime('%Y-%m-%d')
url1 = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971' 
response = requests.get(url1)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
stationsPY = re.findall(u'([A-Z]+)\|([a-z]+)',response.text) 
stations = dict(stations)
stationsPY = dict({v:k for k,v in stationsPY})
#print(stations)

def name(code):
    for k,v in stations.items():
        if code == v:
            return k

Fs = input('From station:\t')
Ts = input('End station:\t')
F = stations.get(Fs) or stationsPY.get(Fs) or 'SHH'
T = stations.get(Ts) or stationsPY.get(Ts) or 'XAY'
date = input('time of train:\t') or nowTime
if len(date) == 8:
    date = '{}-{}-{}'.format(date[:4],date[4:6],date[6:])
elif len(date) == 4:
    date = '{}-{}-{}'.format(time.strftime('%Y'),date[:2],date[2:]) 
elif len(date) == 2:
    date = '{}-{}'.format(time.strftime('%Y-%m'),date)
elif len(date) == 1:
    date = '{}-{}'.format(time.strftime('%Y-%m'),'0'+date)
print(date,F,T)

url = 'https://kyfw.12306.cn/otn/leftTicket/queryA'
header = {'User-Agent': header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
key_word = {
        "leftTicketDTO.train_date": date,
        "leftTicketDTO.from_station": F,
        "leftTicketDTO.to_station": T,
        "purpose_codes": "ADULT"
    }

try:
    a = requests.session().get(url, params=key_word, headers=header)
    lists = a.json()["data"]["result"]
    #print(lists)
except Exception as error:
    print('404 ?_? this url is losted')
    exit(0)
table=PrettyTable(title.split(' '))
#tickets=[]
for list in lists:
    #print(list+'\n\n')
    tacket = []
    lis = list.split('|')
    train_code = lis[3]
    from_station_name=lis[6]
    to_station_name = lis[7]
    start_time= lis[8]
    arrive_time =lis[9]
    lishi = lis[10]
    swz_num = lis[32] or lis[25]
    zy_num = lis[31]
    ze_num = lis[30]
    gr_num =lis[21]
    rw_num = lis[23]
    dw_num = lis[27]
    yw_num = lis[28]
    rz_num = lis[24]
    yz_num = lis[29]
    wz_num = lis[26]
    qt_num = lis[22]
    note_num = lis[1]
    #ticket.append()
    if lis[11] == 'Y':
        lis11 = '有'
    elif lis[11] == 'N':
        lis11 = '无'
    elif lis[11] == 'IS_TIME_NOT_BUY':
        lis11 = 'X'

    fs = (Fore.GREEN + name(lis[6]) + Fore.RESET)
    ts = (Fore.RED + name(lis[7]) + Fore.RESET)
    tfs= Fore.GREEN + lis[8] + Fore.RESET
    tts= Fore.RED + lis[9] + Fore.RESET
    table.add_row([lis[3],fs+'\n'+ts,tfs+'\n'+tts,lis[23],lis[28],lis[29],lis[1]]) 


print(table)
