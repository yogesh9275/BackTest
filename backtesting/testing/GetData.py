import holidays
import json
import pandas as pd
import requests
from datetime import date, datetime
from jugaad_data.nse import NSELive, stock_df, index_df, expiry_dates


def GetLiveMarketPrice(symbol):   
    n = NSELive()
    q = n.stock_quote(symbol)
    priceInfo = q['priceInfo']
    LivePrice = priceInfo['lastPrice']
    # print(f'\r{LivePrice}')
    # print(LivePrice,end='\r')
    return LivePrice

def ExpiryDate(date):
    date = datetime.strptime(date, '%Y-%m-%d').date()
    expiries = expiry_dates(date)
    print(expiries)
    
def ShortDate(date):
    year = int(date[2:4])
    month = int(date[5:7])
    monthstr = {
        1:'Jan',
        2:'Feb',
        3:'Mar',
        4:'Apr',
        5:'May',
        6:'Jun',
        7:'Jul',
        8:'Aug',
        9:'Sep',
        10:'Oct',
        11:'Nov',
        12:'Dec',
    }
    month= monthstr.get(month, 'None')
    return f'{month}{year}'

def HolidayFinder(date):
    # print(int(date[:4]))
    Year = int(date[:4])
    # print('>>>>>>>>>>',Year)
    india_holidays = holidays.India(years=Year)
    # print(india_holidays)
    holidays_Dates = [str(key) for key in india_holidays]
    # print(holidays_Dates)
    # print(len(holidays_Dates))
    return holidays_Dates

