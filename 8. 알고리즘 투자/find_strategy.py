import sqlite3
import pandas as pd
import datetime
import pickle
import numpy as np
import scipy.stats.mstats
import matplotlib.pyplot as plt
import math
import time
import winsound
import os
import easygui

# 먼저 데이터를 불러오고(날짜는 datetime으로 바꾸자) -> 시점을 정한 다음 -> 시점에서 유니버스 생성 -> 유니버스 내부에서 조건에 맞는 종목 탐색해서 매수, 일정시점 이후 매도(2중 for문으로 종목 내 일자별, 종목별 반복), 수익률 계산(산술평균, 기하평균, 확률, 보유기간별, 연도별), 수익률 분포
# -> 그래프 그리기 (시장평균과 비교)

with open('dict.p', 'rb') as file:    # hello.txt 파일을 바이너리 읽기 모드(rb)로 열기
    dic = pickle.load(file)
    theme = pickle.load(file)

con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
cur = con.cursor()




account = []      #들고있는 종목에 대한 리스트(리스트로로 매수가, 경과일의 꼴로 저장)
earning_rate_1d = np.zeros(5326632)                                  #np.array([])    #하루 보유했을 떄 수익률의 리스트
earning_rate_1d_index = np.zeros(5326632)
dict_1d = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_3d = np.zeros(5326632)
earning_rate_3d_index = np.zeros(5326632)
dict_3d = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_1w = np.zeros(5326632)
earning_rate_1w_index = np.zeros(5326632)
dict_1w = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_2w = np.zeros(5326632)
earning_rate_2w_index = np.zeros(5326632)
dict_2w = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_1m = np.zeros(5326632)
earning_rate_1m_index = np.zeros(5326632)
dict_1m = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_3m = np.zeros(5326632)
earning_rate_3m_index = np.zeros(5326632)
dict_3m = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}
earning_rate_6m = np.zeros(5326632)
earning_rate_6m_index = np.zeros(5326632)
dict_6m = {'2007년' : -1, '2008년' : -1, '2009년' : -1, '2010년' : -1, '2011년' : -1, '2012년' : -1, '2013년' : -1, '2014년' : -1, '2015년' : -1, '2016년' : -1, '2017년' : -1, '2018년' : -1}

index_1d = 0
index_3d = 0
index_1w = 0
index_2w = 0
index_1m = 0
index_3m = 0
index_6m = 0

#매수 -> 리스트에 등록(내부에 튜플로 매수가, 경과일) -> 이후 매일 체크하는 함수(경과일 1씩 올리고, 정해진 경과일 지나면 1일, 3일, 1주일... 등 각각의 리스트에 수익률 더한다. 6달이 끝나면 리스트에서 삭제)

num_occurrence = [0,0,0,0,0,0,0,0,0,0,0,0]




def check(index, account, row) :
    global earning_rate_1d, earning_rate_3d, earning_rate_1w, earning_rate_2w, earning_rate_1m, earning_rate_3m, earning_rate_6m, index_1d, index_3d, index_1w, index_2w, index_1m, index_3m, index_6m, num_occurrence
    lapsed_over = []
    for i in account :
        i[1] += 1
        buy_price = i[0]
        lapsed_day = i[1]
        if lapsed_day == 1 :
            earning_rate_1d[index_1d] = calculate_earning(buy_price, row['close'])                                                                                                 #np.append(earning_rate_1d, calculate_earning(buy_price, row['close']))
            earning_rate_1d_index[index_1d] = int(index/10000)
            index_1d += 1
            #if dict_1d[str(int(index/10000))+'년'] == -1 :
            #    dict_1d[str(int(index / 10000)) + '년'] = index_1d-1                                                                          #len(earning_rate_1d)-1
        elif lapsed_day == 3 :
            earning_rate_3d[index_3d] = calculate_earning(buy_price, row['close'])
            earning_rate_3d_index[index_3d] = int(index / 10000)
            index_3d += 1
            #if dict_3d[str(int(index/10000))+'년'] == -1 :
            #    dict_3d[str(int(index / 10000)) + '년'] = index_3d-1
        elif lapsed_day == 5 :
            earning_rate_1w[index_1w] = calculate_earning(buy_price, row['close'])
            earning_rate_1w_index[index_1w] = int(index / 10000)
            index_1w += 1
            #if dict_1w[str(int(index/10000))+'년'] == -1 :
            #    dict_1w[str(int(index / 10000)) + '년'] = index_1w-1
        elif lapsed_day == 10 :
            earning_rate_2w[index_2w] = calculate_earning(buy_price, row['close'])
            earning_rate_2w_index[index_2w] = int(index / 10000)
            index_2w += 1
            #if dict_2w[str(int(index/10000))+'년'] == -1 :
            #    dict_2w[str(int(index / 10000)) + '년'] = index_2w-1
        elif lapsed_day == 20 :
            earning_rate_1m[index_1m] = calculate_earning(buy_price, row['close'])
            earning_rate_1m_index[index_1m] = int(index / 10000)
            index_1m += 1
            #if dict_1m[str(int(index/10000))+'년'] == -1 :
            #    dict_1m[str(int(index / 10000)) + '년'] = index_1m-1
        elif lapsed_day == 60 :
            earning_rate_3m[index_3m] = calculate_earning(buy_price, row['close'])
            earning_rate_3m_index[index_3m] = int(index / 10000)
            index_3m+=1
            #if dict_3m[str(int(index/10000))+'년'] == -1 :
            #    dict_3m[str(int(index / 10000)) + '년'] = index_3m-1
        elif lapsed_day == 120 :
            earning_rate_6m[index_6m] = calculate_earning(buy_price, row['close'])
            earning_rate_6m_index[index_6m] = int(index / 10000)
            index_6m+=1
            #if dict_6m[str(int(index/10000))+'년'] == -1 :
            #    dict_6m[str(int(index / 10000)) + '년'] = index_6m-1
            lapsed_over.append(i)
    for over in lapsed_over :
        account.remove(over)   #6달 지난건 계좌에서 삭제


def calculate_earning(buy_price, sell_price) :   #퍼센트가 아닌 수익률이다, 수수료와 세금 고려, 원금포함
    return (sell_price -sell_price*0.00315 -buy_price*0.00015)/buy_price



def market_strat(index, row) :   #그냥 사는 단순한 전략.. 시장 평균을 확인하기 위함
    account.append([row['open'],-1])      #매수 사인 // 바로 check함수에서 경과일이 1 더해질거니 경과일을 -1로 설정


def report_strat(index, row) :   #첫번쨰 전략 : 리포트가 하나라도 나오면 다음날 시가매수 1일, 3일, 1주일(5일), 2주일(10일), 1달(20일), 3달(60일), 6달(120일)동안의 경과를 보자  -> 3개 이상일 때도 보자
    if df.iloc[df.index.get_loc(index)-1]['num_report'] > 4 :
        account.append([row['open'],-1])      #매수 사인 // 바로 check함수에서 경과일이 1 더해질거니 경과일을 -1로 설정

def newreport_strat(index, row) :   #52주 new report
    if np.sum(df.iloc[df.index.get_loc(index)-22 : df.index.get_loc(index)-2]['num_report']) < 1 and df.iloc[df.index.get_loc(index)-1]['num_report'] > 1 :
        account.append([row['open'],-1])

def strong_strat(index, row) :
    if df.iloc[df.index.get_loc(index)-1]['StrongBuy'] > 1 :
        account.append([row['open'],-1])

def buy_strat(index, row) :     #스트롱바이랑 바이 합쳐서 계산
    if df.iloc[df.index.get_loc(index)-1]['StrongBuy'] + df.iloc[df.index.get_loc(index)-1]['Buy'] > 4 :
        account.append([row['open'],-1])

def tbuy_strat(index, row) :     #트레이딩바이 전략
    if df.iloc[df.index.get_loc(index)-1]['TradingBuy'] > 0 :
        account.append([row['open'],-1])

def nr_strat(index, row) :     #not rated 전략
    if df.iloc[df.index.get_loc(index)-1]['Not_Rated'] > 2 :
        account.append([row['open'],-1])

def tp_strat(index, row) :     #목표주가랑 종가랑 비교해서 계산
    if df.iloc[df.index.get_loc(index)-1]['TP'] != None and df.iloc[df.index.get_loc(index)-1]['TP'] > df.iloc[df.index.get_loc(index)-1]['nominal_price']*2 :
        account.append([row['open'],-1])

def stockholder_strat(index, row) :     #외인수급 3일이상 + -> 매수
    if df.iloc[df.index.get_loc(index)-1]['pension'] > 0 and df.iloc[df.index.get_loc(index)-2]['pension'] > 0 and df.iloc[df.index.get_loc(index)-3]['pension'] > 0 and df.iloc[df.index.get_loc(index)-4]['pension'] > 0 and df.iloc[df.index.get_loc(index)-5]['pension'] > 0 :
        account.append([row['open'],-1])

def new_high(index, row) :     #1달이내 처음 신고가 달성 / 최근 2달동안 저점에서 50%이상 안올라오고 달성
    if df.iloc[df.index.get_loc(index)-1]['52week_high'] > df.iloc[df.index.get_loc(index)-2]['52week_high'] == df.iloc[df.index.get_loc(index)-22]['52week_high'] and df.iloc[df.index.get_loc(index)-1]['52week_high'] < 1.15*np.min(df.iloc[df.index.get_loc(index)-42 : df.index.get_loc(index)-2 ]['low']) :
        account.append([row['open'],-1])

