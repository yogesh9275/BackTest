def create_df(df, stop_loss_pct, target_pct, buy_condition, sell_condition):
    # int(Target)
    # int(Stoploss)
    LastSignal = 'Sell'
    df['Remarks'] = None
    df['BuySellSignal'] = 'Hold'
    df['Entry_Price'] = None
    df['Target'] = None
    df['Stoploss'] = None
    for i in range(len(df)):
        EntryPrice = df.loc[i,'CLOSE']
        Close = df.loc[i,'CLOSE']
        
        if LastSignal == 'Sell' and buy_condition == 'crossover':
            if df['Indicator_0'].iat[i-1] > df['Indicator_1'].iat[i-1] and df['Indicator_0'].iat[i] < df['Indicator_1'].iat[i]:
                df.loc[i,'BuySellSignal'] = 'Buy'
                df.loc[i,'Entry_Price'] = EntryPrice
                df.loc[i, 'Remarks'] = 'Cross Over'
                Target = EntryPrice + ((EntryPrice*(target_pct))/100)
                Stoploss = EntryPrice - ((EntryPrice*(stop_loss_pct))/100)
                df.loc[i, 'Target'] = Target
                df.loc[i, 'Stoploss'] = Stoploss
                LastSignal = 'Buy'
                # print('Cross Over Buy')
            else:
                df.loc[i,'BuySellSignal']  = 'Hold'
        elif LastSignal == 'Sell' and buy_condition == 'greaterthan':
            if df['Indicator_0'].iat[i] > df['Indicator_1'].iat[i]:
                df.loc[i,'BuySellSignal'] = 'Buy'
                df.loc[i,'Entry_Price'] = EntryPrice
                df.loc[i, 'Remarks'] = 'greaterthan'
                Target = EntryPrice + ((EntryPrice*(target_pct))/100)
                Stoploss = EntryPrice - ((EntryPrice*(stop_loss_pct))/100)
                df.loc[i, 'Target'] = Target
                df.loc[i, 'Stoploss'] = Stoploss
                LastSignal = 'Buy'
                # print('greaterthan Buy')
            else:
                df.loc[i,'BuySellSignal']  = 'Hold'
        elif LastSignal == 'Buy' and sell_condition == 'crossdown':
            if df['Indicator_2'].iat[i-1] < df['Indicator_3'].iat[i-1] and df['Indicator_2'].iat[i] > df['Indicator_3'].iat[i]:
                if Close > Target:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'Target Hit'
                    # print('Target Hit')
                elif Close < Stoploss:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'Stoploss Hit'
                    # print('Stop Loss Hit')
                else:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'Cross Down'
                    # print('Cross Down Sell')

            else:
               df.loc[i,'BuySellSignal']  = 'Hold'
        elif LastSignal == 'Buy' and sell_condition == 'lessthan':
            if df['Indicator_2'].iat[i] < df['Indicator_3'].iat[i]:
                if Close > Target:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'Target Hit'
                    # print('Target Hit')
                elif Close < Stoploss:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'Stoploss Hit'
                    # print('Stop Loss Hit')
                else:
                    df.loc[i,'BuySellSignal']  = 'Sell'
                    LastSignal = 'Sell'
                    df.loc[i,'Exit_Price'] = EntryPrice
                    df.loc[i, 'Remarks'] = 'lessthan'
                    # print('Lessthan Sell')
        
            else:
                df.loc[i,'BuySellSignal']  = 'Hold'
               
    if LastSignal == 'Buy' and df['BuySellSignal'].iloc[-1] == 'Hold':
        df.loc[i,'BuySellSignal']  = 'Sell'
        LastSignal = 'Sell'
        df.loc[i,'Exit_Price'] = EntryPrice
        df.loc[i, 'Remarks'] = 'Last Index Sell'
        # print('Last Index Sell')
    df.to_csv('BackTEST.csv')
    df = calculate_PNL(df)
    df.drop(df[df['BuySellSignal'] != 'Sell'].index, inplace=True)
    df = df[['DATE','Indicator_0','Indicator_1','Indicator_2','Indicator_3','Entry_Price','Exit_Price','Stoploss','Target','PNL', 'PNL%','Total PNL','Remarks']]
    return df


def calculate_PNL(df):
    df['PNL'] = None
    df['PNL%'] = None
    df['Total PNL'] = None

    total_pnl = 0
    entry_price = None
    for i in range(len(df)):
        exit_price =  df.loc[i,'Exit_Price']

        # Check if we have a BUY signal
        if  df.loc[i,'BuySellSignal'] == 'Buy':
            entry_price =  df.loc[i,'Entry_Price']
            target = df.loc[i,'Target']
            stoploss = df.loc[i,'Stoploss']
        
        # Check if we have a SELL signal and both entry and exit prices are available
        if df['BuySellSignal'][i] == 'Sell' and entry_price is not None and exit_price is not None:
            pnl = exit_price - entry_price
            pnl_pct = (pnl / entry_price) * 100
            df.loc[i, 'Target'] = target
            df.loc[i, 'Stoploss'] = stoploss
            df.loc[i, 'Entry_Price'] = entry_price
            df.loc[i, 'Exit_Price'] = exit_price
            df.loc[i, 'PNL'] = pnl
            df.loc[i, 'PNL%'] = pnl_pct
            total_pnl += pnl
            df.loc[i, 'Total PNL'] = total_pnl
            entry_price = None
    return df
