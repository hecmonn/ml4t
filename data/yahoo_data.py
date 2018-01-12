import os
import requests
from dateutil.parser import parse
from datetime import datetime

now=datetime.now().strftime("%Y-%m-%d %H:%M")

#default params
symbol='SPY'
sd='2000-01-01'
ed= now

def download_data(symbol=symbol,sd=sd,ed=ed):
    s=parse(sd)
    e=parse(ed)
    url='https://query1.finance.yahoo.com/v7/finance/quote'
    '''payload={
        'symbol': str(symbol)
        ,'a': s.month-1
        ,'b': s.day
        ,'c': s.year
        ,'d': e.month-1
        ,'e': e.day
        ,'f': e.year
        ,'g': 'd'
        ,'ignore': '.csv'
    }'''
    fields = [
    'symbol',
    'regularMarketVolume',
    'regularMarketPrice',
    'regularMarketDayHigh',
    'regularMarketDayLow',
    'regularMarketTime',
    'regularMarketChangePercent'
    ]
    fields = ','.join(fields)
    payload={
        'lang': 'en-US',
        'region': 'US',
        'corsDomain': 'finance.yahoo.com',
        'fields': fields,
        'symbols': str(symbol)
    }
    return requests.get(url,params=payload)

def get_csv(symbol=symbol,sd=sd,ed=ed):
    r=download_data(symbol,sd,ed)
    if r.status_code!=200:
        print ('Unable to fetch data')
        return False
    path=os.path.join('./',str(symbol)+'.csv')
    print (path)
    f=open(path,'wb')
    f.write(r.content)
    f.close()
    return True


#get_csv(symbol='XOM')
response=download_data(symbol='XOM')
print (response)