def bollinger_strat(index, row) :     #볼린저밴드 폭이 이평선의 20% 이하일 때
    if  df.iloc[df.index.get_loc(index)-1]['close'] < df.iloc[df.index.get_loc(index)-1]['bollinger_upper20'] < 1.03*df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index)-2]['close'] < df.iloc[df.index.get_loc(index)-2]['bollinger_upper20'] < 1.03*df.iloc[df.index.get_loc(index)-2]['close'] and df.iloc[df.index.get_loc(index)-3]['close'] < df.iloc[df.index.get_loc(index)-3]['bollinger_upper20'] < 1.03*df.iloc[df.index.get_loc(index)-3]['close'] and df.iloc[df.index.get_loc(index)-4]['close'] < df.iloc[df.index.get_loc(index)-4]['bollinger_upper20'] < 1.03*df.iloc[df.index.get_loc(index)-4]['close'] and df.iloc[df.index.get_loc(index)-5]['close'] < df.iloc[df.index.get_loc(index)-5]['bollinger_upper20'] < 1.03*df.iloc[df.index.get_loc(index)-5]['close'] and df.iloc[df.index.get_loc(index)-1]['52week_high'] < 1.05*df.iloc[df.index.get_loc(index)-1]['close']:
        account.append([row['open'],-1])

def correction(index, row) : #52주신고가 이후 조정받은다음에 다시 상승하는가?
    if 0.35 * df.iloc[df.index.get_loc(index)-1]['52week_high'] + 0.65 * df.iloc[df.index.get_loc(index)-1]['52week_low'] < df.iloc[df.index.get_loc(index)-1]['close'] < 0.4 * df.iloc[df.index.get_loc(index)-1]['52week_high'] + 0.6 * df.iloc[df.index.get_loc(index)-1]['52week_low'] and (df[df['52week_high'].astype('int') == df['high'].astype('int')].index.tolist()[-1] > df[df['52week_low'].astype('int') == df['low'].astype('int')].index.tolist()[-1]) :
        account.append([row['open'], -1])

def incPregnancy_strat(index, row) :     #상승잉태형
    if 0.95 * df.iloc[df.index.get_loc(index)-3]['open']  > df.iloc[df.index.get_loc(index)-3]['close'] and df.iloc[df.index.get_loc(index)-3]['close'] < df.iloc[df.index.get_loc(index)-2]['open'] < df.iloc[df.index.get_loc(index)-2]['close'] < df.iloc[df.index.get_loc(index)-3]['open']  and  df.iloc[df.index.get_loc(index)-3]['open'] < df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index)-1]['close']  > 1.05 * df.iloc[df.index.get_loc(index)-1]['open'] :
        account.append([row['open'],-1])

def invertedHammer_strat(index, row) :     #역망치형
    if 0.95 * df.iloc[df.index.get_loc(index)-2]['open']  > df.iloc[df.index.get_loc(index)-2]['close'] and ((df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['open'] and df.iloc[df.index.get_loc(index) - 1]['open'] * 1.03 > df.iloc[df.index.get_loc(index)-1]['close'] >  df.iloc[df.index.get_loc(index)-2]['close'] and df.iloc[df.index.get_loc(index)-1]['low'] > 0.99 * df.iloc[df.index.get_loc(index)-1]['open'] and df.iloc[df.index.get_loc(index)-1]['high'] - df.iloc[df.index.get_loc(index)-1]['close'] < 2 * (df.iloc[df.index.get_loc(index)-1]['close'] - df.iloc[df.index.get_loc(index)-1]['open'])) or (df.iloc[df.index.get_loc(index)-1]['open'] > df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index) - 1]['close'] * 1.03 > df.iloc[df.index.get_loc(index)-1]['open'] >  df.iloc[df.index.get_loc(index)-2]['close'] and df.iloc[df.index.get_loc(index)-1]['low'] > 0.99 * df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index)-1]['high'] - df.iloc[df.index.get_loc(index)-1]['open'] < 2 * (df.iloc[df.index.get_loc(index)-1]['open'] - df.iloc[df.index.get_loc(index)-1]['close']))) and df.iloc[df.index.get_loc(index)-1]['MA5'] < df.iloc[df.index.get_loc(index)-2]['MA5'] < df.iloc[df.index.get_loc(index)-3]['MA5']:
        account.append([row['open'],-1])

def cci_strat(index, row) :     #구름대랑 224일선 위에서 cci 과매도
    if df.iloc[df.index.get_loc(index)-1]['CCI9'] != None and df.iloc[df.index.get_loc(index)-2]['CCI9'] != None and df.iloc[df.index.get_loc(index)-1]['senkou_span_a'] != None and  df.iloc[df.index.get_loc(index)-1]['senkou_span_b'] != None and df.iloc[df.index.get_loc(index)-1]['MA224'] != None and df.iloc[df.index.get_loc(index)-2]['CCI9'] < -100 and df.iloc[df.index.get_loc(index)-1]['CCI9'] > -100 and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['MA224'] and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['senkou_span_a'] and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['senkou_span_b'] :
        account.append([row['open'],-1])

def rsi_strat(index, row) :     #구름대랑 224일선 위에서 rsi 과매도
    if df.iloc[df.index.get_loc(index)-1]['RSI14'] != None and df.iloc[df.index.get_loc(index)-2]['RSI14'] != None and df.iloc[df.index.get_loc(index)-1]['senkou_span_a'] != None and  df.iloc[df.index.get_loc(index)-1]['senkou_span_b'] != None and df.iloc[df.index.get_loc(index)-1]['MA224'] != None and df.iloc[df.index.get_loc(index)-2]['RSI14'] < 35 and df.iloc[df.index.get_loc(index)-1]['RSI14'] > 35 and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['MA224'] and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['senkou_span_a'] and df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['senkou_span_b'] :
        account.append([row['open'],-1])

def volume_strat(index, row) :
    if df.iloc[df.index.get_loc(index)-1]['VMA20'] != None and df.iloc[df.index.get_loc(index)-1]['volume'] > 5 * df.iloc[df.index.get_loc(index)-1]['VMA20'] and df.iloc[df.index.get_loc(index)-1]['close'] == df.iloc[df.index.get_loc(index)-1]['high']:
        account.append([row['open'],-1])

def invertedHammer_tp_strat(index, row) :     #역망치형
    if 0.95 * df.iloc[df.index.get_loc(index)-2]['open']  > df.iloc[df.index.get_loc(index)-2]['close'] and ((df.iloc[df.index.get_loc(index)-1]['close'] > df.iloc[df.index.get_loc(index)-1]['open'] and df.iloc[df.index.get_loc(index) - 1]['open'] * 1.03 > df.iloc[df.index.get_loc(index)-1]['close'] >  df.iloc[df.index.get_loc(index)-2]['close'] and df.iloc[df.index.get_loc(index)-1]['low'] > 0.99 * df.iloc[df.index.get_loc(index)-1]['open'] and df.iloc[df.index.get_loc(index)-1]['high'] - df.iloc[df.index.get_loc(index)-1]['close'] < 2 * (df.iloc[df.index.get_loc(index)-1]['close'] - df.iloc[df.index.get_loc(index)-1]['open'])) or (df.iloc[df.index.get_loc(index)-1]['open'] > df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index) - 1]['close'] * 1.03 > df.iloc[df.index.get_loc(index)-1]['open'] >  df.iloc[df.index.get_loc(index)-2]['close'] and df.iloc[df.index.get_loc(index)-1]['low'] > 0.99 * df.iloc[df.index.get_loc(index)-1]['close'] and df.iloc[df.index.get_loc(index)-1]['high'] - df.iloc[df.index.get_loc(index)-1]['open'] < 2 * (df.iloc[df.index.get_loc(index)-1]['open'] - df.iloc[df.index.get_loc(index)-1]['close']))) and df.iloc[df.index.get_loc(index)-1]['MA5'] < df.iloc[df.index.get_loc(index)-2]['MA5'] < df.iloc[df.index.get_loc(index)-3]['MA5'] and df.iloc[df.index.get_loc(index)-1]['52week_high'] > df.iloc[df.index.get_loc(index)-2]['52week_high'] == df.iloc[df.index.get_loc(index)-22]['52week_high'] and df.iloc[df.index.get_loc(index)-1]['52week_high'] < 3*np.min(df.iloc[df.index.get_loc(index)-42 : df.index.get_loc(index)-2 ]['low']) :
        account.append([row['open'],-1])


def initialize() :
    global index_1d, index_3d, index_1w, index_2w, index_1m, index_3m, index_6m, account, dict_1d, dict_3d, dict_1w, dict_2w, dict_1m, dict_3m, dict_6m
    account = []
    dict_1d = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_3d = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_1w = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_2w = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_1m = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_3m = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}
    dict_6m = {'2007년': -1, '2008년': -1, '2009년': -1, '2010년': -1, '2011년': -1, '2012년': -1, '2013년': -1, '2014년': -1,
               '2015년': -1, '2016년': -1, '2017년': -1, '2018년': -1}

occur_before_2007 = 0

earning_rate_per_year_1d = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_3d = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_1w = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_2w = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_1m = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_3m = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
earning_rate_per_year_6m = [np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([]),np.array([])]
occur_before_2007_not_1d = [0,0,0,0,0,0]


