from init import *
import pandas as pd
import os

def get_top10_holders(ts_code, start_date, end_date):
    pro = init()
    df = pro.top10_holders(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df
def check_social_security_in_holders(df):

    social_security_holders = []
    if df.empty:
        # print("DataFrame是空的，没有股东数据。")
        return social_security_holders
    for name in df['holder_name']:
        if '社保' in name:
            social_security_holders.append(name)
    return social_security_holders



def save_to_file(data, filename):
    """
    将新的股东信息保存到文件中，如果记录已存在则跳过。
    :param data: 包含日期、股票代码和社保股东名单的数据。
    :param filename: 保存文件的名称。
    """

    if not os.path.exists(filename):
        # 如果文件不存在，则创建一个新文件并添加标题
        df = pd.DataFrame(columns=["date", "ts_code", "social_security_holders"])
        df.to_csv(filename, index=False)

    # 加载现有数据
    existing_df = pd.read_csv(filename)

    # 检查是否已有相同的记录
    if not existing_df[(existing_df['date'] == data['date']) &
                       (existing_df['ts_code'] == data['ts_code']) &
                       (existing_df['social_security_holders'] == data['social_security_holders'])].empty:
        return  # 如果记录已存在，跳过保存

    # 否则，将新记录添加到文件
    new_df = pd.DataFrame([data])
    new_df.to_csv(filename, mode='a', header=False, index=False)


def find_social_security():
    filename = "social_security_holders.csv"
    prefixes = ['600', '601', '603', '000', '001', '002', '300']
    for prefix in prefixes:
        for i in range(1000):
            ts_code = "{}{:03d}.SZ".format(prefix, i)
            start_date = '20240105'
            end_date = '20240511'
            df = get_top10_holders(ts_code, start_date, end_date)
            social_security_holders = check_social_security_in_holders(df)
            if social_security_holders:
                # 将结果保存到文件
                data = {
                    "date": end_date,  # 使用查询的结束日期作为记录日期
                    "ts_code": ts_code,
                    "social_security_holders": ";".join(social_security_holders)  # 使用分号分隔股东名字
                }
                save_to_file(data, filename)
                print("{}中社保持股人：".format(ts_code), social_security_holders)

find_social_security()