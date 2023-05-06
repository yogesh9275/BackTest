import talib



def add_indicators(indicator_choices, df):
    symbol = df.loc[1,'SYMBOL']
    indict = []
    df1 = df.copy()
    for i, indicator in enumerate(indicator_choices):
        if indicator == 'SMA':
            inputs = {'real': df['CLOSE'], 'timeperiod': 10}
            df1['Indicator_'+str(i)] = talib.SMA(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'EMA':
            inputs = {'real': df['CLOSE'], 'timeperiod': 10}
            df1['Indicator_'+str(i)] = talib.EMA(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'RSI':
            inputs = {'real': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.RSI(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'MACD':
            inputs = {'real': df['CLOSE']}
            df1['Indicator_'+str(i)] = talib.MACD(**inputs)[0]
            indict.append('Indicator_'+str(i))
        elif indicator == 'ADX':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.ADX(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'ATR':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.ATR(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'BBANDS_U':
            close =  df['CLOSE']
            df1['Indicator_'+str(i)] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[0] / \
                         talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[0].mean()
            indict.append('Indicator_'+str(i))
        elif indicator == 'BBANDS_M':
            df1['Indicator_'+str(i)] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1] / \
                         talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[1].mean()
            indict.append('Indicator_'+str(i))
        elif indicator == 'BBANDS_L':
            df1['Indicator_'+str(i)] = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2] / \
                         talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)[2].mean()
            indict.append('Indicator_'+str(i))
        elif indicator == 'CCI':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.CCI(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'Chaikin_AD':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'volume': df['Volume']}
            df1['Indicator_'+str(i)] = talib.AD(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'DMI':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.DX(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'OBV':
            df1['Indicator_'+str(i)] = talib.OBV(df['CLOSE'], df['Volume'])
            indict.append('Indicator_'+str(i))
        elif indicator == 'ROC':
            inputs = {'real': df['CLOSE'], 'timeperiod': 10}
            df1['Indicator_'+str(i)] = talib.ROC(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'SAR':
            inputs = {'high': df['HIGH'], 'low': df['LOW']}
            df1['Indicator_'+str(i)] = talib.SAR(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'STDDEV':
            inputs = {'real': df['CLOSE'], 'timeperiod': 5, 'nbdev': 1}
            df1['Indicator_'+str(i)] = talib.STDDEV(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'TRIX':
            inputs = {'real': df['CLOSE'], 'timeperiod': 30}
            df1['Indicator_'+str(i)] = talib.TRIX(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'WILLR':
            inputs = {'high': df['HIGH'], 'low': df['LOW'], 'close': df['CLOSE'], 'timeperiod': 14}
            df1['Indicator_'+str(i)] = talib.WILLR(**inputs)
            indict.append('Indicator_'+str(i))
        elif indicator == 'HIGH':
            df1['Indicator_'+str(i)] = df['HIGH']
            indict.append('Indicator_'+str(i))
        elif indicator == 'OPEN':
            df1['Indicator_'+str(i)] = df['OPEN']
            indict.append('Indicator_'+str(i))
        elif indicator == 'CLOSE':
            df1['Indicator_'+str(i)] = df['CLOSE']
            indict.append('Indicator_'+str(i))
        elif indicator == 'LOW':
            df1['Indicator_'+str(i)] = df['LOW']
            indict.append('Indicator_'+str(i))
    
    df1.dropna(subset=list(indict),inplace=True)
    df1.sort_index(inplace=True)
    df1.fillna(' ', inplace=True)
    df1 = df1.sort_values(by='DATE', ascending=True)
    df1.to_csv(f'{symbol}_Indicator.csv', index=False)
    df1.reset_index(drop=True)
    df1.index = range(1, len(df1)+1)
    return df1
