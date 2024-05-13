import tushare as ts
import time
import pandas as pd
import numpy as np
from init import *

def get_realtime_data(stock_code):
    pro = init()
    # 获取实时数据，这里用的是历史数据来模拟
    df = pro.daily(ts_code=stock_code, start_date='20240101', end_date='20240110')
    return df.iloc[-1]  # 返回最新一条数据来模拟实时数据


def moving_average_strategy(data, short_window=5, long_window=20):
    # 简单的双移动平均线交易策略
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # 创建短期和长期移动平均线
    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # 创建信号，确保长度匹配
    if len(data) >= short_window:
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    else:
        # 如果数据长度小于窗口长度，使用可用数据
        signals['signal'][:len(data)] = np.where(signals['short_mavg'][:len(data)] > signals['long_mavg'][:len(data)], 1.0, 0.0)

    # 生成交易指令
    signals['positions'] = signals['signal'].diff()
    return signals


def trade(stock_code):
    data = pd.DataFrame()
    try:
        while True:
            # 获取实时数据
            latest_data = get_realtime_data(stock_code)
            # 使用concat而不是append
            data = pd.concat([data, latest_data.to_frame().T])

            # 计算交易信号
            signals = moving_average_strategy(data)
            current_position = signals['positions'].iloc[-1]

            # 根据信号买入或卖出
            if current_position > 0:
                print(f"买入信号：在{latest_data['trade_date']}，{stock_code}")
            elif current_position < 0:
                print(f"卖出信号：在{latest_data['trade_date']}，{stock_code}")
            else:
                print("no action")
            # 每隔一定时间查询一次
            time.sleep(60)  # 每分钟查询一次，实际使用中这个时间可以调整

    except KeyboardInterrupt:
        print("停止交易")
trade("000032.SZ")