def cal_earning_rate_per_year():
    global earning_rate_per_year_1d, earning_rate_per_year_3d, earning_rate_per_year_1w, earning_rate_per_year_2w, earning_rate_per_year_1m, earning_rate_per_year_3m, earning_rate_per_year_6m, occur_before_2007_not_1d, dict_1d, dict_3d, dict_1w, dict_2w, dict_1m, dict_3m, dict_6m
    global earning_rate_1d, earning_rate_3d, earning_rate_1w, earning_rate_2w, earning_rate_1m, earning_rate_3m, earning_rate_6m, num_occurrence

    earning_rate_per_year_1d[0] = np.append(earning_rate_per_year_1d[0], earning_rate_1d[dict_1d["2007년"]: dict_1d["2008년"]])
    earning_rate_per_year_1d[1] = np.append(earning_rate_per_year_1d[1], earning_rate_1d[dict_1d["2008년"]: dict_1d["2009년"]])
    earning_rate_per_year_1d[2] = np.append(earning_rate_per_year_1d[2], earning_rate_1d[dict_1d["2009년"]: dict_1d["2010년"]])
    earning_rate_per_year_1d[3] = np.append(earning_rate_per_year_1d[3], earning_rate_1d[dict_1d["2010년"]: dict_1d["2011년"]])
    earning_rate_per_year_1d[4] = np.append(earning_rate_per_year_1d[4], earning_rate_1d[dict_1d["2011년"]: dict_1d["2012년"]])
    earning_rate_per_year_1d[5] = np.append(earning_rate_per_year_1d[5], earning_rate_1d[dict_1d["2012년"]: dict_1d["2013년"]])
    earning_rate_per_year_1d[6] = np.append(earning_rate_per_year_1d[6], earning_rate_1d[dict_1d["2013년"]: dict_1d["2014년"]])
    earning_rate_per_year_1d[7] = np.append(earning_rate_per_year_1d[7], earning_rate_1d[dict_1d["2014년"]: dict_1d["2015년"]])
    earning_rate_per_year_1d[8] = np.append(earning_rate_per_year_1d[8], earning_rate_1d[dict_1d["2015년"]: dict_1d["2016년"]])
    earning_rate_per_year_1d[9] = np.append(earning_rate_per_year_1d[9], earning_rate_1d[dict_1d["2016년"]: dict_1d["2017년"]])
    earning_rate_per_year_1d[10] = np.append(earning_rate_per_year_1d[10], earning_rate_1d[dict_1d["2017년"]: dict_1d["2018년"]])
    earning_rate_per_year_1d[11] = np.append(earning_rate_per_year_1d[11], earning_rate_1d[dict_1d["2018년"] : len(earning_rate_1d[earning_rate_1d > 0])])


    num_occurrence[0] = len(earning_rate_per_year_1d[0])
    num_occurrence[1] = len(earning_rate_per_year_1d[1])
    num_occurrence[2] = len(earning_rate_per_year_1d[2])
    num_occurrence[3] = len(earning_rate_per_year_1d[3])
    num_occurrence[4] = len(earning_rate_per_year_1d[4])
    num_occurrence[5] = len(earning_rate_per_year_1d[5])
    num_occurrence[6] = len(earning_rate_per_year_1d[6])
    num_occurrence[7] = len(earning_rate_per_year_1d[7])
    num_occurrence[8] = len(earning_rate_per_year_1d[8])
    num_occurrence[9] = len(earning_rate_per_year_1d[9])
    num_occurrence[10] = len(earning_rate_per_year_1d[10])
    num_occurrence[11] = len(earning_rate_per_year_1d[11])

    earning_rate_per_year_3d[0] = np.append(earning_rate_per_year_3d[0], earning_rate_3d[dict_3d["2007년"]: dict_3d["2008년"]])
    earning_rate_per_year_3d[1] = np.append(earning_rate_per_year_3d[1], earning_rate_3d[dict_3d["2008년"]: dict_3d["2009년"]])
    earning_rate_per_year_3d[2] = np.append(earning_rate_per_year_3d[2], earning_rate_3d[dict_3d["2009년"]: dict_3d["2010년"]])
    earning_rate_per_year_3d[3] = np.append(earning_rate_per_year_3d[3], earning_rate_3d[dict_3d["2010년"]: dict_3d["2011년"]])
    earning_rate_per_year_3d[4] = np.append(earning_rate_per_year_3d[4], earning_rate_3d[dict_3d["2011년"]: dict_3d["2012년"]])
    earning_rate_per_year_3d[5] = np.append(earning_rate_per_year_3d[5], earning_rate_3d[dict_3d["2012년"]: dict_3d["2013년"]])
    earning_rate_per_year_3d[6] = np.append(earning_rate_per_year_3d[6], earning_rate_3d[dict_3d["2013년"]: dict_3d["2014년"]])
    earning_rate_per_year_3d[7] = np.append(earning_rate_per_year_3d[7], earning_rate_3d[dict_3d["2014년"]: dict_3d["2015년"]])
    earning_rate_per_year_3d[8] = np.append(earning_rate_per_year_3d[8], earning_rate_3d[dict_3d["2015년"]: dict_3d["2016년"]])
    earning_rate_per_year_3d[9] = np.append(earning_rate_per_year_3d[9], earning_rate_3d[dict_3d["2016년"]: dict_3d["2017년"]])
    earning_rate_per_year_3d[10] = np.append(earning_rate_per_year_3d[10], earning_rate_3d[dict_3d["2017년"]: dict_3d["2018년"]])
    earning_rate_per_year_3d[11] = np.append(earning_rate_per_year_3d[11], earning_rate_3d[dict_3d["2018년"] : len(earning_rate_3d[earning_rate_3d > 0])])
    occur_before_2007_not_1d[0] = len(earning_rate_3d[earning_rate_3d > 0])

    earning_rate_per_year_1w[0] = np.append(earning_rate_per_year_1w[0], earning_rate_1w[dict_1w["2007년"] : dict_1w["2008년"]])
    earning_rate_per_year_1w[1] = np.append(earning_rate_per_year_1w[1], earning_rate_1w[dict_1w["2008년"]: dict_1w["2009년"]])
    earning_rate_per_year_1w[2] = np.append(earning_rate_per_year_1w[2], earning_rate_1w[dict_1w["2009년"]: dict_1w["2010년"]])
    earning_rate_per_year_1w[3] = np.append(earning_rate_per_year_1w[3], earning_rate_1w[dict_1w["2010년"]: dict_1w["2011년"]])
    earning_rate_per_year_1w[4] = np.append(earning_rate_per_year_1w[4], earning_rate_1w[dict_1w["2011년"]: dict_1w["2012년"]])
    earning_rate_per_year_1w[5] = np.append(earning_rate_per_year_1w[5], earning_rate_1w[dict_1w["2012년"]: dict_1w["2013년"]])
    earning_rate_per_year_1w[6] = np.append(earning_rate_per_year_1w[6], earning_rate_1w[dict_1w["2013년"]: dict_1w["2014년"]])
    earning_rate_per_year_1w[7] = np.append(earning_rate_per_year_1w[7], earning_rate_1w[dict_1w["2014년"]: dict_1w["2015년"]])
    earning_rate_per_year_1w[8] = np.append(earning_rate_per_year_1w[8], earning_rate_1w[dict_1w["2015년"]: dict_1w["2016년"]])
    earning_rate_per_year_1w[9] = np.append(earning_rate_per_year_1w[9], earning_rate_1w[dict_1w["2016년"]: dict_1w["2017년"]])
    earning_rate_per_year_1w[10] = np.append(earning_rate_per_year_1w[10], earning_rate_1w[dict_1w["2017년"]: dict_1w["2018년"]])
    earning_rate_per_year_1w[11] = np.append(earning_rate_per_year_1w[11], earning_rate_1w[dict_1w["2018년"] : len(earning_rate_1w[earning_rate_1w > 0])])
    occur_before_2007_not_1d[1] = len(earning_rate_1w[earning_rate_1w > 0])

    earning_rate_per_year_2w[0] = np.append(earning_rate_per_year_2w[0], earning_rate_2w[dict_2w["2007년"] : dict_2w["2008년"]])
    earning_rate_per_year_2w[1] = np.append(earning_rate_per_year_2w[1], earning_rate_2w[dict_2w["2008년"]: dict_2w["2009년"]])
    earning_rate_per_year_2w[2] = np.append(earning_rate_per_year_2w[2], earning_rate_2w[dict_2w["2009년"]: dict_2w["2010년"]])
    earning_rate_per_year_2w[3] = np.append(earning_rate_per_year_2w[3], earning_rate_2w[dict_2w["2010년"]: dict_2w["2011년"]])
    earning_rate_per_year_2w[4] = np.append(earning_rate_per_year_2w[4], earning_rate_2w[dict_2w["2011년"]: dict_2w["2012년"]])
    earning_rate_per_year_2w[5] = np.append(earning_rate_per_year_2w[5], earning_rate_2w[dict_2w["2012년"]: dict_2w["2013년"]])
    earning_rate_per_year_2w[6] = np.append(earning_rate_per_year_2w[6], earning_rate_2w[dict_2w["2013년"]: dict_2w["2014년"]])
    earning_rate_per_year_2w[7] = np.append(earning_rate_per_year_2w[7], earning_rate_2w[dict_2w["2014년"]: dict_2w["2015년"]])
    earning_rate_per_year_2w[8] = np.append(earning_rate_per_year_2w[8], earning_rate_2w[dict_2w["2015년"]: dict_2w["2016년"]])
    earning_rate_per_year_2w[9] = np.append(earning_rate_per_year_2w[9], earning_rate_2w[dict_2w["2016년"]: dict_2w["2017년"]])
    earning_rate_per_year_2w[10] = np.append(earning_rate_per_year_2w[10], earning_rate_2w[dict_2w["2017년"]: dict_2w["2018년"]])
    earning_rate_per_year_2w[11] = np.append(earning_rate_per_year_2w[11], earning_rate_2w[dict_2w["2018년"]: len(earning_rate_2w[earning_rate_2w > 0])])
    occur_before_2007_not_1d[2] = len(earning_rate_2w[earning_rate_2w > 0])

    earning_rate_per_year_1m[0] = np.append(earning_rate_per_year_1m[0], earning_rate_1m[dict_1m["2007년"] : dict_1m["2008년"]])
    earning_rate_per_year_1m[1] = np.append(earning_rate_per_year_1m[1], earning_rate_1m[dict_1m["2008년"]: dict_1m["2009년"]])
    earning_rate_per_year_1m[2] = np.append(earning_rate_per_year_1m[2], earning_rate_1m[dict_1m["2009년"]: dict_1m["2010년"]])
    earning_rate_per_year_1m[3] = np.append(earning_rate_per_year_1m[3], earning_rate_1m[dict_1m["2010년"]: dict_1m["2011년"]])
    earning_rate_per_year_1m[4] = np.append(earning_rate_per_year_1m[4], earning_rate_1m[dict_1m["2011년"]: dict_1m["2012년"]])
    earning_rate_per_year_1m[5] = np.append(earning_rate_per_year_1m[5], earning_rate_1m[dict_1m["2012년"]: dict_1m["2013년"]])
    earning_rate_per_year_1m[6] = np.append(earning_rate_per_year_1m[6], earning_rate_1m[dict_1m["2013년"]: dict_1m["2014년"]])
    earning_rate_per_year_1m[7] = np.append(earning_rate_per_year_1m[7], earning_rate_1m[dict_1m["2014년"]: dict_1m["2015년"]])
    earning_rate_per_year_1m[8] = np.append(earning_rate_per_year_1m[8], earning_rate_1m[dict_1m["2015년"]: dict_1m["2016년"]])
    earning_rate_per_year_1m[9] = np.append(earning_rate_per_year_1m[9], earning_rate_1m[dict_1m["2016년"]: dict_1m["2017년"]])
    earning_rate_per_year_1m[10] = np.append(earning_rate_per_year_1m[10], earning_rate_1m[dict_1m["2017년"]: dict_1m["2018년"]])
    earning_rate_per_year_1m[11] = np.append(earning_rate_per_year_1m[11], earning_rate_1m[dict_1m["2018년"] : len(earning_rate_1m[earning_rate_1m > 0])])
    occur_before_2007_not_1d[3] = len(earning_rate_1m[earning_rate_1m > 0])

    earning_rate_per_year_3m[0] = np.append(earning_rate_per_year_3m[0], earning_rate_3m[dict_3m["2007년"] : dict_3m["2008년"]])
    earning_rate_per_year_3m[1] = np.append(earning_rate_per_year_3m[1], earning_rate_3m[dict_3m["2008년"]: dict_3m["2009년"]])
    earning_rate_per_year_3m[2] = np.append(earning_rate_per_year_3m[2], earning_rate_3m[dict_3m["2009년"]: dict_3m["2010년"]])
    earning_rate_per_year_3m[3] = np.append(earning_rate_per_year_3m[3], earning_rate_3m[dict_3m["2010년"]: dict_3m["2011년"]])
    earning_rate_per_year_3m[4] = np.append(earning_rate_per_year_3m[4], earning_rate_3m[dict_3m["2011년"]: dict_3m["2012년"]])
    earning_rate_per_year_3m[5] = np.append(earning_rate_per_year_3m[5], earning_rate_3m[dict_3m["2012년"]: dict_3m["2013년"]])
    earning_rate_per_year_3m[6] = np.append(earning_rate_per_year_3m[6], earning_rate_3m[dict_3m["2013년"]: dict_3m["2014년"]])
    earning_rate_per_year_3m[7] = np.append(earning_rate_per_year_3m[7], earning_rate_3m[dict_3m["2014년"]: dict_3m["2015년"]])
    earning_rate_per_year_3m[8] = np.append(earning_rate_per_year_3m[8], earning_rate_3m[dict_3m["2015년"]: dict_3m["2016년"]])
    earning_rate_per_year_3m[9] = np.append(earning_rate_per_year_3m[9], earning_rate_3m[dict_3m["2016년"]: dict_3m["2017년"]])
    earning_rate_per_year_3m[10] = np.append(earning_rate_per_year_3m[10], earning_rate_3m[dict_3m["2017년"]: dict_3m["2018년"]])
    earning_rate_per_year_3m[11] = np.append(earning_rate_per_year_3m[11], earning_rate_3m[dict_3m["2018년"]: len(earning_rate_3m[earning_rate_3m > 0])])
    occur_before_2007_not_1d[4] = len(earning_rate_3m[earning_rate_3m > 0])

    earning_rate_per_year_6m[0] = np.append(earning_rate_per_year_6m[0], earning_rate_6m[dict_6m["2007년"] : dict_6m["2008년"]])
    earning_rate_per_year_6m[1] = np.append(earning_rate_per_year_6m[1], earning_rate_6m[dict_6m["2008년"]: dict_6m["2009년"]])
    earning_rate_per_year_6m[2] = np.append(earning_rate_per_year_6m[2], earning_rate_6m[dict_6m["2009년"]: dict_6m["2010년"]])
    earning_rate_per_year_6m[3] = np.append(earning_rate_per_year_6m[3], earning_rate_6m[dict_6m["2010년"]: dict_6m["2011년"]])
    earning_rate_per_year_6m[4] = np.append(earning_rate_per_year_6m[4], earning_rate_6m[dict_6m["2011년"]: dict_6m["2012년"]])
    earning_rate_per_year_6m[5] = np.append(earning_rate_per_year_6m[5], earning_rate_6m[dict_6m["2012년"]: dict_6m["2013년"]])
    earning_rate_per_year_6m[6] = np.append(earning_rate_per_year_6m[6], earning_rate_6m[dict_6m["2013년"]: dict_6m["2014년"]])
    earning_rate_per_year_6m[7] = np.append(earning_rate_per_year_6m[7], earning_rate_6m[dict_6m["2014년"]: dict_6m["2015년"]])
    earning_rate_per_year_6m[8] = np.append(earning_rate_per_year_6m[8], earning_rate_6m[dict_6m["2015년"]: dict_6m["2016년"]])
    earning_rate_per_year_6m[9] = np.append(earning_rate_per_year_6m[9], earning_rate_6m[dict_6m["2016년"]: dict_6m["2017년"]])
    earning_rate_per_year_6m[10] = np.append(earning_rate_per_year_6m[10], earning_rate_6m[dict_6m["2017년"]: dict_6m["2018년"]])
    earning_rate_per_year_6m[11] = np.append(earning_rate_per_year_6m[11], earning_rate_6m[dict_6m["2018년"]: len(earning_rate_6m[earning_rate_6m > 0])])
    occur_before_2007_not_1d[5] = len(earning_rate_6m[earning_rate_6m > 0])


