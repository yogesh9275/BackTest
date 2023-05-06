import pandas as pd
from datetime import datetime
# from GetData import BuySellSignal, StockMarketData, PNLCreater
# from Indicator import IndicatorData
from testing.GetData import BuySellSignal, StockMarketData, PNLCreater
from testing.Indicator import IndicatorData


def TakeTrader(Symbol, StartDate, EndDate, Target, Stoploss, Indicator1, Indicator2, Indicator3, Indicator4, BuyAction,
               SellAction, TotalAmount, ShareQuantity, Period1=0, Period2=0, Period3=0, Period4=0,):
    
    # print('Symbol:',Symbol,type(Symbol))
    # print('FromDate:', StartDate, type(StartDate))
    # print('EndDate:', EndDate, type(EndDate))
    # print('Indicator1:', Indicator1, type(Indicator1))
    # print('Indicator2:', Indicator2, type(Indicator2))
    # print('Indicator3:', Indicator3, type(Indicator3))
    # print('Indicator4:', Indicator4, type(Indicator4))
    # print('BuyAction:', BuyAction, type(BuyAction))
    # print('SellAction:', SellAction, type(SellAction))
    # print('Period1:', Period1, type(Period1))
    # print('Period2:', Period2, type(Period2))
    # print('Period3:', Period3, type(Period3))
    # print('Period4:', Period4, type(Period4))
    df = StockMarketData(Symbol, StartDate, EndDate)
    # print(df)
    df = IndicatorData(df, Indicator1, 1, int(Period1))
    df = IndicatorData(df, Indicator2, 2, int(Period2))
    df = IndicatorData(df, Indicator3, 3, int(Period3))
    df = IndicatorData(df, Indicator4, 4, int(Period4))
    df = df.dropna()
    df.reset_index(inplace=True)
    df.drop(df.columns[[0,]], axis=1, inplace=True)
    df['BuySellSignal'] = None
    print(df)
    df = BuySellSignal(df, BuyAction, SellAction, int(Target), int(Stoploss),int(TotalAmount), int(ShareQuantity))
    
    df = df.loc[(df['BuySellSignal'] == 'Buy') | (df['BuySellSignal'] == 'Sell')]
    print('Only buy and sell >>>>>>>>\n',df)
    df.reset_index(inplace=True,drop=True)
    df= PNLCreater(df,ShareQuantity)
    print('PNL >>>>>>>>\n',df)
    return df
    # print(len(df))
    # df.to_csv(
    #     f'E:\\Cdrive\\Desktop\\Vatsal files\\Vatsal office\\data science\\Vatsal office work\\Personal project\\StockMarketProject\\Results\\{StrategyName} for {Symbol}.csv')

    # print(df)



# Symbol = "TITAN"
# StartDate = '2020-03-04'
# EndDate = '2023-04-04'
# Indicator1 = 'CLOSE'
# Indicator2 = 'SuperTrend'
# Indicator3 = 'CLOSE'
# Indicator4 = 'SuperTrend'
# Period1 = 0
# Period2 = 0
# Period3 = 0
# Period4 = 0
# BuyAction = 'GreaterThan'
# SellAction = 'LessThan'
# Target = 3
# Stoploss = 2
# TotalAmount = 100000
# ShareQuantity = 2


# df = TakeTrader(Symbol, StartDate, EndDate, Target, Stoploss, Indicator1, Indicator2, Indicator3, Indicator4, BuyAction,
#                SellAction, TotalAmount, ShareQuantity, Period1=0, Period2=0, Period3=0, Period4=0,)
# df.to_csv('BackTestResult.csv')

# print(TakeTrader(Symbol, StartDate, EndDate, Indicator1, Indicator2, Indicator3, Indicator4, BuyAction,
#                SellAction, Period1, Period2, Period3, Period4,))

