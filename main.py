from init import *
from get_deal_amount import *
from find_target_id import *

if '__main__' == __name__:
    # get_deal_amount()
    pro=init()
    # df = pro.daily(ts_code='000001.SZ', start_date='20240430', end_date='20240430')
    #
    # print(df)
    # find_target_id("深桑达A")
    plot_trade_data('000032.SZ', '20240430', '20240430')

