import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取之前保存的建模结果
project_dir = Path(__file__).resolve().parent.parent
path = project_dir / 'data' / 'warming_results.csv'

df = pd.read_csv(path)

# 分离历史窗口与2022年目标窗口
is_target = df['is_target'].astype(str).str.lower().eq('true')
history = df.loc[~is_target]
target = df.loc[is_target].iloc[0]

# 2. 设置Seaborn风格
sns.set_theme(style='whitegrid', context='paper', font_scale=1.3)

fig, ax = plt.subplots(figsize=(9, 6))

# 3. 绘制历史窗口
sns.scatterplot(
    data=history,
    x='slope',
    y='temp_diff',
    color='steelblue',
    alpha=0.65,
    s=65,
    label='Historical Windows',
    ax=ax
)

# 4. 突出显示2022年3月
ax.scatter(
    target['slope'],
    target['temp_diff'],
    color='crimson',
    s=250,
    marker='*',
    label='March 2022',
    zorder=5
)

ax.annotate(
    '2022-03',
    xy=(target['slope'], target['temp_diff']),
    xytext=(12, 12),
    textcoords='offset points',
    fontsize=11,
    fontweight='bold'
)

# 5. 历史均值参考线
ax.axvline(
    history['slope'].mean(),
    linestyle='--',
    color='gray',
    alpha=0.6
)

ax.axhline(
    history['temp_diff'].mean(),
    linestyle='--',
    color='gray',
    alpha=0.6
)

# 6. 图表设置
ax.set_xlabel('Regression Slope (°C/year)')
ax.set_ylabel('10-Year Temperature Difference (°C)')
ax.set_title('Historical 10-Year Global Warming Comparison')

ax.legend()
sns.despine()
plt.tight_layout()

# 7. 保存论文图片
plt.savefig(
    project_dir / 'figures' / 'warming_scatter.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()