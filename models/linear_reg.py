from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from helpers import get_data,daily_returns,cumulative_returns,bollinger_bands
from datetime import datetime
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#reading data
symbols=['SPY']
c_symbol=str(symbols[0])
sd='2015-01-01'
#ed=datetime.now().strftime("%Y-%m-%d")
ed='2018-01-09'

df=get_data(sd,symbols)
dr=daily_returns(df).rename(columns={c_symbol:'DR'})
cr=cumulative_returns(df,sd,ed).rename(columns={c_symbol:'CR'})
df_kpis=dr.join(cr,how='inner')

bb=bollinger_bands(df,sd,ed)
sma=df.rolling(window=20).mean()
r_std=df.rolling(window=20).std()
sma=sma.rename(columns={c_symbol:'SMA'})
#ax=df.plot(title='Adj Close X SMA')
#ax.set_xlabel('Dates')
#ax.set_ylabel  ('Price')
#sma.plot(label='SMA',ax=ax)

dr.plot(title="Daily returns")
plt.show()

df_kpis=df_kpis.ix[19:] #removed nan dates for kpis

df_model=df_kpis.join(df,how='inner').rename(columns={c_symbol:'Y'})
df_model=df_model.join(sma,how='inner')
df_model=df_model.join(bb,how='inner').rename(columns={c_symbol:'BB'})

X=df_model.ix[:-2,['CR','SMA','BB']].values
y=df_model.ix[1:-1,['Y']].values

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4)
reg=LinearRegression()
reg.fit(X_train,y_train)
pred=reg.predict(X_test)
sme=mean_squared_error(y_test,pred)

plt.scatter(pred,y_test,c='r')
#plt.plot(X_test,pred,c='b')
#plt.show()
to_predict=df_model.ix[-1,['CR','SMA','BB']].values
last_pred=reg.predict([to_predict])
print (df_model)
print('Prediction for',ed ,last_pred)
print ('Score of model: ', reg.score(X_test,y_test))
print ('SME: ',sme)

#dataframe 0:dr 1:cr 2:sma 3:bb
print ('Coeff: ', reg.coef_)
print ('Intercept: ', reg.intercept_)

#Correlation
print (df_model.corr(method='pearson'))
