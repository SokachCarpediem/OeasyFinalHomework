# OeasyFinalHomework 网页抓取与数据处理 - 期末作业

本项目旨在通过Selenium进行网页抓取，并对《绝命毒师》和《风骚律师》两部剧集在IMDb上的评分及相关信息进行分析。项目包括爬虫代码、数据存储、热力图和散点图绘制以及网页制作。

## 目录结构

- `bb_scrawler.py`：用于爬取《绝命毒师》的相关数据。
- `bcs_scrawler.py`：用于爬取《风骚律师》的相关数据。
- `breaking_bad_episodes_full.csv`：存储《绝命毒师》的数据。
- `better_call_saul_episodes_full.csv`：存储《风骚律师》的数据。
- `bb_rating.py`：生成《绝命毒师》评分的热力图。
- `bcs_rating.py`：生成《风骚律师》评分的热力图。
- `director.py`：生成导演评分关系的散点图。
- `Main_Page.html`：主页面HTML文件，包含导航至不同页面的功能。

## 使用说明

### 爬取数据

1. **《绝命毒师》**
    ```bash
    python bb_scrawler.py
    ```
2. **《风骚律师》**
    ```bash
    python bcs_scrawler.py
    ```

### 数据可视化

#### 热力图

- **《绝命毒师》**
    ```bash
    python bb_rating.py
    ```
- **《风骚律师》**
    ```bash
    python bcs_rating.py
    ```

#### 散点图

- **导演评分关系**
    ```bash
    python director.py
    ```

### 网页展示

打开`Main_Page.html`即可浏览项目的主要成果，该页面提供导航按钮以方便切换查看不同的图表和数据。
