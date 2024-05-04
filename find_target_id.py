from init import *

def find_target_id(target_name):
    pro=init()
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    target_stock = data[data['name'] == target_name]

    if not target_stock.empty:
        print(f"股票代码是: {target_stock.iloc[0]['ts_code']}")
    else:
        print(f"没找到{target_name}")
