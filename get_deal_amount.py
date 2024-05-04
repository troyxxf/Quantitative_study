import pandas as pd
import matplotlib.pyplot as plt
from init import *
def get_vol_amount(ts_code, start_date, end_date):
    pro = init()
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    if not df.empty and 'trade_date' in df.columns:
        return df[['trade_date', 'vol', 'amount']]
    else:
        return pd.DataFrame()  # 返回一个空的DataFrame作为错误处理

def plot_trade_data(ts_code, start_date, end_date):
    df = get_vol_amount(ts_code, start_date, end_date)
    if not df.empty:
        df['trade_date'] = pd.to_datetime(df['trade_date'])
        plt.figure(figsize=(10, 5))
        plt.plot(df['trade_date'], df['vol'], label='Volume')
        plt.plot(df['trade_date'], df['amount'], label='Amount')
        plt.xlabel('Date')
        plt.ylabel('Volume / Amount')
        plt.title(f'Trade Volume and Amount for {ts_code}')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("No data available")

# 示例调用
