import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 数据准备
combined = pd.concat([
    pd.read_csv('breaking_bad_episodes_full.csv'),
    pd.read_csv('better_call_saul_episodes_full.csv')
], ignore_index=True)

# 预处理
combined['AirDate'] = pd.to_datetime(combined['AirDate'])
combined['Director'] = combined['Director'].str.strip().str.title()

# 统计导演数据
director_stats = combined.groupby('Director').agg(
    AvgRating=('Rating', 'mean'),
    EpisodeCount=('Episode', 'count'),
    RatingStd=('Rating', 'std')
).reset_index().sort_values('AvgRating', ascending=False)

# 筛选有足够样本的导演 (至少执导3集)
valid_directors = director_stats[director_stats['EpisodeCount'] >= 3]

# 可视化
plt.figure(figsize=(16, 10))
cmap = sns.color_palette("viridis", as_cmap=True)

# 主散点图
scatter = sns.scatterplot(
    x='AvgRating',
    y='Director',
    size='EpisodeCount',
    sizes=(100, 400),
    hue='AvgRating',
    palette=cmap,
    data=valid_directors,
    legend='auto'
)

# 添加误差线
plt.errorbar(
    x=valid_directors['AvgRating'],
    y=valid_directors['Director'],
    xerr=valid_directors['RatingStd'],
    fmt='none',
    color='gray',
    alpha=0.6
)

# 辅助线
plt.axvline(
    x=combined['Rating'].mean(),
    color='red',
    linestyle='--',
    label=f'Overall Average ({combined["Rating"].mean():.1f})'
)

# 美化
plt.title('Director Performance Analysis\n(Size=Episodes Directed, Color=Avg Rating)', fontsize=14, pad=20)
plt.xlabel('Average Rating (with Standard Deviation)', fontsize=12)
plt.ylabel('')
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.xlim(7.5, 9.5)
plt.legend(bbox_to_anchor=(1, 0.9), frameon=False)

# 添加数据标签
for line in range(valid_directors.shape[0]):
    plt.text(
        x=valid_directors.AvgRating.iloc[line] + 0.05,
        y=line,
        s=f"{valid_directors.EpisodeCount.iloc[line]} eps",
        verticalalignment='center',
        fontsize=8
    )

plt.tight_layout()
plt.savefig('director_performance_analysis.png', dpi=300, bbox_inches='tight')
plt.show()