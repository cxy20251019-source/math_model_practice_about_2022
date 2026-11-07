import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取建模结果
project_dir = Path(__file__).resolve().parent.parent
path = project_dir / 'data' / 'warming_results.csv'

df = pd.read_csv(path)

# 2. 处理时间
df['end_date'] = pd.to_datetime(df['end_date'], format='mixed')
df['year'] = df['end_date'].dt.year
df = df.sort_values('year')

# 3. 提取2022年数据
target = df[df['year'] == 2022].iloc[0]

# 4. 设置绘图风格
sns.set_theme(style='whitegrid', context='paper', font_scale=1.3)

fig, ax = plt.subplots(figsize=(12, 6))

# 5. 绘制历史十年升温趋势
sns.lineplot(
    data=df,
    x='year',
    y='slope',
    color='steelblue',
    linewidth=1.8,
    errorbar=None,
    ax=ax,
    label='10-Year Warming Trend'
)

# 6. 突出2022年
ax.scatter(
    target['year'],
    target['slope'],
    color='crimson',
    s=150,
    marker='*',
    zorder=5,
    label='March 2022'
)

ax.annotate(
    f"2022: {target['slope']:.4f}",
    xy=(target['year'], target['slope']),
    xytext=(-95, 25),
    textcoords='offset points',
    arrowprops=dict(arrowstyle='->', color='crimson'),
    fontsize=10,
    fontweight='bold'
)

# 7. 零值参考线
ax.axhline(
    y=0,
    color='gray',
    linestyle='--',
    alpha=0.7
)

# 8. 图表设置
ax.set_xlabel('Window Ending Year')
ax.set_ylabel('Regression Slope (°C/year)')
ax.set_title('Historical Evolution of 10-Year Global Warming Trends')

ax.legend()
sns.despine()
plt.tight_layout()

# 9. 保存图表
plt.savefig(
    project_dir / 'figures' / 'warming_trend_history.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()