start_day_init = '20060601'  #2007년에 시작하는데 1년전꺼부터 불러옴
for i, code in enumerate(dic) :
    initialize()
    print(i)
    if int(dic[code]['date']) <= int(start_day_init)+1000 :
        start_day = start_day_init
    else :
        start_day = dic[code]['date']
    df = pd.read_sql('SELECT * FROM "%s" WHERE "index" >= %s' % (code, start_day), con, index_col='index')
    for index, row in df.loc[int(start_day)+10000 : ].iterrows() :                #이것이 메인루프, 상장한지 1년 이상 지난 종목만 본다
        #report_strat(index, row)   # 리포트전략
        #market_strat(index, row)   #시장 평균
        #strong_strat(index, row)  #스트롱바이 전략
        #buy_strat(index, row)    #바이 전략
        #tp_strat(index, row)      #TP 전략
        #stockholder_strat(index, row)  #수급 전략
        #tbuy_strat(index, row)  # 트레이딩바이 전략
        #nr_strat(index, row)   #nr 전략
        #new_high(index, row) #신고가 달성
        #bollinger_strat(index, row) # 볼린저밴드 전략
        #correction(index, row) # 52주 신고가에서 조정받으면 다시 매수 - 코드오류로 일단 실행못함
        #incPregnancy_strat(index, row) # 상승잉태형
        #invertedHammer_strat(index, row) # 역망치형
        #cci_strat(index, row) #cci 전략
        #rsi_strat(index, row)  # rsi 전략
        #newreport_strat(index, row)  # 52주 new report
        #volume_strat(index, row)  # 거래량지표
        invertedHammer_tp_strat(index, row)  # 역망치형 + tp
        check(index, account, row)
    #cal_earning_rate_per_year()

earning_rate_per_year_1d[0] = np.append(earning_rate_per_year_1d[0], earning_rate_1d[earning_rate_1d_index == 2007])
earning_rate_per_year_1d[1] = np.append(earning_rate_per_year_1d[1], earning_rate_1d[earning_rate_1d_index == 2008])
earning_rate_per_year_1d[2] = np.append(earning_rate_per_year_1d[2], earning_rate_1d[earning_rate_1d_index == 2009])
earning_rate_per_year_1d[3] = np.append(earning_rate_per_year_1d[3], earning_rate_1d[earning_rate_1d_index == 2010])
earning_rate_per_year_1d[4] = np.append(earning_rate_per_year_1d[4], earning_rate_1d[earning_rate_1d_index == 2011])
earning_rate_per_year_1d[5] = np.append(earning_rate_per_year_1d[5], earning_rate_1d[earning_rate_1d_index == 2012])
earning_rate_per_year_1d[6] = np.append(earning_rate_per_year_1d[6], earning_rate_1d[earning_rate_1d_index == 2013])
earning_rate_per_year_1d[7] = np.append(earning_rate_per_year_1d[7], earning_rate_1d[earning_rate_1d_index == 2014])
earning_rate_per_year_1d[8] = np.append(earning_rate_per_year_1d[8], earning_rate_1d[earning_rate_1d_index == 2015])
earning_rate_per_year_1d[9] = np.append(earning_rate_per_year_1d[9], earning_rate_1d[earning_rate_1d_index == 2016])
earning_rate_per_year_1d[10] = np.append(earning_rate_per_year_1d[10], earning_rate_1d[earning_rate_1d_index == 2017])
earning_rate_per_year_1d[11] = np.append(earning_rate_per_year_1d[11], earning_rate_1d[earning_rate_1d_index == 2018])


