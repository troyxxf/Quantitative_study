import pandas_datareader as pdr
from datetime import datetime
import yfinance as yf

#输入股票代码，开始日期，结束日期，获取股票数据
def get_data_from_Yahoo(stock,start_date,end_date):
    # 设置获取数据的时间范围    # start_date = datetime(2020, 1, 1)
    #     # end_date = datetime(2023, 1, 1)


    # 创建一个ticker对象
    ticker = yf.Ticker(stock)

    # 获取股票的历史数据
    # data = ticker.history(period="1y")  # 获取最近一年的股票数据
    data = ticker.history(start=start_date, end=end_date)  # 获取指定时间范围的股票数据

    # 显示数据的前几行
    # print(data.head())

    return data
# # 设置股票代码
# stock = 'AAPL'
# start_date=datetime(2020, 1, 1)
# end_date=datetime(2023, 1, 1)
# get_data_from_Yahoo(stock,start_date,end_date)