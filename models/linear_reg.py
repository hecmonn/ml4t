from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from helpers import get_data,daily_returns,cumulative_returns,bollinger_bands
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#reading data

symbols=['XRP-USD']
c_symbol=str(symbols[0])
sd,ed='2017-01-01','2018-01-01'
df=get_data(sd,ed,symbols)
dr=daily_returns(df).rename(columns={c_symbol:'DR'})
cr=cumulative_returns(df,sd,ed).rename(columns={c_symbol:'CR'})
df_kpis=dr.join(cr,how='inner')

bb=bollinger_bands(df,'2017-01-01',ed)
sma=df.rolling(window=20).mean()
r_std=df.rolling(window=20).std()
sma=sma.rename(columns={c_symbol:'SMA'})
#ax=df.plot(title='Adj Close X SMA')
#ax.set_xlabel('Dates')
#ax.set_ylabel('Price')
#sma.plot(label='SMA',ax=ax)
#plt.show()


df_kpis=df_kpis.ix[19:-1] #removed nan dates for kpis
df_model=df_kpis.join(df,how='inner').rename(columns={c_symbol:'Y'})
df_model=df_model.join(sma,how='inner')
df_model=df_model.join(bb,how='inner').rename(columns={c_symbol:'BB'})


X=df_model.ix[:-2,['CR','SMA','BB']].values
y=df_model.ix[1:-1,['Y']].values

#add sma
#add bb


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4)
reg=LinearRegression()
reg.fit(X_train,y_train)
pred=reg.predict(X_test)

plt.scatter(pred,y_test,c='r')
#plt.plot(X_test,pred,c='b')
plt.show()

print 'Score of model: ', reg.score(X_test,y_test)

#dataframe 0:dr 1:cr 2:sma 3:bb
print 'Coeff: ', reg.coef_
print 'Intercept: ', reg.intercept_

#Correlation
print df_model.corr(method='pearson')


