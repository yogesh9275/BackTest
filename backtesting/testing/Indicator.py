import talib
import pandas as pd

# Symbol = "SBIN"
# StartDate = '2016-01-01'
# EndDate = '2023-01-30'

# while True:
#     print(GetLiveMarketPrice(Symbol), end='\r')

# df = StockMarketData(Symbol, StartDate, EndDate)
# close = df['CLOSE'].values
# low = df['LOW'].values
# high = df['HIGH'].values
# open = df['OPEN'].values

# df['RSI_14'] = talib.RSI(close, timeperiod=14)
# df['MA'] = talib.MA(close, timeperiod=20)
# df['SMA50'] = talib.SMA(close, timeperiod=50)
# df['SMA200'] = talib.SMA(close, timeperiod=200)
# df['EMA50'] = talib.EMA(close, timeperiod=50)
# df['EMA200'] = talib.EMA(close, timeperiod=200)
# df['BBANDup'], df['BBANDmid'], df['BBANDlow'] = talib.BBANDS(
#     close, timeperiod=20, nbdevup=20, nbdevdn=2, matype=0)
# df['ATR_14'] = talib.ATR(high, low, close, timeperiod=14)
# df["Stochastic_k"], df["Stochastic_d"] = talib.STOCH(
#     high, low, close, fastk_period=14, slowk_period=3, slowd_period=3)
# df['StochasticRSI_k'], df['StochasticRSI_d'] = talib.STOCHRSI(close)
# df['KAMA'] = talib.KAMA(close)
# df['MAX'] = talib.MAX(close)
# df['MIN'] = talib.MIN(close)
# df['CCI'] = talib.CCI(high, low, close)
# df['ADX'] = talib.ADX(high, low, close)
# df['WILLR'] = talib.WILLR(high, low, close)
# df['APO'] = talib.APO(close, 12, 26, 0)

# df['Signal'] = None
# RSI(close, timeperiod=14)
# df.to_csv('indicator_data.csv')
# print(df)

def IndicatorData(df, Indicator, IndicatorNumber,timeperiod=0):
    # df = df.to_numpy()
    # print(df)
    close = df['CLOSE']
    low = df['LOW']
    high = df['HIGH']
    open = df['OPEN']
    int(timeperiod)
    i = IndicatorNumber
    if Indicator == 'CLOSE':
        df[f'Indicator{i}'] = df['CLOSE']
    elif Indicator == 'OPEN':
        df[f'Indicator{i}'] = df['OPEN']
    elif Indicator == 'HIGH':
        df[f'Indicator{i}'] = df['HIGH']
    elif Indicator == 'LOW':
        df[f'Indicator{i}'] = df['LOW']
    elif Indicator == '52W H':
        df[f'Indicator{i}'] = df['52W H']
    elif Indicator == '52W L':
        df[f'Indicator{i}'] = df['52W L']
    elif Indicator == 'RSI':
        timeperiod = 14 if timeperiod == 0 else timeperiod
        df[f'Indicator{i}'] = talib.RSI(close, timeperiod=timeperiod)
    elif Indicator == 'MA':
        timeperiod = 50 if timeperiod == 0 else timeperiod
        df[f'Indicator{i}'] = talib.MA(close, timeperiod=timeperiod)
    elif Indicator == 'SMA':
        timeperiod = 50 if timeperiod == 0 else timeperiod
        df[f'Indicator{i}'] = talib.SMA(close, timeperiod=timeperiod)
    elif Indicator == 'EMA':
        timeperiod = 50 if timeperiod == 0 else timeperiod
        df[f'Indicator{i}'] = talib.EMA(close, timeperiod=timeperiod)
    elif Indicator == 'BBANDup':
        timeperiod = 20 if timeperiod == 0 else timeperiod+1
        df[f'Indicator{i}'], x, y = talib.BBANDS(
            close, timeperiod=timeperiod, nbdevup=20, nbdevdn=2, matype=0)
        del x,y
    elif Indicator == 'BBANDmid':
        timeperiod = 20 if timeperiod == 0 else timeperiod+1
        x, df[f'Indicator{i}'], y = talib.BBANDS(
            close, timeperiod=timeperiod, nbdevup=20, nbdevdn=2, matype=0)
        del x,y
    elif Indicator == 'BBANDlow':
        timeperiod = 20 if timeperiod == 0 else timeperiod+1
        x, y, df[f'Indicator{i}'] = talib.BBANDS(
            close, timeperiod=timeperiod, nbdevup=20, nbdevdn=2, matype=0)
        del x,y
    elif Indicator == 'ATR':
        timeperiod = 14 if timeperiod == 0 else timeperiod
        df[f'Indicator{i}'] = talib.ATR(
            high, low, close, timeperiod=timeperiod)
    elif Indicator == 'Stochastic_k':
        df[f'Indicator{i}'], x  = talib.STOCH(
            high, low, close, fastk_period=14, slowk_period=3, slowd_period=3)
        del x
    elif Indicator == 'Stochastic_d':
        x, df[f'Indicator{i}']  = talib.STOCH(
            high, low, close, fastk_period=14, slowk_period=3, slowd_period=3)
        del x
    elif Indicator == 'StochasticRSI_k':
        df[f'Indicator{i}'], x = talib.STOCHRSI(close)
        del x
    elif Indicator == 'StochasticRSI_d':
        x, df[f'Indicator{i}'] = talib.STOCHRSI(close)
        del x
    elif Indicator == 'KAMA':
        df[f'Indicator{i}'] = talib.KAMA(close)
    elif Indicator == 'MAX':
        df[f'Indicator{i}'] = talib.MAX(close)
    elif Indicator == 'MIN':
        df[f'Indicator{i}'] = talib.MIN(close)
    elif Indicator == 'ADX':
        df[f'Indicator{i}'] = talib.ADX(high, low, close)
    elif Indicator == 'APO':
        df[f'Indicator{i}'] = talib.APO(close, 12, 26, 0)
    elif Indicator == 'SuperTrend':
        df[f'Indicator{i}'] = talib.supertrend(
            df['HIGH'], df['LOW'], df['CLOSE'], length=10, multiplier=3)['SUPERT_10_3.0']
    elif Indicator == 'Number':
        df[f'Indicator{i}'] = timeperiod
    
    return df
