import pandas as pd
import os
def get_path(symbol):
    base_dir='data'
    return os.path.join(base_dir,'{}.csv'.format(str(symbol)))
    
def get_data(sd,ed,symbols):
    range_dates=pd.date_range(sd,ed)
    df=pd.DataFrame(index=range_dates)
    dfs_symbols=[]
    for symbol in symbols:
        path=get_path(symbol)
        df_symbol=pd.read_csv(path
                        ,index_col='Date'
                        ,parse_dates=True
                        ,usecols=['Date','Adj Close']
                        ,na_values=['nan'])
        df_symbol=df_symbol.rename(columns={'Adj Close':symbol})
        dfs_symbols.append(df_symbol)
        df=df.join(df_symbol,how='inner')
    return df

def daily_returns(df, use_pandas=True):
    if not use_pandas:
        # Note: Returned DataFrame must have the same number of rows
        daily_returns = df.copy() # copy given DataFrame to match size and column names
        # Compute daily returns for row 1 onwards
        # df[1:] picks all the rows from 1 till the end
        # df[:-1] picks all the row from 0 till 1 less than the end
        daily_returns[1:] = (df[1:] / df[:-1].values) - 1
        daily_returns.ix[0, :] = 0  # set daily returns for row 0 to 0
    else:
        daily_returns = (df / df.shift(1)) - 1
    return daily_returns
    
def cumulative_returns(df, begin_date, end_date):
    if len(df) > 1:
        cumulative_returns = (df.ix[begin_date:end_date, :] / df.ix[0]) - 1
    else:
        cumulative_returns = (df.ix[begin_date:end_date] / df.ix[0]) - 1
    return cumulative_returns
    
def momentum(df,sd,ed):
    return (df[sd]/df[ed])-1


def bollinger_bands(df,sd,ed):
    sma=df.rolling(window=20).mean()
    std=df[sd:ed].std()
    bb=(df[sd:ed]-sma)/(2*std)
    return bb
    
def fill_data(df):
    df.fillna(method='bfill',inplace=True)
    df.fillna(method='ffill',inplace=True)
    return df