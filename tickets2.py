# coding: utf-8
"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> [<date>]

Options:
    -g     高铁
    -d     动车
    -t     特快
    -k     快速
    -z     直达
    -h   --help     display this help
    -v   --version  show version 

Example:
    tickets 上海 北京 2018-05-01
    tickets -gdt beijing shanghai 2018-08-25
    
By FASLZ @github.com/faslz/12306
"""
import json
import time
import requests
import price
import station
import stationPY
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style


#   创建颜色类
#通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
init(autoreset=False)  # False 关闭
class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET
    #  灰色style
    def dim(self, s):
        #print(Style.DIM + s + Style.RESET_ALL)
        return Style.DIM + s + Style.RESET_ALL
    def bright(self, s):  #高亮
        return Style.BRIGHT + s + Style.RESET_ALL

color = Colored()#创建Colored对象

#   初始化
''''''
date        = "2018-05-01"
fromStation = "AOH"
toStation   = "NCG"
version     = "tackets 1.3.3"
title       = "车次 站点 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座"
NOTE        = False
''''''
table = PrettyTable(title.split())
msg   = PrettyTable(["Time","车次","站点","状态","备注"])

def getUrl():

    url = ("https://kyfw.12306.cn/otn/leftTicket/queryZ?"
           "leftTicketDTO.train_date={}"
           "&leftTicketDTO.from_station={}"
           "&leftTicketDTO.to_station={}"
           "&purpose_codes=ADULT").format(date, fromStation, toStation)

    url2 = ("https://kyfw.12306.cn/otn/leftTicket/queryT?"
           "leftTicketDTO.train_date={}"
           "&leftTicketDTO.from_station={}"
           "&leftTicketDTO.to_station={}"
           "&purpose_codes=ADULT").format(date, fromStation, toStation)

    header= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115'}

    RAIL_EXPIRATION = "1576651914389"
    RAIL_DEVICEID = "lBJStCNl0YGo_HVkGtwOo2LWziXcwzpIk5gc2vAILNYdRfaeZ04nJtZ1JZwgQIssMDksn10rAz6Hz-bekeufhAusaKJId8f2BCg05ocgrzc8-chv8h4IB-lQ9H04XjLXr2fbnHw-SLZga3PewEfgPz2s-mhp7NAz"
    session = requests.Session()
    # session.verify=False
    session.cookies.set("RAIL_EXPIRATION", RAIL_EXPIRATION)
    session.cookies.set("RAIL_DEVICEID", RAIL_DEVICEID)

    try:
        #r    = requests.get(url, headers=header)
        r   = session.get(url, headers=header, timeout=20)
        lists= r.json()["data"]['result']
    except:
        try:
            r = session.get(url2, headers=header, timeout=20)
            lists= r.json()["data"]['result']
        except:
            print('The NetWork likes out work? or That time URL haven\'t be open. try again.')
            exit(0)
    return lists


def findKey(lists,trainType):
    tackets=[]
    for list in lists:
        li = list.split('|')
        train_no        = li[2]
        from_station_no = li[16]
        to_station_no   = li[17]
        seat_types      = li[35]

        train_code = li[3]
        from_station_name = li[6]
        to_station_name   = li[7]
        start_time        = li[8]
        arrive_time       = li[9]
        diachronic        = li[10] #历时
        shangWuZuo        = li[32] or li[25] or '--' #商务座
        yiDengZuo         = li[31] or '--' #一等座
        erDengZuo         = li[30] or '--' #二等座
        gaoJiRuanWo       = li[21] or '--' #高级软卧
        ruanWo            = li[23] or '--' #软卧
        dongWo            = li[27] or '--' #动卧
        yingWo            = li[28] or '--' #硬卧
        ruanZuo           = li[24] or '--' #软座
        yingZuo           = li[29] or '--' #硬座
        wuZuo             = li[26] or '--' #无座
        others            = li[22] or '--' #其他信息
        note              = li[1]  or '--' #备注
        state             = li[11] #状态 -Y -N -IS_TIME_NOT_BUY
        diachronic        = diachronic.split(':')[0] + '时' + diachronic.split(':')[1] + '分'

        #过滤车型
        if train_code[0] not in trainType:
            continue
        
        if state == 'Y':
            #获取价格
            A,B,C,D,E,F,G,H,I,J = price.getPrice(train_no, from_station_no, to_station_no, seat_types, date)

            table.add_row([
                 color.yellow(train_code),
                 (color.green(station.get_name(from_station_name))+'\n'+color.red(station.get_name(to_station_name))),
                 (color.green(start_time)+'\n'+color.red(arrive_time)),
                 diachronic,
                 (shangWuZuo   +'\n'+color.blue(A)),
                 (yiDengZuo    +'\n'+color.blue(B)),
                 (erDengZuo    +'\n'+color.blue(J) if (train_code[0]=='G') else color.blue(C)),
                 (gaoJiRuanWo  +'\n'+color.blue(D)),
                 (ruanWo       +'\n'+color.blue(E)),
                 (dongWo       +'\n'+color.blue(F)),
                 (yingWo       +'\n'+color.blue(G)),
                 (ruanZuo      +'\n'+color.blue(H)),
                 (yingZuo      +'\n'+color.blue(I)),
                 (wuZuo        +'\n'+color.blue(C) if (train_code[0]=='G') else color.blue(J)),
                 #others,
                 #note
             ])
        # 已售完
        elif state == 'N':
            table.add_row([
               # Style.DIM+
                 color.dim(train_code),
                 ( color.dim(station.get_name(from_station_name)) +'\n'+ color.dim(station.get_name(to_station_name)) ),
                 ( color.dim(start_time) +'\n'+ color.dim(arrive_time)),
                 color.dim(diachronic),
                 color.dim(shangWuZuo),
                 color.dim(yiDengZuo),
                 color.dim(erDengZuo),
                 color.dim(gaoJiRuanWo),
                 color.dim(ruanWo),
                 color.dim(dongWo),
                 color.dim(yingWo),
                 color.dim(ruanZuo),
                 color.dim(yingZuo),
                 color.dim(wuZuo),
                 #color.dim(others),
                 #color.dim(note)
                # +Style.RESET_ALL
                ])
        # 
        elif state == 'IS_TIME_NOT_BUY':
            global NOTE
            NOTE = True
            #msg = PrettyTable(["Time","车次","站点","状态","备注"])
            msg.add_row([
                "当日",
                color.red(train_code),
                color.red(station.get_name(from_station_name)+' --> '+station.get_name(to_station_name)),
                color.red(note),
                state])
            #print(msg)
            #return ''
            continue
        
    return tackets


def printTickets(tackets):
    if NOTE:
        print(msg)
    #将时间转换成时间数组
    date_array = time.strptime(date,'%Y-%m-%d')
    #将时间数组转换为指定格式
    print_date = time.strftime('%A   %Y-%m-%d   %B',date_array)
    now_time   = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    #print('{:^120}{:<}'.format(print_date,now_time))
    print('{:>85}{:>50}'.format(color.bright(print_date),now_time))
    print(table.get_string())


def decisionInput(arguments):
    global fromStation, toStation, date
    
    fromStation = arguments.get('<from>')
    toStation   = arguments.get('<to>')
    date        = arguments.get('<date>')
    
    # get type of train
    trainTypes = ['-g','-d','-t','-k','-z']
    train_type = [ trainType[-1].upper() for trainType in trainTypes if arguments.get(trainType) ]
    if not train_type:
        train_type = [trainType[-1].upper() for trainType in trainTypes]
        #print('this is all of train type')
    #print(train_type)
    
    # time style
    if date == None:
        date = time.strftime('%Y-%m-%d',time.localtime())
    elif len(date) == 8:
        date = '{}-{}-{}'.format(date[:4],date[4:6],date[6:])
    elif len(date) == 4:
        date = '{}-{}-{}'.format(time.strftime('%Y',time.localtime()),date[:2],date[2:])
    elif len(date) == 2:
        date = '{}-{}'.format(time.strftime('%Y-%m',time.localtime()),date)
    
    
    chinese_f, pinyin_f = False, False
    chinese_t, pinyin_t = False, False
    for char in fromStation:
        if (char >= u'\u0041' and char<=u'\u005a') or (char >= u'\u0061' and char<=u'\u007a'):  # 拼音
            pinyin_f, chinese_f = True, False
        if (u'\u9fa5' >= char >= u'\u4e00'):  # 中文
            pinyin_f, chinese_f = False, True
    for char in toStation:
        if (char >= u'\u0041' and char<=u'\u005a') or (char >= u'\u0061' and char<=u'\u007a'):  # 拼音
            pinyin_t, chinese_t = True, False
        if u'\u9fa5' >= char >= u'\u4e00':  # 中文
            pinyin_t, chinese_t = False, True
    #print(chinese_f,pinyin_f,chinese_t,pinyin_t)
    # 输入为拼音
    if pinyin_f:
        fromStation = stationPY.stations.get(fromStation)
    # 输入为中文
    elif chinese_f:
        fromStation = station.stations.get(fromStation)
    if pinyin_t:
        toStation = stationPY.stations.get(toStation)
    elif chinese_t:
        toStation = station.stations.get(toStation)
    if (not pinyin_f and not chinese_f) or (not pinyin_t and not chinese_t):
        print('Error , check input')
        exit(0)
    return train_type
    

def main():
    
    arguments   = docopt(__doc__, version = version)
    #print(arguments)
    print('Lodding now... please wait a minute',end='\r')
    trainType = decisionInput(arguments)
    #print(fromStation,toStation,date)
    lists   = getUrl()
    tackets = findKey(lists,trainType)
    printTickets(tackets)
    
if __name__ == '__main__':
    main()

                           
