import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import time
import pandas as pd
import sqlite3
import datetime
import pickle
import talib
import numpy as np
import sys


TR_REQ_TIME_INTERVAL = 0.6

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.OnEventConnect.connect(self.event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_loop = QEventLoop()
        self.login_loop.exec_()

    def event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("not connected")

        self.login_loop.exit()

    def get_codelist_by_market(self, market):
        func = 'GetCodeListByMarket("%s")' % market
        codes = self.dynamicCall(func)
        return codes.split(';')

    def get_master_code_name(self, code):
        func = 'GetMasterCodeName("%s")' % code
        name = self.dynamicCall(func)
        return name

    def get_master_listed_stock_cnt(self, code):
        func = 'GetMasterListedStockCnt("%s")' % code
        cnt = self.dynamicCall(func)
        return cnt

    def get_master_listed_stock_date(self, code):
        func = 'GetMasterListedStockDate("%s")' % code
        date = self.dynamicCall(func)
        return date

    def get_theme_group_list(self, type = 0):
        func = 'GetThemeGroupList("%s")' % type
        codes = self.dynamicCall(func)
        return codes.split(';')

    def get_theme_group_code(self, code):
        func = 'GetThemeGroupCode("%s")' % code
        codes = self.dynamicCall(func).split(';')
        for i, code in enumerate(codes) :
            codes[i] = code[1:]
        return codes

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opt10059_req":
            self._opt10059(rqname, trcode)
        elif rqname == "opt10014_req":
            self._opt10014(rqname, trcode)
        elif rqname == "opt10013_req":
            self._opt10013(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            trading_value = self._comm_get_data(trcode, "", rqname, i, "거래대금")

            self.data_to_list_basic(date, open, high, low, close, volume, trading_value)

    def _opt10059(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        for i in range(data_cnt):
            individual = self._comm_get_data(trcode, "", rqname, i, "개인투자자")
            foreigner = self._comm_get_data(trcode, "", rqname, i, "외국인투자자")
            institution = self._comm_get_data(trcode, "", rqname, i, "기관계")
            pension = self._comm_get_data(trcode, "", rqname, i, "연기금등")
            self.data_to_list_group(individual, foreigner, institution, pension)

    def _opt10014(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        for i in range(data_cnt):
            short_rate = self._comm_get_data(trcode, "", rqname, i, "매매비중")   #공매도 비율
            self.ohlcv['short_rate'].append(float(short_rate))

    def _opt10013(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        for i in range(data_cnt):
            donation_rate = self._comm_get_data(trcode, "", rqname, i, "공여율")
            balance_rate = self._comm_get_data(trcode, "", rqname, i, "잔고율")
            self.ohlcv['donation_rate'].append(float(donation_rate))
            self.ohlcv['balance_rate'].append(float(balance_rate))



    def data_to_list_basic(self, date, open, high, low, close, volume, trading_value):
        self.ohlcv['date'].append(int(date))
        self.ohlcv['open'].append(int(open))
        self.ohlcv['high'].append(int(high))
        self.ohlcv['low'].append(int(low))
        self.ohlcv['close'].append(int(close))
        self.ohlcv['volume'].append(int(volume))
        self.ohlcv['trading_value'].append(int(trading_value))
        self.ohlcv['market_cap'].append(int(close)*self.cnt)  #시가총액

    def data_to_list_group(self, individual, foreigner, institution, pension):
        self.ohlcv['individual'].append(int(individual))
        self.ohlcv['foreigner'].append(int(foreigner))
        self.ohlcv['institution'].append(int(institution))
        self.ohlcv['pension'].append(int(pension))

def process_code() :                                                        #중간중간 재시작할때 지금까지 처리한 코드들을 정리하는 함수
    con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
    cur = con.cursor()
    cur.execute('select name from sqlite_master where type="table"')

    table_list = cur.fetchall()
    code_list = []

    for i in table_list :
        code_list.append(i[0])

    print(code_list)
    print(len(code_list))

    with open('c:/Users/김세윤/sample_32/processed_code.p', 'wb') as file:  # hello.txt 파일을 바이너리 쓰기 모드(rb)로 열기
        pickle.dump(code_list, file)



if __name__ == "__main__":
    start_time = time.time()
    process_code()

    app = QApplication(sys.argv)

    # Test Code
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    today =  '20180301'                                              #datetime.datetime.now().date().strftime('%Y%m%d')  원래 이건데 실행시간이 워낙 길어서 날짜가 넘어가버리니까 그냥 직접 지정하는게 좋을듯

    """
    # 종목 코드
    kospi_codes = kiwoom.get_codelist_by_market(0)
    kosdaq_codes = kiwoom.get_codelist_by_market(10)
    ETF = kiwoom.get_codelist_by_market(8)
    codes = kospi_codes + kosdaq_codes

    kiwoom.krx_dic = {}


    # 종목 이름
    for code in codes:   #우선주, ETF, ETN, 스팩 제외한 코스피, 코스닥의 전 종목의 코드
        name = kiwoom.get_master_code_name(code)
        cnt = kiwoom.get_master_listed_stock_cnt(code)
        date = kiwoom.get_master_listed_stock_date(code)
        if (code[5:6] == '0') and ('스팩' not in name) and (code not in ETF) and ('ETN' not in name):
            kiwoom.krx_dic[code] = {'name' : name, 'cnt' : cnt, 'date' : date}  #종목명, 상장주식수, 상장일

    #테마 코드
    theme_codes = kiwoom.get_theme_group_list()
    theme_dic = {}

    for code in theme_codes :
        theme_dic[code[:3]] = kiwoom.get_theme_group_code(code[:3])

    with open('dict.p', 'wb') as file:  # hello.txt 파일을 바이너리 쓰기 모드(rb)로 열기
        pickle.dump(kiwoom.krx_dic, file)
        pickle.dump(theme_dic, file)

    """

    with open('c:/Users/김세윤/sample_32/dict.p', 'rb') as file:  #다시 실행할때마다 위에 과정 반복 안하도록  ######################처음부터 돌릴떄는 이거 없어야 함
        kiwoom.krx_dic = pickle.load(file)

    with open('c:/Users/김세윤/sample_32/processed_code.p', 'rb') as file:  #이미 처리한 코드들의 리스트(중간중간 끊었다가 처리할 수 있도록)  ######################처음부터 돌릴떄는 이거 없어야 함
        processed_code = pickle.load(file)

    #데이터베이스 생성.. 나중에는 for문을 바탕으로 전 종목에 대하여 생성해야함

    i = 1
    time.sleep(TR_REQ_TIME_INTERVAL)

    for code in kiwoom.krx_dic :
        if time.time()-start_time > 500 :
            print('중간 종료')
            sys.exit()

        print(i)
        i = i+1
        if code in processed_code :     #이미 실행한 코드는 다시 하지 않도록... ################################처음부터 돌릴떄는 이거 없어야 함  #대충 18분 50초정도 시작
            continue
        st = time.time()
        print(code)
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.cnt = kiwoom.krx_dic[code]['cnt']#이 포문안으로 다 넣어야한다

        kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': [], 'trading_value':[], 'market_cap':[], 'individual':[], 'foreigner':[], 'institution':[], 'pension':[], 'short_rate' : [], 'donation_rate': [], 'balance_rate' : []}
        kiwoom.set_input_value("종목코드", "%s"%code)
        kiwoom.set_input_value("기준일자", today)
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", "%s"%code)
            kiwoom.set_input_value("기준일자", today)
            kiwoom.set_input_value("수정주가구분", 1)
            kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

            print('하나')

        time.sleep(TR_REQ_TIME_INTERVAL)


        kiwoom.set_input_value("종목코드", "%s"%code)
        kiwoom.set_input_value("일자", today)
        kiwoom.set_input_value("금액수량구분", "1")
        kiwoom.set_input_value("매매구분", "0")
        kiwoom.set_input_value("단위구분", "1")

        kiwoom.comm_rq_data("opt10059_req", "opt10059", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", "%s"%code)
            kiwoom.set_input_value("일자", today)
            kiwoom.set_input_value("금액수량구분", "1")
            kiwoom.set_input_value("매매구분", "0")
            kiwoom.set_input_value("단위구분", "1")
            kiwoom.comm_rq_data("opt10059_req", "opt10059", 2, "0101")
            print('둘')

        time.sleep(TR_REQ_TIME_INTERVAL)


        kiwoom.set_input_value("종목코드", "%s"%code)
        kiwoom.set_input_value("시간구분", "1")
        kiwoom.set_input_value("시작일자", "")
        kiwoom.set_input_value("종료일자", today)


        kiwoom.comm_rq_data("opt10014_req", "opt10014", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", "%s"%code)
            kiwoom.set_input_value("시간구분", "1")
            kiwoom.set_input_value("시작일자", "")
            kiwoom.set_input_value("종료일자", today)
            kiwoom.comm_rq_data("opt10014_req", "opt10014", 2, "0101")
            print('셋')

        time.sleep(TR_REQ_TIME_INTERVAL)


        kiwoom.set_input_value("종목코드", "%s"%code)
        kiwoom.set_input_value("일자", today)
        kiwoom.set_input_value("조회구분", "1")


        kiwoom.comm_rq_data("opt10013_req", "opt10013", 0, "0101")

        while kiwoom.remained_data == True:
            time.sleep(TR_REQ_TIME_INTERVAL)
            kiwoom.set_input_value("종목코드", "%s"%code)
            kiwoom.set_input_value("일자", today)
            kiwoom.set_input_value("조회구분", "1")
            kiwoom.comm_rq_data("opt10013_req", "opt10013", 2, "0101")
            print('넷')



        def ichimoku(d) :                     #일목균형표가 talib에 없어서 따로 만듦
            nine_period_high = pd.rolling_max(d['high'], window=9)
            nine_period_low = pd.rolling_min(d['low'], window=9)
            tenkan_sen = (nine_period_high + nine_period_low) / 2

            # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
            period26_high = pd.rolling_max(d['high'], window=26)
            period26_low = pd.rolling_min(d['low'], window=26)
            kijun_sen = (period26_high + period26_low) / 2

            # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
            senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

            # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
            period52_high = pd.rolling_max(d['high'], window=52)
            period52_low = pd.rolling_min(d['low'], window=52)
            senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

            return  senkou_span_a, senkou_span_b

        #공매도 비율이 16년 8월 23일부터 지원해서 그 이전 데이터는 모두 0으로 처리
        diff = len(kiwoom.ohlcv['pension'])-len(kiwoom.ohlcv['short_rate'])
        dummy_list = [0 for i in range(diff)]
        kiwoom.ohlcv['short_rate'] += dummy_list

        df = pd.DataFrame(kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume', 'trading_value','market_cap', 'individual', 'foreigner', 'institution', 'pension', 'short_rate', 'donation_rate', 'balance_rate'], index=kiwoom.ohlcv['date']).iloc[::-1]



        close = df['close'].astype(float).as_matrix()
        high = df['high'].astype(float).as_matrix()
        low = df['low'].astype(float).as_matrix()
        open = df['open'].astype(float).as_matrix()
        volume = df['volume'].astype(float).as_matrix()



        ma5 = talib.MA(close, timeperiod = 5)
        df['MA5'] = ma5
        ma20 = talib.MA(close, timeperiod = 20)
        df['MA20'] = ma20
        ma60 = talib.MA(close, timeperiod = 60)
        df['MA60'] = ma60
        ma120 = talib.MA(close, timeperiod = 120)
        df['MA120'] = ma120
        ma224 = talib.MA(close, timeperiod=224)
        df['MA224'] = ma224
        vma5 = talib.MA(volume, timeperiod = 5)
        df['VMA5'] = vma5
        vma20 = talib.MA(volume, timeperiod = 20)
        df['VMA20'] = vma20
        upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        df['bollinger_upper20'] = upperband
        df['bollinger_lower20'] = lowerband
        cci = talib.CCI(high, low, close, timeperiod=9)
        df['CCI9'] = cci
        rsi = talib.RSI(close, timeperiod=14)
        df['RSI14'] = rsi
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=12, slowk_period=5, slowd_period=5)
        df['Stochastic_K'] = slowk
        df['Stochastic_D'] = slowd
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD'] = macd
        df['MACD_signal'] = macdsignal
        senkou_a,senkou_b = ichimoku(df[['high', 'low']])
        df['senkou_span_a'] = senkou_a
        df['senkou_span_b'] = senkou_b

        df["52week_high"] = pd.rolling_max(df['high'], window=224, min_periods=1)   #52주신고가
        df["52week_low"] = pd.rolling_min(df['low'], window=224, min_periods=1)    #52주신저가



        con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
        df.to_sql('%s'%code, con, if_exists='replace')
        et = time.time()
        print(et-st)
    print('완료')





