import sys
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
# 获取项目根目录（2022题C）
project_dir = Path(__file__).resolve().parent.parent
# 将项目根目录加入模块搜索路径
sys.path.insert(0, str(project_dir))
# 导入清洗后的两个 DataFrame
from data_clean import df, df2
march_tem_diff = df2[(df2.year == 2022) & (df2.month == 3)].absolute_temp_C.iloc[0] - df2[(df2.year == 2012) & (df2.month == 3)].absolute_temp_C.iloc[0]
avg_uptemp = march_tem_diff/10
#找到截止于2022年3月的最新窗口
window = df2.loc[
    (df2['date'] >= '2012-04-01') &
    (df2['date'] <= '2022-03-01')
].sort_values('date')

print(len(window))  # 应为120
# 时间单位：年
x = np.arange(len(window)) / 12
# 使用月度气温距平，消除固定季节性基准差异
y = window['monthly_anomaly_C']
slope, intercept = np.polyfit(x, y, 1)
print(f"十年升温趋势：{slope:.4f} °C/年")
target_slope = slope


# 按日期排序，重置索引
df2 = df2.sort_values('date').reset_index(drop=True)
results = []
# 从第121个月开始，逐月构造十年窗口
for i in range(122, len(df2) - 12, 12):
    # 十年前和当前月份的气温
    start = df2.iloc[i - 120]
    end = df2.iloc[i]
    # 1. 十年首尾温差
    temp_diff = end['absolute_temp_C'] - start['absolute_temp_C']
    # 2. 平均升温速度
    warming_rate = temp_diff / 10
    # 3. 最近120个月的线性回归斜率
    window = df2.iloc[i - 119:i + 1]
    x = np.arange(120)
    y = window['monthly_anomaly_C']
    slope = np.polyfit(x, y, 1)[0] * 12
    # 保存每个窗口的结果
    results.append({
        'start_date': start['date'],
        'end_date': end['date'],
        'temp_diff': temp_diff,
        'warming_rate': warming_rate,
        'slope': slope
    })
# 转换为DataFrame
df_windows = pd.DataFrame(results)
#开始统计22年三月结尾的十年在所有十年区间中的排名如何
# 1. 2022年3月的十年升温指标
target_diff = march_tem_diff  # 之前计算过的首尾温差
# 2q. 比较函数
def compare_history(column, target_value):
    history = df_windows[column]

    # 历史排名（越大排名越靠前）
    rank = (history > target_value).sum() + 1

    # 超过了百分之多少的历史窗口
    percentile = (history < target_value).mean() * 100

    return {
        '2022年指标': target_value,
        '历史平均值': history.mean(),
        '历史最大值': history.max(),
        '历史最小值': history.min(),
        '历史排名': f'{rank}/{len(history) + 1}',
        '超过历史窗口比例': f'{percentile:.2f}%'
    }

# 4. 分别计算两个指标
comparison = pd.DataFrame({
    '首尾温差': compare_history('temp_diff', target_diff),
    '回归斜率': compare_history('slope', target_slope)
}).T

print(comparison.to_string())

#=======================保存结果=======================
# 2022年3月的结果与162个历史窗口合并
target = pd.DataFrame([{
    'start_date': '2012-03-01',
    'end_date': '2022-03-01',
    'temp_diff': march_tem_diff,
    'slope': target_slope,
    'is_target': True
}])

history = df_windows.copy()
history['is_target'] = False

plot_data = pd.concat([history, target], ignore_index=True)

# 保存到data文件夹
project_dir = Path(__file__).resolve().parent.parent

plot_data.to_csv(
    project_dir / 'data' / 'warming_results.csv',
    index=False,
    encoding='utf-8-sig'
)

print("保存成功：", len(plot_data), "个窗口")

#=====================检验结果准确性======================
# 选择2012年4月—2022年3月的数据
window = df2[
    (df2['date'] >= '2012-04-01') &
    (df2['date'] <= '2022-03-01')
].sort_values('date')

assert len(window) == 120

# 时间单位：年
x = np.arange(120) / 12
y = window['monthly_anomaly_C'].to_numpy()

# 构造带截距的线性回归
X = sm.add_constant(x)

# 普通最小二乘回归
ols = sm.OLS(y, X).fit()

# HAC稳健标准误，考虑最多12个月的残差相关
hac = sm.OLS(y, X).fit(
    cov_type='HAC',
    cov_kwds={'maxlags': 12}
)

# 输出比较结果
print(f"回归斜率：{ols.params[1]:.6f} °C/年")
print(f"普通OLS标准误：{ols.bse[1]:.6f}")
print(f"HAC稳健标准误：{hac.bse[1]:.6f}")

ci_low, ci_high = hac.conf_int()[1]

print(f"HAC 95%置信区间：[{ci_low:.6f}, {ci_high:.6f}]")
print(f"HAC p值：{hac.pvalues[1]:.6f}")
for lag in [6, 12, 18, 24]:
    model = sm.OLS(y, X).fit(
        cov_type='HAC',
        cov_kwds={'maxlags': lag}
    )

    print(
        f"lag={lag:2d}, "
        f"SE={model.bse[1]:.6f}, "
        f"p={model.pvalues[1]:.6f}"
    )