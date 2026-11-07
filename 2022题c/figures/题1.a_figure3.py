import pandas as pd
import numpy as np
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_dir / 'data' / 'warming_results.csv'
)

df['year'] = pd.to_datetime(
    df['end_date'], format='mixed'
).dt.year

df = df.sort_values('year').reset_index(drop=True)

target_year = 2022
target_slope = df.loc[
    df['year'] == target_year, 'slope'
].iloc[0]

results = []

# 测试不同滑动步长
for k in [1, 2, 3, 5, 10]:

    # 以2022年为锚点向前取样
    selected = df[
        (target_year - df['year']) % k == 0
    ].copy()

    # 2022年历史排名
    rank = (selected['slope'] > target_slope).sum() + 1

    # 对斜率时间序列进行线性插值
    # 只比较采样年份覆盖的区间，不进行外推
    full = df[
        df['year'].between(
            selected['year'].min(),
            selected['year'].max()
        )
    ]

    predicted = np.interp(
        full['year'],
        selected['year'],
        selected['slope']
    )

    # 重构误差
    rmse = np.sqrt(
        np.mean((full['slope'] - predicted) ** 2)
    )

    overlap = max(0, (10 - k) / 10)

    results.append({
        '步长（年）': k,
        '窗口数量': len(selected),
        '重叠比例': overlap,
        '重构RMSE': rmse,
        '2022历史排名': f'{rank}/{len(selected)}'
    })

comparison = pd.DataFrame(results)

print(comparison.to_string(index=False))