def StockMarketData(Symbol,start_date,end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    df = stock_df(Symbol, start_date, end_date, "EQ")
    # print(df)
    df = df[['SYMBOL', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', '52W H', '52W L']]
    df = df.iloc[::-1]
    df.reset_index(inplace=True, drop=True)
    print(df)
    return df


def BuySellSignal(df, BuyAction, SellAction, Target, Stoploss, TotalAmount, ShareQuantity ):
    # int(Target)
    # int(Stoploss)
    LastSignal = 'Sell'
    df['Remarks'] = None
    df['TotalAmount'] = None
    for i in range(len(df)):
        EntryPrice = df['CLOSE'].iat[i]
        Close = df['CLOSE'].iat[i]
        
        if LastSignal == 'Sell' and BuyAction == 'crossover' and TotalAmount > (df['CLOSE'].iat[i] * ShareQuantity):
            if df['Indicator1'].iat[i-1] < df['Indicator2'].iat[i] and df['Indicator1'].iat[i] > df['Indicator2'].iat[i]:
                df['BuySellSignal'].iat[i] = 'Buy'
                Target = EntryPrice + ((EntryPrice*(Target))/100)
                Stoploss = EntryPrice - ((EntryPrice*Stoploss)/100)
                TotalAmount = TotalAmount - (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
                LastSignal = 'Buy'
                # print('Buy')
            else:
                df['BuySellSignal'].iat[i] = 'Hold'
        elif LastSignal == 'Sell' and BuyAction == 'greaterthan' and TotalAmount > (df['CLOSE'].iat[i] * ShareQuantity):
            if df['Indicator1'].iat[i] > df['Indicator2'].iat[i]:
                df['BuySellSignal'].iat[i] = 'Buy'
                Target = EntryPrice + (EntryPrice*Target)/100
                Stoploss = EntryPrice - (EntryPrice*Stoploss)/100
                TotalAmount = TotalAmount - (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
                LastSignal = 'Buy'
                # print('Buy')
            else:
                df['BuySellSignal'].iat[i] = 'Hold'
        elif LastSignal == 'Buy' and SellAction == 'crossdown':
            if df['Indicator3'].iat[i-1] > df['Indicator4'].iat[i] and df['Indicator3'].iat[i] < df['Indicator4'].iat[i]:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Condition Satisfied'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
                # print('Sell')
            elif Target < Close:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Target Hit'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
            elif Stoploss > Close:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Stoploss Hit'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount

            else:
                df['BuySellSignal'].iat[i] = 'Hold'
        elif LastSignal == 'Buy' and SellAction == 'lessthan':
            if df['Indicator3'].iat[i] < df['Indicator4'].iat[i]:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Condition Satisfied'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
                # print('Sell')
            elif Target < Close:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Target Hit'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
            elif Stoploss>Close:
                df['BuySellSignal'].iat[i] = 'Sell'
                LastSignal = 'Sell'
                df['Remarks'].iat[i] = 'Stoploss Hit'
                TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
                df['TotalAmount'].iat[i] = TotalAmount
            else:
                df['BuySellSignal'].iat[i] = 'Hold'
        if LastSignal == 'Buy' and df['BuySellSignal'].iloc[-1] == 'Hold':
            df['BuySellSignal'].iat[i] = 'Sell'
            LastSignal = 'Sell'
            df['Remarks'].iat[i] = 'Last Index Sell'
            TotalAmount = TotalAmount + (df['CLOSE'].iat[i] * ShareQuantity)
            df['TotalAmount'].iat[i] = TotalAmount
            # print('Sell')
    df.to_csv('Signal.csv')
    
    return df

def PNLCreater(df,ShareQuantity):
    print('pnl>>',df)
    ADDdf = pd.DataFrame(columns=['Symbol','EntryDate','EntryPrice','ExitDate',
                                  'ExitPrice','PNL','PNLinPercent','TotalAmount'])
    # print('Newdf: ',ADDdf)
    for i in range(len(df)):
        if i % 2 == 0:
            # dict1 = {'Symbol':df['SYMBOL'].iat[i],
            #     'EntryDate': df['DATE'].iat[i],
            #     'EntryPrice': df['CLOSE'].iat[i],
            #     'ExitDate': df['DATE'].iat[i+1],
            #     'ExitPrice': df['CLOSE'].iat[i+1],
            #     'PNL': (df['CLOSE'].iat[i+1]-df['CLOSE'].iat[i]),
            #     'Remarks':df['Remarks'].iat[i+1],
            #       }
            # pd.concat([ADDdf, dict1], ignore_index=True)
            PNLinPerct = (((df['CLOSE'].iat[i+1]-df['CLOSE'].iat[i])/df['CLOSE'].iat[i])*100)
            ADDdf.loc[-1] = [df['SYMBOL'].iat[i],df['DATE'].iat[i+1],
                          df['CLOSE'].iat[i],df['DATE'].iat[i],df['CLOSE'].iat[i+1],
                          (round((df['CLOSE'].iat[i+1]-df['CLOSE'].iat[i])*float(ShareQuantity),2)),
                          round(PNLinPerct,2),round(df['TotalAmount'].iat[i+1],2)]  # adding a row
            ADDdf.index = ADDdf.index + 1  # shifting index
            ADDdf = ADDdf.sort_index()
            # ADDdf = ADDdf.append(dict1,ignore_index=True)
        else:
            pass
    ADDdf['ShareQuantity'] = ShareQuantity
    ADDdf = ADDdf.loc[::-1].reset_index(drop=True)
    ADDdf['CumSum'] = round(ADDdf['PNL'].cumsum(axis=0),2)
    ADDdf['HighValue'] = ADDdf['CumSum'].cummax()
    ADDdf['DrawDown'] = ADDdf['CumSum'] - ADDdf['HighValue']
    print(ADDdf)
    # FinalValue = ADDdf['CumSum'].iloc[-1]
    return ADDdf
# Symbol = "SBIN"
# StartDate = '2016-01-01'
# EndDate = '2023-03-30'
# while True:
#     print(GetLiveMarketPrice(Symbol), end='\r')
    
# df = StockMarketData(Symbol,StartDate,EndDate)
# ExpiryDate(StartDate)
# importing holidays module
# getting India holidays
# print(df)
# HolidayFinder(StartDate)

