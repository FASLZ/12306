#coding: utf-8
'''
票价查询
'''
import json
import requests


def getPrice(train_no,from_station_no,to_station_no,seat_types,date):
    #不同座位票价
    A,B,C,D,E,F,G,H,I,J='','','','','','','','','',''
    
    header  = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    priceUrl= ("https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?"
               "train_no={}"
               "&from_station_no={}"
               "&to_station_no={}"
               "&seat_types={}"
               "&train_date={}").format(train_no, from_station_no, to_station_no, seat_types, date)

    RAIL_EXPIRATION = "1576651914389"
    RAIL_DEVICEID = "lBJStCNl0YGo_HVkGtwOo2LWziXcwzpIk5gc2vAILNYdRfaeZ04nJtZ1JZwgQIssMDksn10rAz6Hz-bekeufhAusaKJId8f2BCg05ocgrzc8-chv8h4IB-lQ9H04XjLXr2fbnHw-SLZga3PewEfgPz2s-mhp7NAz"
    session = requests.Session()
    # session.verify=False
    session.cookies.set("RAIL_EXPIRATION", RAIL_EXPIRATION)
    session.cookies.set("RAIL_DEVICEID", RAIL_DEVICEID)    
    
    
    try:
        #priceData = requests.get(priceUrl,headers=header)
        priceData = session.get(priceUrl,headers=header)
        #print(priceData)
        priceDict = priceData.json()['data']
        #print(priceDict)
        priceDict = dict(priceDict)
        #print(priceDict)
        A = priceDict.get('A9', '')  #商务座对应key:A9
        B = priceDict.get('M' , '')  #一等座对应key:M
        C = priceDict.get('0' , '')  #二等座对应key:0
        D = priceDict.get('A6', '')  #高级卧铺座对应key:A6
        E = priceDict.get('A4', '')  #软卧对应key:A4
        F = priceDict.get('F' , '')  #动卧对应key:F
        G = priceDict.get('A3', '')  #硬卧对应key:A3
        H = priceDict.get('A2', '')  #软座对应key:A2
        I = priceDict.get('A1', '')  #硬座对应key:A1
        J = priceDict.get('WZ', '')  #站票对应key:WZ
        #print(A,B,C,D,E,F,F,H,I,J)
                
    except:
        print('can\'t get tickets price. ')

    #return A[1:],B[1:],C[1:],D[1:],E[1:],F[1:],G[1:],H[1:],I[1:],J[1:]
    return A,B,C,D,E,F,G,H,I,J
