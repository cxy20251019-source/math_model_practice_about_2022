from pathlib import Path
import pandas as pd
from charset_normalizer import from_path
#==========================================表'2022_APMCM_C_Data.csv'=================================================
path = Path(__file__).resolve().parent/'data'/'2022_APMCM_C_Data.csv'
result = from_path(path).best()
df = pd.read_csv(path, encoding = 'cp1250')
# #计算数据缺失率
# na_city = df.groupby('City')['AverageTemperature'].agg(
#     size='size',
#     na_num=lambda x: x.isna().sum()
# )
# na_city['na_rate'] = na_city['na_num'] / na_city['size']
# na_city = na_city[na_city['na_num'] > 0]
# na_city = na_city.sort_values('na_rate', ascending=False)
# print(na_city)

# #计算年份缺失率
# df['year'] = pd.to_datetime(df['dt'], format='mixed').dt.year
# year_na = df.groupby('year')['AverageTemperature'].agg(
#     total='size',
#     missing=lambda x: x.isna().sum()
# )
# year_na['na_rate'] = year_na['missing'] / year_na['total']
# year_na= year_na.sort_values('na_rate', ascending=False).head(20)
# print(year_na)

#发现缺失值是因为当年未统计造成，删除
df = df.dropna(subset='AverageTemperature')
#==========================================表'Global_month_data.csv'=================================================
path = Path(__file__).resolve().parent/'data'/'Global_month_data.csv'
result = from_path(path).best()
df2 = pd.read_csv(path)
#转换数据格式
df2['date'] = pd.to_datetime(df2['date'])

#=========数据清洗=========
# # 1. 检查重复记录
# print("重复记录数：", df2.duplicated(subset=['year', 'month']).sum())
#
# # 2. 检查月份是否连续
# dates = pd.to_datetime(df2['date'])
# expected = pd.date_range('1850-01-01', '2022-03-01', freq='MS')
#
# print("缺失月份数：", len(expected.difference(pd.DatetimeIndex(dates))))
# print("额外月份数：", len(pd.DatetimeIndex(dates).difference(expected)))
#
# # 3. 检查气温计算是否一致
# error = (
#     df2['absolute_temp_C']
#     - df2['monthly_anomaly_C']
#     - df2['monthly_baseline_1951_1980_C']
# ).abs()
#
# print("最大计算误差：", error.max())

