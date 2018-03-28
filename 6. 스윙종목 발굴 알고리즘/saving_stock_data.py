import pandas as pd
import openpyxl
import random
import re
#from sklearn import model_selection, svm, metrics
import pickle



code = pd.read_csv('code.csv') #투자대상종목들의 종목코드
after16 = pd.read_csv('after16.csv')  #16년이후 상장된 종목들의 종목코드(16년부터 학습시키므로, 학습시에는 제외시켜야한다)

code = list(code)
after16 = list(after16)

transfer = []

for i in code :
    new = str(i[1:])
    transfer.append(new)

code = transfer

transfer = []

for i in after16 :
    new = str(i[1:])
    transfer.append(new)

after16 = transfer

for i in code :                  #code에서 2016년이후 상장된 종목들은 제거
    if i in after16 :
        code.remove(i)

excel = openpyxl.load_workbook("stock_data.xlsx")
company_list = excel.get_sheet_names()    #모든 시트의 리스트


data_num = 6000    #training, test 데이터 전체의 개수
X = []
label = []


for i in range(data_num) :
    print(i)
    company_name = random.choice(company_list)
    df = pd.read_excel("stock_data.xlsx", sheetname=company_name, header=None).T
    col_len = len(df[0])
    start_day = random.randint(5,col_len-20)
    if int(str(df[0][start_day]).replace(',','')) < int(str(df[0][start_day-1]).replace(',','')) < int(str(df[0][start_day-5]).replace(',','')) :
        label.append(1)
    else :
        label.append(0)
    df = df[start_day:start_day+20]
    df = df.applymap(lambda x: str(x).replace(',',''))
    df = df.astype(int)

    for j in range(4) :   #정규화
        c = df[j]
        v_max = df[j].max()
        v_min = df[j].min()
        if v_max >= abs(v_min) :
            v_max = v_max
        else :
            v_max = abs(v_min)
        #df[j] = (c-v_min) / (v_max-v_min)
        if v_max != 0:
            df[j] = c/v_max
        else :
            df[j] = c
    k = pd.concat([df[0],df[1],df[2],df[3]], axis=0)

    X.append(k.as_matrix().astype('float16'))

print(X)
print(label, sum(label))

border = int(data_num*2/3)

train_X = X[:border]
train_y = label[:border]
test_X = X[border:]
test_y = label[border:]

with open('data.p', 'wb') as file:    # hello.txt 파일을 바이너리 쓰기 모드(rb)로 열기
    pickle.dump(train_X, file)
    pickle.dump(train_y, file)
    pickle.dump(test_X, file)
    pickle.dump(test_y, file)

#clf = svm.SVC()
#clf.fit(train_X, train_y)
#predict = clf.predict(test_X)

#ac_score = metrics.accuracy_score(test_y, predict)
#cl_report = metrics.classification_report(test_y, predict)
#print("정답률=",ac_score)
#print(cl_report)
