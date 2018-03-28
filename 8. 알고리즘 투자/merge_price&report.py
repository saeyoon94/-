import sqlite3
import pandas as pd
import time
import datetime
"""
con = sqlite3.connect("c:/Users/김세윤/sample_32/report.db")                       #중구난방인 투자의견을 5가지로 통일
df = pd.read_sql('select * from "report"', con)
df['comment'] = df['comment'].replace(['적극매수', '강력매수', 'Strong Buy', 'STRONGBUY', 'STRONG BUY'], 'StrongBuy')
df['comment'] = df['comment'].replace(['비중확대', '매수', 'buy', 'Outperform', 'OVERWEIGHT', 'OUTPERFORM', 'OUTPER', 'OURPERFORM', 'Buy', 'BUY'], 'Buy')
df['comment'] = df['comment'].replace(['장기매수', 'Trading Buy', 'TRADINGBUY', 'TRADING BUY'], 'TradingBuy')
df['comment'] = df['comment'].replace(['축소', '중립', '주의', '시장평균', '시장수익률', '비중축소', '보유', '매도', 'underperform', 'neutral', 'marketperform', 'UNDERPERFORM', 'UNDERPER', 'Sell', 'SUSPENDED', 'SELL', 'Reduce', 'REDUCE', 'Neutral', 'NEUTRAL', 'MKTUNDERPERF', 'MKTPERFORM', 'MKTPERF', 'MKTPER', 'MARKET PERFORM', 'Hold', 'HOLD', 'MARKETPERFORM', 'UNDERWEIGHT', 'mktper', '적극매도'], 'Hold')
df['comment'] = df['comment'].replace(['nr', 'Not Rated', '-', None], 'Not Rated')

def to_datetime(str) :
    return datetime.datetime.strptime(str, '%Y%m%d')

df['date'] = df['date'].astype(str).apply(to_datetime)


con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
weekday = pd.read_sql('select "index" from "005930"', con)   # 평일만 모두 긁어온다 (상장한지 오래된 삼성전자 기준)
weekday = weekday['index'].astype(str).apply(to_datetime).tolist()

holiday_report_index = []


def last_weekday(date) :
    date = date-datetime.timedelta(days=1)
    if date not in weekday :
        date = date - datetime.timedelta(days=1)
        if date not in weekday:
            date = date - datetime.timedelta(days=1)
            if date not in weekday:
                date = date - datetime.timedelta(days=1)
                if date not in weekday:
                    date = date - datetime.timedelta(days=1)
                    if date not in weekday:
                        date = date - datetime.timedelta(days=1)
                        if date not in weekday:
                            date = date - datetime.timedelta(days=1)
                            if date not in weekday:
                                date = date - datetime.timedelta(days=1)
                                if date not in weekday:
                                    date = date - datetime.timedelta(days=1)
                                    if date not in weekday:
                                        date = date - datetime.timedelta(days=1)

    return date

for i in range(len(df)) :
    date = df['date'].ix[i]
    if date not in weekday :
        holiday_report_index.append(date)
        df['date'].ix[i] = last_weekday(date)
        print(date,"에서",df['date'].ix[i],"로")

print(holiday_report_index)

def datetime_to_int(date) :
    date = date.strftime('%Y%m%d')
    return date

df['date'] = df['date'].apply(datetime_to_int).astype(int)

df.to_sql('report', con, if_exists='replace', index=False)

a = []                                                            #빠진것 없나 체크
for i in list(df['comment']) :
    if i in a :
        continue
    else :
        a.append(i)
print(a)

"""

##############################################################################################

con = sqlite3.connect("c:/Users/김세윤/sample_32/stock.db")
cur = con.cursor()
cur.execute('select name from sqlite_master where type="table"')

table_list = cur.fetchall()
code_list = []

for i in table_list[:len(table_list)-1] :
    code_list.append(i[0])

print(code_list)              # 데이터베이스 속 전 종목의 코드리스트
print(len(code_list))


"""
#cur.execute('CREATE TABLE ab AS SELECT * FROM "005930"')
#cur.execute('ALTER TABLE ab ADD TP REAL')
#cur.execute('ALTER TABLE ab ADD Buy INT')
#cur.execute('ALTER TABLE ab ADD Hold INT')
#cur.execute('INSERT INTO ab(TP) SELECT AVG(TP) FROM report WHERE report.date = 20180220 AND report.code = "005930"')

cur.execute('SELECT AVG(report.TP) FROM report, "005930" WHERE report.date = "005930.index" AND report.code = "005930"')
cur.execute('INSERT INTO ab(TP, Buy, Hold) SELECT  AVG( TP ) TPAvg, COUNT( case when comment="Buy" THEN 1 END) BuyCount, COUNT( case when comment="Hold" THEN 1 END ) HoldCount FROM report where code="005930" AND group by date')
print(cur.fetchall())


for i, code in enumerate(code_list) :                    #칼럼부터 추가   이거필요없음
    print(i)
    if code == '040300' :
        continue
    cur.execute('ALTER TABLE "%s" ADD TP REAL' % code)
    cur.execute('ALTER TABLE "%s" ADD num_report INT' % code)
    cur.execute('ALTER TABLE "%s" ADD StrongBuy INT'%code)
    cur.execute('ALTER TABLE "%s" ADD Buy INT'%code)
    cur.execute('ALTER TABLE "%s" ADD TradingBuy INT' % code)
    cur.execute('ALTER TABLE "%s" ADD Hold INT'%code)
    cur.execute('ALTER TABLE "%s" ADD Not_Rated INT' % code)


"""



for i, code in enumerate(code_list) :
    print(i)
    df_report = pd.read_sql('SELECT date, AVG( TP ) TP, COUNT(*) num_report, COUNT( case when comment="StrongBuy" THEN 1 END) StrongBuy, COUNT( case when comment="Buy" THEN 1 END) Buy, COUNT( case when comment="TradingBuy" THEN 1 END) TradingBuy, COUNT( case when comment="Hold" THEN 1 END ) Hold, COUNT( case when comment="Not Rated" THEN 1 END ) Not_Rated FROM report where code="%s" group by date'%code, con, index_col='date')
    df_company = pd.read_sql('SELECT * FROM "%s"'%code, con, index_col='index')
    df = pd.concat([df_company, df_report], axis=1)
    df[['num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']] = df[['num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']].fillna(0)  #결측치 처리
    #df[['open', 'high', 'low', 'close', 'volume', 'trading_value','market_cap', 'individual', 'foreigner', 'institution', 'pension','num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']] = df[['open', 'high', 'low', 'close', 'volume', 'trading_value','market_cap', 'individual', 'foreigner', 'institution', 'pension','num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']].astype(int)
    df[['num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']] = df[['num_report', 'StrongBuy', 'Buy', 'TradingBuy', 'Hold', 'Not_Rated']].astype(int)
    df.to_sql(code, con, if_exists='replace')

    #con.commit()


