from datetime import datetime
from jugaad_data.nse import stock_df

def download_stock_data(stock_name, start_date, end_date):
    
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # Download stock data to pandas dataframe
    data = stock_df(symbol=stock_name, from_date=start_date,to_date=end_date, series="EQ")
    print("Data has been Downloaded")
    # print(data.columns)
    
    # Store the data in a CSV file
    # filename = f"{stock_name}.csv"
    # data.to_csv(filename)

    # Return the filename
    return data