import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Rectangle

# 配置参数
CSV_PATH = "breaking_bad_episodes_full.csv"
COLORS = [
    '#ffff00',  # 黄色 (7.5-8)
    '#d9f0a3',  # 浅绿 (8-8.5)
    '#78c679',  # 中绿 (8.5-9)
    '#238443',  # 深绿 (9-9.5)
    '#005a32'  # 墨绿 (9.5-10)
]
BINS = [7.5, 8, 8.5, 9, 9.5, 10]

# 加载数据
df = pd.read_csv(CSV_PATH)
df = df[['Season', 'Episode', 'Rating']].dropna()

# 创建画布（调整为更长而不是更宽）
fig, ax = plt.subplots(figsize=(10, 20))  # 更窄但更长

ax.set_aspect('equal')

# 隐藏所有坐标轴线
for spine in ax.spines.values():
    spine.set_visible(False)

# 计算布局参数
max_season = df.Season.max()
max_episode = df.groupby('Season')['Episode'].max().max()
cell_size = 1.0  # 调整单元格大小以适应新布局

# 创建自定义颜色映射
cmap = mcolors.ListedColormap(COLORS)
norm = mcolors.BoundaryNorm(BINS, cmap.N)

# 绘制热力格子
for season in range(1, max_season + 1):
    season_df = df[df.Season == season]

    for _, row in season_df.iterrows():
        x = season * cell_size + 0.5  # 调整X坐标以适应新布局
        y = (max_episode - row['Episode'] + 1) * cell_size - 0.5  # 调整Y坐标以适应新布局

        color = cmap(norm(row['Rating']))

        # 绘制方块
        rect = Rectangle(
            (x, y), cell_size, cell_size,
            facecolor=color,
            edgecolor='white',
            linewidth=2
        )
        ax.add_patch(rect)

        # 添加评分文本
        ax.text(
            x + cell_size / 2, y + cell_size / 2,
            f"{row['Rating']:.1f}",
            ha='center', va='center',
            color='black' if row['Rating'] < 9 else 'white',
            fontsize=10
        )

# 设置坐标轴范围
ax.set_xlim(0, (max_season + 2) * cell_size)  # 增加一点额外的空间
ax.set_ylim(0, (max_episode + 3) * cell_size)  # 增加额外空间以便放置标题和编号

# 添加标题系统 -------------------------------------------------
# 顶部Season标题
ax.text(
    (max_season + 1) / 1.6, max_episode * cell_size + 1.55,  # 调整Y位置以增加空间
    'Season',
    ha='center', va='center',
    fontsize=16,
    fontweight='bold'
)

# 季节编号
for season in range(1, max_season + 1):
    ax.text(
        season * cell_size + 1, max_episode * cell_size + 0.85,  # 调整Y位置以适应新布局
        str(season),
        ha='center', va='center',
        fontsize=12
    )

# 左侧Episode系统 -------------------------------------------------
# Episode标题
ax.text(
    -0.2, (max_episode + 1) / 2,  # X位置向左移动以避免与矩形重叠
    'Episode',
    ha='center', va='center',
    rotation=90,
    fontsize=16,
    fontweight='bold'
)

# 集数编号
for ep in range(1, max_episode + 1):
    ax.text(
        1.05, max_episode - ep + 0.95,  # Y位置调整以适应新布局及行间距
        str(ep),
        ha='right', va='center',
        fontsize=10
    )

# 隐藏坐标轴
ax.set_xticks([])
ax.set_yticks([])
ax.tick_params(axis='both', which='both', length=0)

# 设置主标题
plt.title("Breaking Bad Episodes Rating Matrix",
          y=0.95, fontsize=18,  # 调整Y位置和字体大小
          fontweight='bold')

plt.tight_layout()
plt.show()