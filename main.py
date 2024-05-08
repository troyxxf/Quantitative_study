from init import *
from get_deal_amount import *
from find_target_id import *

from deal_data import *
from get_data import *
from server_jiang import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
if '__main__' == __name__:
    all_text="------Start------        "
    for stock in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']:
        # 使用函数
        start_date = datetime(2022, 1, 1)
        # end_date=datetime(2024, 1, 1)
        end_date = datetime.today()
        # 获取数据
        data = get_data_from_Yahoo(stock, start_date, end_date)
        # 使用策略
        strategy_data = macd_strategy(data)
        if strategy_data['Buy_Signal'].iloc[-1] == True:
            text="------Buy Signal for {}------   ".format(stock)
            all_text+=text
            # server_jiang_send_message(text)
            # print("Buy Signal for AAPL", "A buy signal was generated today for AAPL.")
            # plot_macd_withSignal(strategy_data)
        elif strategy_data['Sell_Signal'].iloc[-1] == True:
            text="------Sell Signal for {}------   ".format(stock)
            all_text+=text
            # server_jiang_send_message(text)
            # print("Sell Signal for AAPL", "A sell signal was generated today for AAPL.")
            # plot_macd_withSignal(strategy_data)
        else:
            macd_current = strategy_data['MACD'].iloc[-1]
            signal_line_current = strategy_data['Signal_Line'].iloc[-1]
            if macd_current > signal_line_current:
                text = " %%{}. Current status: Predicting rise.   ".format(stock)
            else:
                text = " %%{}. Current status: Predicting fall.   ".format(stock)
            all_text += text
            # print("No Signal for {}".format(stock))
            # plot_macd_withSignal(strategy_data)

    server_jiang_send_message(all_text)
    # print(all_text)
    # 回测结果
    # backtest_data = basktest(strategy_data)




    # # get_deal_amount()
    # pro=init()
    # # df = pro.daily(ts_code='000001.SZ', start_date='20240430', end_date='20240430')
    # #
    # # print(df)
    # # find_target_id("深桑达A")
    # plot_trade_data('000032.SZ', '20240430', '20240430')

