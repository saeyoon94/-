from bs4 import BeautifulSoup
import urllib.request as req
import datetime
import pandas as pd
import sqlite3
import time
import pandas as pd
from gensim.models import word2vec
from konlpy.tag import Twitter
import re

sdate = '2002-01-01'
edate = today = datetime.datetime.now().date().strftime('%Y-%m-%d')
page = 1

"""
twiter = Twitter()

def report_score(topic) :
    model = word2vec.Word2Vec.load('wiki.model')
    score_list = model.most_similar(positive = ['긍정', '성장', '기대'], negative = ['부정', '우려'])
    score_list += [('긍정',1),('성장',1),('기대',1),('부정',-1),('우려',-1)]
    score_dic = dict(score_list)
    malist = twiter.pos(topic, norm = True, stem = True)
    topic = []
    score = 0
    for word in malist :
        if not word[1] in ['Josa', 'Eomi', 'Punctuation'] :
            topic.append(word[0])
    for w in topic :
        if w in score_dic :
            score += score_dic[w]
    return score

리포트가 긍정적인지 부정적인지 점수를 평가하려했으나 포기(제목을 다음을 수 없었고, 실행시키는데 시간이 너무 오래걸림)

"""

def extract_code(text) :
    num_list = re.findall('[0-9]+', text)
    for num in num_list :
        if len(num) == 6 :
            return num
    for num in num_list :
        if len(num) == 5 :
            if num[-1] != '0' :
                return num+'0'
            else :
                return '0'+num
    return False




url = 'http://hkconsensus.hankyung.com/apps.analysis/analysis.list?&sdate='+ sdate + 'edate=' + edate + '&report_type=CO&pagenum=80&order_type=&now_page=' + str(page)
res = req.urlopen(url)
soup = BeautifulSoup(res, 'html.parser')

max_page = soup.select('div.paging > a')[-1].attrs['href'][-4:]
print(max_page)
while True :
    if page > int(max_page) :
        break
    print(page)

    url = 'http://hkconsensus.hankyung.com/apps.analysis/analysis.list?&sdate='+ sdate + 'edate=' + edate + '&report_type=CO&pagenum=80&order_type=&now_page=' + str(page)

    dfs = pd.read_html(url)
    df = dfs[0]

    df['code'] = df['제목 '].apply(extract_code)
    #df['code'] = df['제목 '].str.split("(", expand = True)[1].str[:6]              #그냥 괄호말고 대괄호 안에 넣은것도 있고, 괄호안에 실수로 띄어쓰기 넣어논 것도 있어서 정상적으로 처리 안됌. 숫자 6개만 잘 뽑아내도록 수정해야 할듯.
    df['작성일 '] = df['작성일 '].str.replace('-', "").astype(int)
    #df['적정가격 '] = df['적정가격 '].str.replace(",", "").astype(int)

    df = df[['작성일 ', '적정가격 ', '투자의견 ', 'code']]
    #df['score'] = df['제목 '].apply(report_score)

    if page == 1 :
        report_data = df

    else :
        report_data = report_data.append(df, ignore_index = True)
    page += 1
    time.sleep(0.35)

report_data.columns = ['date', 'TP', 'comment', 'code']


print(report_data)
con = sqlite3.connect("c:/Users/김세윤/sample_32/report.db")
report_data.to_sql('report', con, if_exists='replace')
print('완료')



#strong buy : 적극매수, 강력매수, Strong Buy, STRONGBUY, STRONG BUY
#buy : 비중확대, 매수, buy, Outperform, OVERWEIGHT, OUTPERFORM, OUTPER, OURPERFORM, Buy, BUY
#trading buy : 장기매수, Trading Buy, TRADINGBUY, TRADING BUY
#hold 이하 : 축소, 중립, 주의, 시장평균, 시장수익률, 비중축소, 보유, 매도, underperform, neutral, marketperform, UNDERPERFORM, UNDERPER, Sell, SUSPENDED, SELL, Reduce, REDUCE, Neutral, NEUTRAL, MKTUNDERPERF, MKTPERFORM, MKTPERF, MKTPER, MARKET PERFORM, Hold, HOLD
#NR : nr, Not Rated, -, NULL

#끝에가 0, 앞에도 0일 가능성이 높다.