import tushare as ts

# ts.set_token('471872b540c262a114dcc5b089eb1dd4e65f75385d13fa866010060d')
#
# pro = ts.pro_api()

def init():
    ts.set_token('471872b540c262a114dcc5b089eb1dd4e65f75385d13fa866010060d')

    pro = ts.pro_api()
    return pro
# df = pro.daily(ts_code='000001.SZ', start_date='20240430', end_date='20240430')
#
# print(df)