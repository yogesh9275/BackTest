from django.shortcuts import render
import pandas as pd
# from .Data import download_stock_data
# from .apply_Indicator import add_indicators
# from .PNL_Report import create_df
from .TakeTrade import TakeTrader

def my_view(request):
    if request.method == 'POST':
        stock_name = request.POST.get('stock_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        indicator1 = request.POST.get('indicator1')
        indicator2 = request.POST.get('indicator2')
        indicator3 = request.POST.get('indicator3')
        indicator4 = request.POST.get('indicator4')
        buy_condition = request.POST.get('buy_condition')
        sell_condition = request.POST.get('sell_condition')
        stoploss = request.POST.get('stoploss')
        target = request.POST.get('target')
        total_amount = request.POST.get('total_amount')
        share_quantity = request.POST.get('share_quantity')

        # # Call download_stock_data() to download stock data and save to CSV file
        # data = download_stock_data(stock_name, start_date, end_date)

        # # Apply Indicator
        # indicators = []
        # indicators.extend([indicator1, indicator2, indicator3, indicator4])
        # print(indicators)
        # df = add_indicators(indicators, data)

        # # PNL 
        # print(f'Target = {target}\nStop Loss = {stoploss}\nBuy Condtion = {buy_condition}\nSell Condtion = {sell_condition}')
        # stoploss = float(stoploss)
        # target = float(target)
        # buy_condition = str(buy_condition)
        # sell_condition = str(sell_condition)
        # df = create_df(df, stoploss, target, buy_condition, sell_condition)
        # # Add the DataFrame to the context dictionary
        
        df =  TakeTrader(stock_name, start_date, end_date, target, stoploss, indicator1, indicator2, indicator3, indicator4, buy_condition,
               sell_condition, total_amount, share_quantity, Period1=0, Period2=0, Period3=0, Period4=0,)
        context = {
            'stock_name': stock_name,
            'start_date': start_date,
            'end_date': end_date,
            'indicator1': indicator1,
            'indicator2': indicator2,
            'indicator3': indicator3,
            'indicator4': indicator4,
            'stoploss': stoploss,
            'target': target,
            'total_amount': total_amount,
            'share_quantity': share_quantity,
            'data':df.to_html(classes='my-table', index=False),
        }

        return render(request, 'output.html', context=context)
    else:
        return render(request, 'input.html')

# except Exception as e:
        #     context = {
        #         'error': str(e)
        #     }
        #     return render(request, 'error.html', context=context)

