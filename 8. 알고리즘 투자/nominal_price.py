# 오래된 리포트의 목표주가가 그 당시의 수정주가가 아닌 명목주가를 기준으로 적혀져 있는데, 이것을 초기에 고려 못하고 수정주가만 데이터베이스에 넣음
# example파일로 종목별 데이터베이스 생성 -> report_data파일로 리포트데이터 생성 -> metge_price&report파일로 둘이 합친 데이터베이스 생성
# quant파일은 계속 끊었다가 실행할 수 있도록 하는데 도움이 되려고 좀 쓴건데 example파일 코드에 포함시켜서 쓸모 없음
# 위에거 다 하고나면 이걸로 명목주가만 받아와서 합치자 ->> 나중에는 example파일을 수정해서 아예 이것을 필요없도록 하자

from example import Kiwoom
import time
import sys
import pickle
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import sqlite3


TR_REQ_TIME_INTERVAL = 0.6

if __name__ == "__main__":
    con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
    cur = con.cursor()

    app = QApplication(sys.argv)

    # Test Code
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    today =  '20180301'                                              #datetime.datetime.now().date().strftime('%Y%m%d')  원래 이건데 실행시간이 워낙 길어서 날짜가 넘어가버리니까 그냥 직접 지정하는게 좋을듯



    with open('c:/Users/김세윤/sample_32/dict.p', 'rb') as file:  #다시 실행할때마다 위에 과정 반복 안하도록  ######################처음부터 돌릴떄는 이거 없어야 함
        kiwoom.krx_dic = pickle.load(file)

    with open('c:/Users/김세윤/sample_32/processed_code.p', 'rb') as file:  #이미 처리한 코드들의 리스트(중간중간 끊었다가 처리할 수 있도록)  ######################처음부터 돌릴떄는 이거 없어야 함
        processed_code = pickle.load(file)

    #데이터베이스 생성.. 나중에는 for문을 바탕으로 전 종목에 대하여 생성해야함

    i = 1
    time.sleep(TR_REQ_TIME_INTERVAL)

    for code in kiwoom.krx_dic :
        cur.execute("SELECT sql FROM sqlite_master WHERE name='%s'"%code + "AND sql LIKE '%nominal_price%'")           #지금까지 진행한것은 뺴는 코드(nominal price가 있는 테이블만 제외
        table_list = cur.fetchall()
        if table_list != []:
            continue
        print(i)
        i = i+1
        print(code)
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.cnt = kiwoom.krx_dic[code]['cnt']#이 포문안으로 다 넣어야한다

        kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'trading_value':[], 'market_cap':[]}
        kiwoom.set_input_value("종목코드", "%s"%code)
        kiwoom.set_input_value("기준일자", today)
        kiwoom.set_input_value("수정주가구분", 0)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", "%s"%code)
            kiwoom.set_input_value("기준일자", today)
            kiwoom.set_input_value("수정주가구분", 0)
            kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")



        df = pd.DataFrame(kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume', 'trading_value','market_cap'], index=kiwoom.ohlcv['date']).iloc[::-1]
        df.columns = ['open', 'high', 'low', 'nominal_price', 'volume', 'trading_value','market_cap']
        df = df['nominal_price']
        df_company = pd.read_sql('SELECT * FROM "%s"' % code, con, index_col='index')
        df = pd.concat([df_company, df], axis=1)
        df.to_sql(code, con, if_exists='replace')


    print('완료')
