import tushare as ts
from private_param import tushare_token

#
# pro = ts.pro_api()

def init():
    token=tushare_token
    # print(token)
    ts.set_token(token)

    pro = ts.pro_api()
    return pro
# df = pro.daily(ts_code='000001.SZ', start_date='20240430', end_date='20240430')
#
# print(df)