num_occurrence[0] = len(earning_rate_per_year_1d[0])
num_occurrence[1] = len(earning_rate_per_year_1d[1])
num_occurrence[2] = len(earning_rate_per_year_1d[2])
num_occurrence[3] = len(earning_rate_per_year_1d[3])
num_occurrence[4] = len(earning_rate_per_year_1d[4])
num_occurrence[5] = len(earning_rate_per_year_1d[5])
num_occurrence[6] = len(earning_rate_per_year_1d[6])
num_occurrence[7] = len(earning_rate_per_year_1d[7])
num_occurrence[8] = len(earning_rate_per_year_1d[8])
num_occurrence[9] = len(earning_rate_per_year_1d[9])
num_occurrence[10] = len(earning_rate_per_year_1d[10])
num_occurrence[11] = len(earning_rate_per_year_1d[11])

earning_rate_per_year_3d[0] = np.append(earning_rate_per_year_3d[0], earning_rate_3d[earning_rate_3d_index == 2007])
earning_rate_per_year_3d[1] = np.append(earning_rate_per_year_3d[1], earning_rate_3d[earning_rate_3d_index == 2008])
earning_rate_per_year_3d[2] = np.append(earning_rate_per_year_3d[2], earning_rate_3d[earning_rate_3d_index == 2009])
earning_rate_per_year_3d[3] = np.append(earning_rate_per_year_3d[3], earning_rate_3d[earning_rate_3d_index == 2010])
earning_rate_per_year_3d[4] = np.append(earning_rate_per_year_3d[4], earning_rate_3d[earning_rate_3d_index == 2011])
earning_rate_per_year_3d[5] = np.append(earning_rate_per_year_3d[5], earning_rate_3d[earning_rate_3d_index == 2012])
earning_rate_per_year_3d[6] = np.append(earning_rate_per_year_3d[6], earning_rate_3d[earning_rate_3d_index == 2013])
earning_rate_per_year_3d[7] = np.append(earning_rate_per_year_3d[7], earning_rate_3d[earning_rate_3d_index == 2014])
earning_rate_per_year_3d[8] = np.append(earning_rate_per_year_3d[8], earning_rate_3d[earning_rate_3d_index == 2015])
earning_rate_per_year_3d[9] = np.append(earning_rate_per_year_3d[9], earning_rate_3d[earning_rate_3d_index == 2016])
earning_rate_per_year_3d[10] = np.append(earning_rate_per_year_3d[10], earning_rate_3d[earning_rate_3d_index == 2017])
earning_rate_per_year_3d[11] = np.append(earning_rate_per_year_3d[11], earning_rate_3d[earning_rate_3d_index == 2018])
occur_before_2007_not_1d[0] = len(earning_rate_3d[earning_rate_3d > 0])

earning_rate_per_year_1w[0] = np.append(earning_rate_per_year_1w[0], earning_rate_1w[earning_rate_1w_index == 2007])
earning_rate_per_year_1w[1] = np.append(earning_rate_per_year_1w[1], earning_rate_1w[earning_rate_1w_index == 2008])
earning_rate_per_year_1w[2] = np.append(earning_rate_per_year_1w[2], earning_rate_1w[earning_rate_1w_index == 2009])
earning_rate_per_year_1w[3] = np.append(earning_rate_per_year_1w[3], earning_rate_1w[earning_rate_1w_index == 2010])
earning_rate_per_year_1w[4] = np.append(earning_rate_per_year_1w[4], earning_rate_1w[earning_rate_1w_index == 2011])
earning_rate_per_year_1w[5] = np.append(earning_rate_per_year_1w[5], earning_rate_1w[earning_rate_1w_index == 2012])
earning_rate_per_year_1w[6] = np.append(earning_rate_per_year_1w[6], earning_rate_1w[earning_rate_1w_index == 2013])
earning_rate_per_year_1w[7] = np.append(earning_rate_per_year_1w[7], earning_rate_1w[earning_rate_1w_index == 2014])
earning_rate_per_year_1w[8] = np.append(earning_rate_per_year_1w[8], earning_rate_1w[earning_rate_1w_index == 2015])
earning_rate_per_year_1w[9] = np.append(earning_rate_per_year_1w[9], earning_rate_1w[earning_rate_1w_index == 2016])
earning_rate_per_year_1w[10] = np.append(earning_rate_per_year_1w[10], earning_rate_1w[earning_rate_1w_index == 2017])
earning_rate_per_year_1w[11] = np.append(earning_rate_per_year_1w[11], earning_rate_1w[earning_rate_1w_index == 2018])
occur_before_2007_not_1d[1] = len(earning_rate_1w[earning_rate_1w > 0])

earning_rate_per_year_2w[0] = np.append(earning_rate_per_year_2w[0], earning_rate_2w[earning_rate_2w_index == 2007])
earning_rate_per_year_2w[1] = np.append(earning_rate_per_year_2w[1], earning_rate_2w[earning_rate_2w_index == 2008])
earning_rate_per_year_2w[2] = np.append(earning_rate_per_year_2w[2], earning_rate_2w[earning_rate_2w_index == 2009])
earning_rate_per_year_2w[3] = np.append(earning_rate_per_year_2w[3], earning_rate_2w[earning_rate_2w_index == 2010])
earning_rate_per_year_2w[4] = np.append(earning_rate_per_year_2w[4], earning_rate_2w[earning_rate_2w_index == 2011])
earning_rate_per_year_2w[5] = np.append(earning_rate_per_year_2w[5], earning_rate_2w[earning_rate_2w_index == 2012])
earning_rate_per_year_2w[6] = np.append(earning_rate_per_year_2w[6], earning_rate_2w[earning_rate_2w_index == 2013])
earning_rate_per_year_2w[7] = np.append(earning_rate_per_year_2w[7], earning_rate_2w[earning_rate_2w_index == 2014])
earning_rate_per_year_2w[8] = np.append(earning_rate_per_year_2w[8], earning_rate_2w[earning_rate_2w_index == 2015])
earning_rate_per_year_2w[9] = np.append(earning_rate_per_year_2w[9], earning_rate_2w[earning_rate_2w_index == 2016])
earning_rate_per_year_2w[10] = np.append(earning_rate_per_year_2w[10], earning_rate_2w[earning_rate_2w_index == 2017])
earning_rate_per_year_2w[11] = np.append(earning_rate_per_year_2w[11], earning_rate_2w[earning_rate_2w_index == 2018])
occur_before_2007_not_1d[2] = len(earning_rate_2w[earning_rate_2w > 0])

earning_rate_per_year_1m[0] = np.append(earning_rate_per_year_1m[0], earning_rate_1m[earning_rate_1m_index == 2007])
earning_rate_per_year_1m[1] = np.append(earning_rate_per_year_1m[1], earning_rate_1m[earning_rate_1m_index == 2008])
earning_rate_per_year_1m[2] = np.append(earning_rate_per_year_1m[2], earning_rate_1m[earning_rate_1m_index == 2009])
earning_rate_per_year_1m[3] = np.append(earning_rate_per_year_1m[3], earning_rate_1m[earning_rate_1m_index == 2010])
earning_rate_per_year_1m[4] = np.append(earning_rate_per_year_1m[4], earning_rate_1m[earning_rate_1m_index == 2011])
earning_rate_per_year_1m[5] = np.append(earning_rate_per_year_1m[5], earning_rate_1m[earning_rate_1m_index == 2012])
earning_rate_per_year_1m[6] = np.append(earning_rate_per_year_1m[6], earning_rate_1m[earning_rate_1m_index == 2013])
earning_rate_per_year_1m[7] = np.append(earning_rate_per_year_1m[7], earning_rate_1m[earning_rate_1m_index == 2014])
earning_rate_per_year_1m[8] = np.append(earning_rate_per_year_1m[8], earning_rate_1m[earning_rate_1m_index == 2015])
earning_rate_per_year_1m[9] = np.append(earning_rate_per_year_1m[9], earning_rate_1m[earning_rate_1m_index == 2016])
earning_rate_per_year_1m[10] = np.append(earning_rate_per_year_1m[10], earning_rate_1m[earning_rate_1m_index == 2017])
earning_rate_per_year_1m[11] = np.append(earning_rate_per_year_1m[11], earning_rate_1m[earning_rate_1m_index == 2018])
occur_before_2007_not_1d[3] = len(earning_rate_1m[earning_rate_1m > 0])

