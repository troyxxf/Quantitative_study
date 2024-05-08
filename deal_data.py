import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from get_data import get_data_from_Yahoo
from datetime import datetime

def fetch_and_apply_strategy(data):
    if data.empty:
        print("No data available to apply strategy.")
        return data

    short_window = 10
    long_window = 50
    data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    data['signal'] = 0
    data.iloc[short_window:, data.columns.get_loc('signal')] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, 0)
    data['positions'] = data['signal'].diff()

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'].values, label='Close Price')
    plt.plot(data.index, data['short_mavg'].values, label='10-Day Moving Average')
    plt.plot(data.index, data['long_mavg'].values, label='50-Day Moving Average')
    plt.plot(data.index[data['positions'] == 1], data['Close'].values[data['positions'] == 1], 'g^', markersize=10, label='Buy Signal')
    plt.plot(data.index[data['positions'] == -1], data['Close'].values[data['positions'] == -1], 'rv', markersize=10, label='Sell Signal')
    plt.title('Stock Price and Moving Averages')
    plt.legend()
    plt.show()

    return data


def calculate_macd(data):
    # 计算短期和长期的指数移动平均
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()

    # 计算MACD线
    data['MACD'] = short_ema - long_ema

    # 计算信号线
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data
def plot_macd(data):
    plt.figure(figsize=(12, 8))

    # 绘制收盘价
    plt.subplot(211)
    plt.plot(data['Close'], label='Close Price')
    plt.title('Close Price History')
    plt.legend(loc='upper left')

    # 绘制MACD和信号线
    plt.subplot(212)
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal_Line'], label='Signal Line', color='red')
    plt.bar(data.index, data['MACD'] - data['Signal_Line'], label='Histogram', color='gray')
    plt.title('MACD')
    plt.legend(loc='upper left')
    plt.show()


def plot_macd_withSignal(data):
    plt.figure(figsize=(12, 8))

    # 绘制收盘价和买卖信号
    plt.subplot(211)
    plt.plot(data['Close'], label='Close Price', color='skyblue')
    plt.plot(data.index[data['Buy_Signal']], data['Close'][data['Buy_Signal']], '^', markersize=10, color='g',
             label='Buy Signal')
    plt.plot(data.index[data['Sell_Signal']], data['Close'][data['Sell_Signal']], 'v', markersize=10, color='r',
             label='Sell Signal')
    plt.title('Close Price Buy/Sell Signals')
    plt.legend(loc='upper left')

    # 绘制MACD和信号线
    plt.subplot(212)
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal_Line'], label='Signal Line', color='red')
    plt.bar(data.index, data['MACD'] - data['Signal_Line'], label='Histogram', color='gray')
    plt.title('MACD')
    plt.legend(loc='upper left')
    plt.show()
def generate_macd_signals(data):
    data['Buy_Signal'] = (data['MACD'] > data['Signal_Line']) & (data['MACD'].shift(1) <= data['Signal_Line'].shift(1))
    data['Sell_Signal'] = (data['MACD'] < data['Signal_Line']) & (data['MACD'].shift(1) >= data['Signal_Line'].shift(1))
    return data
def macd_strategy(data):
    data = calculate_macd(data)
    data = generate_macd_signals(data)
    # plot_macd(data)
    # plot_macd_withSignal(data)
    return data

def backtest_strategy(data):
    # 将布尔信号转换为整数，然后计算仓位
    data['Position'] = data['Buy_Signal'].astype(int) - data['Sell_Signal'].astype(int)
    data['Position'] = data['Position'].replace(to_replace=0, method='ffill')
    data['Market Return'] = data['Close'].pct_change()
    data['Strategy Return'] = data['Market Return'] * data['Position'].shift(1)
    data['Cumulative Market Returns'] = (1 + data['Market Return']).cumprod()
    data['Cumulative Strategy Returns'] = (1 + data['Strategy Return']).cumprod()
    return data
def calculate_performance(data):
    #总汇报
    total_return = data['Cumulative Strategy Returns'].iloc[-1]
    #年化回报
    annual_return = data['Cumulative Strategy Returns'].iloc[-1] ** (252/len(data)) - 1
    annual_volatility = data['Strategy Return'].std() * np.sqrt(252)
    #夏普比率
    sharpe_ratio = annual_return / annual_volatility
    #最大回撤
    max_drawdown = (data['Cumulative Strategy Returns'].cummax() - data['Cumulative Strategy Returns']).max()
    return total_return, annual_return, sharpe_ratio, max_drawdown
def basktest(data):
    data = backtest_strategy(data)
    total_return, annual_return, sharpe_ratio, max_drawdown = calculate_performance(data)
    print(f"Total Return: {total_return:.2f}")
    print(f"Annual Return: {annual_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    plt.figure(figsize=(10, 5))
    plt.plot(data['Cumulative Market Returns'], label='Market Returns')
    plt.plot(data['Cumulative Strategy Returns'], label='Strategy Returns')
    plt.title('Strategy Backtest')
    plt.legend()
    plt.show()
    return data