earning_rate_per_year_3m[0] = np.append(earning_rate_per_year_3m[0], earning_rate_3m[earning_rate_3m_index == 2007])
earning_rate_per_year_3m[1] = np.append(earning_rate_per_year_3m[1], earning_rate_3m[earning_rate_3m_index == 2008])
earning_rate_per_year_3m[2] = np.append(earning_rate_per_year_3m[2], earning_rate_3m[earning_rate_3m_index == 2009])
earning_rate_per_year_3m[3] = np.append(earning_rate_per_year_3m[3], earning_rate_3m[earning_rate_3m_index == 2010])
earning_rate_per_year_3m[4] = np.append(earning_rate_per_year_3m[4], earning_rate_3m[earning_rate_3m_index == 2011])
earning_rate_per_year_3m[5] = np.append(earning_rate_per_year_3m[5], earning_rate_3m[earning_rate_3m_index == 2012])
earning_rate_per_year_3m[6] = np.append(earning_rate_per_year_3m[6], earning_rate_3m[earning_rate_3m_index == 2013])
earning_rate_per_year_3m[7] = np.append(earning_rate_per_year_3m[7], earning_rate_3m[earning_rate_3m_index == 2014])
earning_rate_per_year_3m[8] = np.append(earning_rate_per_year_3m[8], earning_rate_3m[earning_rate_3m_index == 2015])
earning_rate_per_year_3m[9] = np.append(earning_rate_per_year_3m[9], earning_rate_3m[earning_rate_3m_index == 2016])
earning_rate_per_year_3m[10] = np.append(earning_rate_per_year_3m[10], earning_rate_3m[earning_rate_3m_index == 2017])
earning_rate_per_year_3m[11] = np.append(earning_rate_per_year_3m[11], earning_rate_3m[earning_rate_3m_index == 2018])
occur_before_2007_not_1d[4] = len(earning_rate_3m[earning_rate_3m > 0])

earning_rate_per_year_6m[0] = np.append(earning_rate_per_year_6m[0], earning_rate_6m[earning_rate_6m_index == 2007])
earning_rate_per_year_6m[1] = np.append(earning_rate_per_year_6m[1], earning_rate_6m[earning_rate_6m_index == 2008])
earning_rate_per_year_6m[2] = np.append(earning_rate_per_year_6m[2], earning_rate_6m[earning_rate_6m_index == 2009])
earning_rate_per_year_6m[3] = np.append(earning_rate_per_year_6m[3], earning_rate_6m[earning_rate_6m_index == 2010])
earning_rate_per_year_6m[4] = np.append(earning_rate_per_year_6m[4], earning_rate_6m[earning_rate_6m_index == 2011])
earning_rate_per_year_6m[5] = np.append(earning_rate_per_year_6m[5], earning_rate_6m[earning_rate_6m_index == 2012])
earning_rate_per_year_6m[6] = np.append(earning_rate_per_year_6m[6], earning_rate_6m[earning_rate_6m_index == 2013])
earning_rate_per_year_6m[7] = np.append(earning_rate_per_year_6m[7], earning_rate_6m[earning_rate_6m_index == 2014])
earning_rate_per_year_6m[8] = np.append(earning_rate_per_year_6m[8], earning_rate_6m[earning_rate_6m_index == 2015])
earning_rate_per_year_6m[9] = np.append(earning_rate_per_year_6m[9], earning_rate_6m[earning_rate_6m_index == 2016])
earning_rate_per_year_6m[10] = np.append(earning_rate_per_year_6m[10], earning_rate_6m[earning_rate_6m_index == 2017])
earning_rate_per_year_6m[11] = np.append(earning_rate_per_year_6m[11], earning_rate_6m[earning_rate_6m_index == 2018])
occur_before_2007_not_1d[5] = len(earning_rate_6m[earning_rate_6m > 0])

















earning_rate_1d = earning_rate_1d[earning_rate_1d>0]
earning_rate_3d = earning_rate_3d[earning_rate_3d>0]
earning_rate_1w = earning_rate_1w[earning_rate_1w>0]
earning_rate_2w = earning_rate_2w[earning_rate_2w>0]
earning_rate_1m = earning_rate_1m[earning_rate_1m>0]
earning_rate_3m = earning_rate_3m[earning_rate_3m>0]
earning_rate_6m = earning_rate_6m[earning_rate_6m>0]

with open('market_avg.p', 'rb') as file:    # hello.txt 파일을 바이너리 읽기 모드(rb)로 열기
    market_total_arithmetic_mean = pickle.load(file)
    market_total_geometric_mean = pickle.load(file)
    market_total_inc_prob = pickle.load(file)
    market_arithmetic_mean_3d = pickle.load(file)
    market_geometric_mean_3d = pickle.load(file)
    market_arithmetic_mean_1w = pickle.load(file)
    market_geometric_mean_1w = pickle.load(file)
    market_arithmetic_mean_2w = pickle.load(file)
    market_geometric_mean_2w = pickle.load(file)
    market_arithmetic_mean_1m = pickle.load(file)
    market_geometric_mean_1m = pickle.load(file)
    market_arithmetic_mean_3m = pickle.load(file)
    market_geometric_mean_3m = pickle.load(file)
    market_arithmetic_mean_6m = pickle.load(file)
    market_geometric_mean_6m = pickle.load(file)



total_arithmetic_mean_1d = np.mean(earning_rate_1d)-1       #1일경과 산술평균
total_geometric_mean_1d = scipy.stats.mstats.gmean(earning_rate_1d)-1    #1일경과 기하평균
total_inc_prob_1d = np.count_nonzero(earning_rate_1d > 1)/len(earning_rate_1d)   #1일경과 상승 확률

total_arithmetic_mean_3d = np.mean(earning_rate_3d)-1
total_geometric_mean_3d = scipy.stats.mstats.gmean(earning_rate_3d)-1
total_inc_prob_3d = np.count_nonzero(earning_rate_3d > 1)/len(earning_rate_3d)

total_arithmetic_mean_1w = np.mean(earning_rate_1w)-1
total_geometric_mean_1w = scipy.stats.mstats.gmean(earning_rate_1w)-1
total_inc_prob_1w = np.count_nonzero(earning_rate_1w > 1)/len(earning_rate_1w)

total_arithmetic_mean_2w = np.mean(earning_rate_2w)-1
total_geometric_mean_2w = scipy.stats.mstats.gmean(earning_rate_2w)-1
total_inc_prob_2w = np.count_nonzero(earning_rate_2w > 1)/len(earning_rate_2w)

total_arithmetic_mean_1m = np.mean(earning_rate_1m)-1
total_geometric_mean_1m = scipy.stats.mstats.gmean(earning_rate_1m)-1
total_inc_prob_1m = np.count_nonzero(earning_rate_1m > 1)/len(earning_rate_1m)

total_arithmetic_mean_3m = np.mean(earning_rate_3m)-1
total_geometric_mean_3m = scipy.stats.mstats.gmean(earning_rate_3m)-1
total_inc_prob_3m = np.count_nonzero(earning_rate_3m > 1)/len(earning_rate_3m)

total_arithmetic_mean_6m = np.mean(earning_rate_6m)-1
total_geometric_mean_6m = scipy.stats.mstats.gmean(earning_rate_6m)-1
total_inc_prob_6m = np.count_nonzero(earning_rate_6m > 1)/len(earning_rate_6m)

total_arithmetic_mean = [total_arithmetic_mean_1d*100, total_arithmetic_mean_3d*100, total_arithmetic_mean_1w*100,total_arithmetic_mean_2w*100,total_arithmetic_mean_1m*100,total_arithmetic_mean_3m*100,total_arithmetic_mean_6m*100] #1 뺴고 100 곱해야지
total_arithmetic_mean = [round(float(i),2) for i in total_arithmetic_mean]
total_geometric_mean = [total_geometric_mean_1d*100, total_geometric_mean_3d*100, total_geometric_mean_1w*100,total_geometric_mean_2w*100,total_geometric_mean_1m*100,total_geometric_mean_3m*100,total_geometric_mean_6m*100]
total_geometric_mean = [round(float(i),2) for i in total_geometric_mean]
total_inc_prob = [total_inc_prob_1d*100, total_inc_prob_3d*100, total_inc_prob_1w*100, total_inc_prob_2w*100, total_inc_prob_1m*100, total_inc_prob_3m*100, total_inc_prob_6m*100]
total_inc_prob = [round(i,2) for i in total_inc_prob]

total_index = ['a_1d', 'b_3d', 'c_1w', 'd_2w', 'e_1m', 'f_3m', 'g_6m']

winsound.Beep(500,5000)


dir = 'C:/Users/김세윤/Desktop/전략/strat'
os.mkdir(dir)

f = open(dir + '/report.txt', 'w')




print("전체 수익률 산술평균 : ",total_arithmetic_mean)
f.write("전체 수익률 산술평균 : "+str(total_arithmetic_mean) + "\n\n")
plt.plot(total_index, total_arithmetic_mean, 'rs--', label = 'strategy')
plt.plot(total_index, market_total_arithmetic_mean, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('total arithmetic mean')
plt.savefig(dir + '/1.png')
plt.show()

print("전체 수익률 기하평균 : ", total_geometric_mean)
f.write("전체 수익률 기하평균 : "+str(total_geometric_mean) + "\n\n")
plt.plot(total_index, total_geometric_mean, 'rs--', label = 'strategy')
plt.plot(total_index, market_total_geometric_mean, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('total geometric mean')
plt.savefig(dir + '/2.png')
plt.show()

print("전체 상승확률 : ", total_inc_prob)
f.write("전체 상승확률 : "+str(total_inc_prob) + "\n\n")
plt.plot(total_index, total_inc_prob, 'rs--', label = 'strategy')
plt.plot(total_index, market_total_inc_prob, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('total probability of increses')
plt.savefig(dir + '/3.png')
plt.show()




year_index = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

#3일치 연도별
arithmetic_mean_3d = []
geometric_mean_3d = []

for year in year_index :
    arithmetic_mean_3d.append((np.mean(earning_rate_per_year_3d[year-2007])-1)*100)
    geometric_mean_3d.append((scipy.stats.mstats.gmean(earning_rate_per_year_3d[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_3d) :
    if math.isnan(v) :
        arithmetic_mean_3d[i] = 0
for i, v in enumerate(geometric_mean_3d) :
    if math.isnan(v) :
        geometric_mean_3d[i] = 0
arithmetic_mean_3d = [round(float(i),2) for i in arithmetic_mean_3d]
geometric_mean_3d = [round(float(i),2) for i in geometric_mean_3d]


print("연도별 3일치 산술평균 : ", arithmetic_mean_3d)
f.write("연도별 3일치 산술평균 : "+str(arithmetic_mean_3d) + "\n\n")
plt.plot(year_index, arithmetic_mean_3d, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_3d, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 3d')
plt.savefig(dir + '/4.png')
plt.show()

print("연도별 3일치 기하평균 : ", geometric_mean_3d)
f.write("연도별 3일치 기하평균 : "+str(geometric_mean_3d) + "\n\n")
plt.plot(year_index, geometric_mean_3d, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_3d, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 3d')
plt.savefig(dir + '/5.png')
plt.show()


#1주일
arithmetic_mean_1w = []
geometric_mean_1w = []

for year in year_index :
    arithmetic_mean_1w.append((np.mean(earning_rate_per_year_1w[year-2007])-1)*100)
    geometric_mean_1w.append((scipy.stats.mstats.gmean(earning_rate_per_year_1w[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_1w) :
    if math.isnan(v) :
        arithmetic_mean_1w[i] = 0
for i, v in enumerate(geometric_mean_1w) :
    if math.isnan(v) :
        geometric_mean_1w[i] = 0

arithmetic_mean_1w = [round(float(i),2) for i in arithmetic_mean_1w]
geometric_mean_1w = [round(float(i),2) for i in geometric_mean_1w]

print("연도별 1주일치 산술평균 : ", arithmetic_mean_1w)
f.write("연도별 1주일치 산술평균 : "+str(arithmetic_mean_1w) + "\n\n")
plt.plot(year_index, arithmetic_mean_1w, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_1w, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 1w')
plt.savefig(dir + '/6.png')
plt.show()

print("연도별 1주일치 기하평균 : ", geometric_mean_1w)
f.write("연도별 1주일치 기하평균 : "+str(geometric_mean_1w) + "\n\n")
plt.plot(year_index, geometric_mean_1w, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_1w, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 1w')
plt.savefig(dir + '/7.png')
plt.show()


#2주일
arithmetic_mean_2w = []
geometric_mean_2w = []

for year in year_index :
    arithmetic_mean_2w.append((np.mean(earning_rate_per_year_2w[year-2007])-1)*100)
    geometric_mean_2w.append((scipy.stats.mstats.gmean(earning_rate_per_year_2w[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_2w) :
    if math.isnan(v) :
        arithmetic_mean_2w[i] = 0
for i, v in enumerate(geometric_mean_2w) :
    if math.isnan(v) :
        geometric_mean_2w[i] = 0

arithmetic_mean_2w = [round(float(i),2) for i in arithmetic_mean_2w]
geometric_mean_2w = [round(float(i),2) for i in geometric_mean_2w]

print("연도별 2주일치 산술평균 : ", arithmetic_mean_2w)
f.write("연도별 2주일치 산술평균 : "+str(arithmetic_mean_2w) + "\n\n")
plt.plot(year_index, arithmetic_mean_2w, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_2w, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 2w')
plt.savefig(dir + '/8.png')
plt.show()

print("연도별 2주일치 기하평균 : ", geometric_mean_2w)
f.write("연도별 2주일치 기하평균 : "+str(geometric_mean_2w) + "\n\n")
plt.plot(year_index, geometric_mean_2w, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_2w, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 2w')
plt.savefig(dir + '/9.png')
plt.show()


#1달
arithmetic_mean_1m = []
geometric_mean_1m = []

for year in year_index :
    arithmetic_mean_1m.append((np.mean(earning_rate_per_year_1m[year-2007])-1)*100)
    geometric_mean_1m.append((scipy.stats.mstats.gmean(earning_rate_per_year_1m[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_1m) :
    if math.isnan(v) :
        arithmetic_mean_1m[i] = 0
for i, v in enumerate(geometric_mean_1m) :
    if math.isnan(v) :
        geometric_mean_1m[i] = 0

arithmetic_mean_1m = [round(float(i),2) for i in arithmetic_mean_1m]
geometric_mean_1m = [round(float(i),2) for i in geometric_mean_1m]

print("연도별 1달치 산술평균 : ", arithmetic_mean_1m)
f.write("연도별 1달치 산술평균 : "+str(arithmetic_mean_1m) + "\n\n")
plt.plot(year_index, arithmetic_mean_1m, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_1m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 1m')
plt.savefig(dir + '/10.png')
plt.show()

print("연도별 1달치 기하평균 : ", geometric_mean_1m)
f.write("연도별 1달치 기하평균 : "+str(geometric_mean_1m) + "\n\n")
plt.plot(year_index, geometric_mean_1m, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_1m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 1m')
plt.savefig(dir + '/11.png')
plt.show()


#3달
arithmetic_mean_3m = []
geometric_mean_3m = []

for year in year_index :
    arithmetic_mean_3m.append((np.mean(earning_rate_per_year_3m[year-2007])-1)*100)
    geometric_mean_3m.append((scipy.stats.mstats.gmean(earning_rate_per_year_3m[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_3m) :
    if math.isnan(v) :
        arithmetic_mean_3m[i] = 0
for i, v in enumerate(geometric_mean_3m) :
    if math.isnan(v) :
        geometric_mean_3m[i] = 0

arithmetic_mean_3m = [round(float(i),2) for i in arithmetic_mean_3m]
geometric_mean_3m = [round(float(i),2) for i in geometric_mean_3m]

print("연도별 3달치 산술평균 : ", arithmetic_mean_3m)
f.write("연도별 3달치 산술평균 : "+str(arithmetic_mean_3m) + "\n\n")
plt.plot(year_index, arithmetic_mean_3m, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_3m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 3m')
plt.savefig(dir + '/12.png')
plt.show()

print("연도별 3달치 기하평균 : ", geometric_mean_3m)
f.write("연도별 3달치 기하평균 : "+str(geometric_mean_3m) + "\n\n")
plt.plot(year_index, geometric_mean_3m, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_3m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 3m')
plt.savefig(dir + '/13.png')
plt.show()


#6달
arithmetic_mean_6m = []
geometric_mean_6m = []

for year in year_index :
    arithmetic_mean_6m.append((np.mean(earning_rate_per_year_6m[year-2007])-1)*100)
    geometric_mean_6m.append((scipy.stats.mstats.gmean(earning_rate_per_year_6m[year-2007])-1)*100)

for i, v in enumerate(arithmetic_mean_6m) :
    if math.isnan(v) :
        arithmetic_mean_6m[i] = 0
for i, v in enumerate(geometric_mean_6m) :
    if math.isnan(v) :
        geometric_mean_6m[i] = 0

arithmetic_mean_6m = [round(float(i),2) for i in arithmetic_mean_6m]
geometric_mean_6m = [round(float(i),2) for i in geometric_mean_6m]

print("연도별 6달치 산술평균 : ", arithmetic_mean_6m)
f.write("연도별 6달치 산술평균 : "+str(arithmetic_mean_6m) + "\n\n")
plt.plot(year_index, arithmetic_mean_6m, 'rs--', label = 'strategy')
plt.plot(year_index, market_arithmetic_mean_6m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('arithmetic mean 6m')
plt.savefig(dir + '/14.png')
plt.show()

print("연도별 6달치 기하평균 : ", geometric_mean_6m)
f.write("연도별 6달치 기하평균 : "+str(geometric_mean_6m) + "\n\n")
plt.plot(year_index, geometric_mean_6m, 'rs--', label = 'strategy')
plt.plot(year_index, market_geometric_mean_6m, 'bs--', label = 'market average')
plt.legend(loc='upper left')
plt.title('geometric mean 6m')
plt.savefig(dir + '/15.png')
plt.show()

print('전체 발생 횟수 : ', len(earning_rate_1d), '2007년 : ', num_occurrence[0], "2008년 : ", num_occurrence[1], "2009년 : ", num_occurrence[2], "2010년 : ", num_occurrence[3], "2011년 : ", num_occurrence[4], "2012년 : ", num_occurrence[5],  "2013년 : ", num_occurrence[6], "2014년 : ", num_occurrence[7],  "2015년 : ", num_occurrence[8], "2016년 : ", num_occurrence[9],  "2017년 : ", num_occurrence[10], "2018년 : ", num_occurrence[11])
f.write('전체 발생 횟수 : ' + str(len(earning_rate_1d)) + '  2007년 : '+ str(num_occurrence[0]) + "  2008년 : " + str(num_occurrence[1]) + "  2009년 : " + str(num_occurrence[2]) + "  2010년 : "+ str(num_occurrence[3]) + "  2011년 : " + str(num_occurrence[4]) + "  2012년 : " + str(num_occurrence[5]) +  "  2013년 : " + str(num_occurrence[6]) + "  2014년 : " + str((num_occurrence[7])) +  "  2015년 : " + str(num_occurrence[8]) + "  2016년 : " + str(num_occurrence[9]) +  "  2017년 : " + str(num_occurrence[10]) + "  2018년 : " + str(num_occurrence[11]) + "\n\n")

print('3일치 최대수익률 : ', str(round((max(earning_rate_3d)-1)*100,2))+"%", '3일치 최소수익률 : ', str(round((min(earning_rate_3d)-1)*100,2))+'%')
f.write('3일치 최대수익률 : '+ str(round((max(earning_rate_3d)-1)*100,2))+"%  " + '3일치 최소수익률 : ' + str(round((min(earning_rate_3d)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_3d, bins='auto')
plt.title('3d histogram')
plt.savefig(dir + '/16.png')
plt.show()

print('1주일치 최대수익률 : ', str(round((max(earning_rate_1w)-1)*100,2))+"%", '1주일치 최소수익률 : ', str(round((min(earning_rate_1w)-1)*100,2))+'%')
f.write('1주일치 최대수익률 : '+ str(round((max(earning_rate_1w)-1)*100,2))+"%  " + '1주일치 최소수익률 : ' + str(round((min(earning_rate_1w)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_1w, bins='auto')
plt.title('1w histogram')
plt.savefig(dir + '/17.png')
plt.show()

print('2주일치 최대수익률 : ', str(round((max(earning_rate_2w)-1)*100,2))+"%", '2주일치 최소수익률 : ', str(round((min(earning_rate_2w)-1)*100,2))+'%')
f.write('2주일치 최대수익률 : '+ str(round((max(earning_rate_2w)-1)*100,2))+"%  "+ '2주일치 최소수익률 : '+ str(round((min(earning_rate_2w)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_2w, bins='auto')
plt.title('2w histogram')
plt.savefig(dir + '/18.png')
plt.show()

print('1달치 최대수익률 : ', str(round((max(earning_rate_1m)-1)*100,2))+"%", '1달치 최소수익률 : ', str(round((min(earning_rate_1m)-1)*100,2))+'%')
f.write('1달치 최대수익률 : '+ str(round((max(earning_rate_1m)-1)*100,2))+"%  "+ '1달치 최소수익률 : '+ str(round((min(earning_rate_1m)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_1m, bins='auto')
plt.title('1m histogram')
plt.savefig(dir + '/19.png')
plt.show()

print('3달치 최대수익률 : ', str(round((max(earning_rate_3m)-1)*100,2))+"%", '3달치 최소수익률 : ', str(round((min(earning_rate_3m)-1)*100,2))+'%')
f.write('3달치 최대수익률 : '+ str(round((max(earning_rate_3m)-1)*100,2))+"%  "+ '3달치 최소수익률 : '+ str(round((min(earning_rate_3m)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_3m, bins='auto')
plt.title('3m histogram')
plt.savefig(dir + '/20.png')
plt.show()

print('6달치 최대수익률 : ', str(round((max(earning_rate_6m)-1)*100,2))+"%", '6달치 최소수익률 : ', str(round((min(earning_rate_6m)-1)*100,2))+'%')
f.write('6달치 최대수익률 : '+ str(round((max(earning_rate_6m)-1)*100,2))+"%  "+ '6달치 최소수익률 : '+ str(round((min(earning_rate_6m)-1)*100,2))+'%' + "\n\n")
plt.hist(earning_rate_6m, bins='auto')
plt.title('6m histogram')
plt.savefig(dir + '/21.png')
plt.show()

f.close()
easygui.msgbox("폴더 제목을 바꿔!!", title="Warning")


"""
with open('c:/Users/김세윤/sample_32/market_avg.p', 'wb') as file:    #시장평균 저장
    pickle.dump(total_arithmetic_mean, file)
    pickle.dump(total_geometric_mean, file)
    pickle.dump(total_inc_prob, file)
    pickle.dump(arithmetic_mean_3d, file)
    pickle.dump(geometric_mean_3d, file)
    pickle.dump(arithmetic_mean_1w, file)
    pickle.dump(geometric_mean_1w, file)
    pickle.dump(arithmetic_mean_2w, file)
    pickle.dump(geometric_mean_2w, file)
    pickle.dump(arithmetic_mean_1m, file)
    pickle.dump(geometric_mean_1m, file)
    pickle.dump(arithmetic_mean_3m, file)
    pickle.dump(geometric_mean_3m, file)
    pickle.dump(arithmetic_mean_6m, file)
    pickle.dump(geometric_mean_6m, file)

"""

# 전체 수익률 산술평균 :  [-0.35258543895838601, -0.2207885806836396, -0.094984764460792626, 0.20004955745853703, 0.80067327729311799, 2.988591193153578, 6.2056362807452192]
# 전체 수익률 기하평균 :  [-0.46305474944672298, -0.45207845279505721, -0.44287269966005738, -0.42640672425597881, -0.38979051287159061, -0.35814527870601243, -0.34504979440617145]
# 전체 상승확률 :  [42.09775984022264, 43.62461029445958, 44.29364948693539, 45.28821980498289, 45.88841623811824, 46.91926032353219, 47.21388973442447]
# 연도별 3일치 산술평균 :  [-0.38491993467115737, -0.90128331914894888, 0.33428288916217408, -0.1558150116172885, -0.33823643298031003, -0.23767389604818501, -0.32402715070710686, -0.19534593738254058, 0.11832594842364763, -0.27726741222450224, -0.3752345472871399, 0.59552604238264362]
# 연도별 3일치 기하평균 :  [-0.69852458218443436, -1.3221637782245499, 0.043361620025894609, -0.36678113143217006, -0.60621170280376058, -0.46071641090025262, -0.47910536987796348, -0.35583570551170896, -0.14997002349137478, -0.47061199412671284, -0.52441205938442703, 0.36391454070421325]
# 연도별 1주일치 산술평균 :  [-0.35727454264967706, -1.2067451345540992, 0.80702643649479544, -0.0048648035200105078, -0.25936587691982593, -0.11276247407829842, -0.23913905282983983, -0.059046812142926619, 0.44048612265621401, -0.18789351909248575, -0.35151089790532719, 1.1647119476340562]
# 연도별 1주일치 기하평균 :  [-0.83528352231696523, -1.8311252486053586, 0.36978012035864261, -0.31991204819823427, -0.65470181215315781, -0.45247064155700123, -0.47272934787866427, -0.3027738788623946, 0.033588969909081889, -0.47773751555022503, -0.57408066106846567, 0.80934795336884413]
# 연도별 2주일치 산술평균 :  [-0.32343642968787334, -2.0885262821575878, 1.9916391351767482, 0.37681983461623769, -0.13343235369988049, 0.24218384008196647, -0.032877344224180316, 0.28609168285966824, 1.1980499640218412, 0.06698782450951235, -0.24057818475197168, 1.9474930362939125]
# 연도별 2주일치 기하평균 :  [-1.20096597413899, -3.1045364113638452, 1.174573952269431, -0.19016750047810005, -0.82816903635868355, -0.38053638352113506, -0.46973347858413339, -0.1638817399971626, 0.4578734676906393, -0.46307333553916585, -0.63841966901837521, 1.3262452304137362]
# 연도별 1달치 산술평균 :  [-0.47909955304443752, -4.3228586766775763, 4.610708885484982, 1.3424007466793508, 0.14902147528987886, 0.95582226522719083, 0.44138253931353955, 0.93481703071509603, 2.7605440906275591, 0.35277589214026683, 0.16461496172586187, 3.928265749371862]
# 연도별 1달치 기하평균 :  [-2.1166639864755643, -6.0030995577893709, 2.9958176549186755, 0.2348442180609922, -1.1218552899790013, -0.24957290469921345, -0.40411546429404144, 0.072013916926061405, 1.2981070839197972, -0.6290639347719118, -0.5917896360281949, 2.7814151380363139]
# 연도별 3달치 산술평균 :  [-1.3052326488270816, -13.351396173357966, 14.969792353599388, 4.8797546125596947, -0.061869521041291176, 5.1957484548901034, 1.8404865147149785, 3.1757715544408205, 9.3721782160443254, 1.8456168829760866, 0.050643602358713125, 10.915230370198703]
# 연도별 3달치 기하평균 :  [-6.0549991213535659, -16.969486258775046, 10.079921517345781, 2.0203049367717441, -3.1004907235312906, 1.7471147699406497, -0.35135678665063619, 0.65368206152023323, 4.9777886105899061, -0.88411677307039804, -1.8297465359018106, 7.4942311839190534]
# 연도별 6달치 산술평균 :  [-1.0187635771393255, -18.827319147915734, 24.133005504896321, 7.5597336082325661, 1.753260361696718, 9.7016491688852735, 5.3053885727902372, 6.7408634424475089, 18.201198204058056, 5.999222588830766, -0.76387099948224124, 7.8116187759508238]
# 연도별 6달치 기하평균 :  [-9.763674044460025, -24.861948869550645, 11.712766353199289, 2.281859918844642, -3.9391382540430619, 3.4979678058564945, 0.99589993107671582, 1.782504015915487, 9.5220808533815529, 0.59882763436160946, -4.2098720307437993, 2.2241624061861032]
# 전체 발생 횟수 :  4046631 2007년 :  169059 2008년 :  304978 2009년 :  329195 2010년 :  339855 2011년 :  356461 2012년 :  378712 2013년 :  392242 2014년 :  398185 2015년 :  414638 2016년 :  434021 2017년 :  452738 2018년 :  76547
# 3일치 최대수익률 :  782.909285714% 3일치 최소수익률 :  -87.490474359%
# 1주일치 최대수익률 :  1003.98825733% 1주일치 최소수익률 :  -87.9671771641%
# 2주일치 최대수익률 :  1140.36513029% 2주일치 최소수익률 :  -90.3273165892%
# 1달치 최대수익률 :  1380.29165798% 1달치 최소수익률 :  -95.6582981835%
# 3달치 최대수익률 :  3686.39848649% 3달치 최소수익률 :  -97.869095453%
# 6달치 최대수익률 :  4648.07352868% 6달치 최소수익률 :  -98.0842192725%