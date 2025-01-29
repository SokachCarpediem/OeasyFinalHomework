from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import time
import random

# ================== 配置区 ==================
SEASONS = [
    {
        "season": 1,
        "tt_ids": [
            "tt0959621", "tt1054724", "tt1054725",
            "tt1054726", "tt1054727", "tt1054728", "tt1054729"
        ]
    },
    {
        "season": 2,
        "tt_ids": [
            "tt1232244", "tt1232249", "tt1232250", "tt1232251",
            "tt1232252", "tt1232253", "tt1232254", "tt1232255",
            "tt1232256", "tt1232245", "tt1232246", "tt1232247", "tt1232248"
        ]
    },
    {
        "season": 3,
        "tt_ids": [
            "tt1528116", "tt1615186", "tt1615187", "tt1615554",
            "tt1615555", "tt1615556", "tt1615944", "tt1615557",
            "tt1615558", "tt1615550", "tt1615551", "tt1615552", "tt1615553"
        ]
    },
    {
        "season": 4,
        "tt_ids": [
            "tt1683084", "tt1683089", "tt1683090", "tt1683091",
            "tt1683092", "tt1683093", "tt1683094", "tt1683095",
            "tt1683096", "tt1683085", "tt1683086", "tt1683087", "tt1683088"
        ]
    },
    {
        "season": 5,
        "tt_ids": [
            "tt2081647", "tt2301457", "tt2301459", "tt2301461",
            "tt2301463", "tt2301465", "tt2301467", "tt2301469",
            "tt2301471", "tt2301443", "tt2301445", "tt2301447",
            "tt2301449", "tt2301451", "tt2301453", "tt2301455"
        ]
    }
]

OUTPUT_FILE = "breaking_bad_episodes_full.csv"
CHROMEDRIVER_PATH = "chromedriver.exe"

# ================== 工具函数 ==================
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def parse_air_date(date_str):
    """转换播出日期格式"""
    try:
        clean_date = date_str.replace("Episode aired ", "").strip()
        date_obj = datetime.strptime(clean_date, "%b %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
    except:
        return date_str  # 保留原始格式如果解析失败

# ================== 核心爬取逻辑 ==================
def get_episode_data(driver, tt_id):
    """获取单集完整数据"""
    url = f"https://www.imdb.com/title/{tt_id}/"

    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='hero__primary-text']"))
        )

        # 获取基础信息
        title = driver.find_element(
            By.CSS_SELECTOR,
            "[data-testid='hero__primary-text']"
        ).text.strip()

        # 获取评分信息
        rating = float(driver.find_element(
            By.CSS_SELECTOR,
            "span[class*='imUuxf']"
        ).text.strip())

        # 投票数处理
        votes_text = driver.find_element(
            By.CSS_SELECTOR,
            "div[class*='dwhNqC']"
        ).text.strip().upper()
        votes = int(float(votes_text.replace('K', '')) * 1000) if 'K' in votes_text else int(votes_text.replace(',', ''))

        # 获取播出日期
        air_date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                "//li[contains(@class, 'ipc-inline-list__item') and contains(text(), 'Episode aired')]"))
        )
        air_date = parse_air_date(air_date_element.text)

        # 获取导演信息（原代码保持不变）
        directors = []
        try:
            director_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//li[.//span[text()='Director' or text()='Directors']]"))
            )
            directors = [a.text for a in director_section.find_elements(
                By.CSS_SELECTOR,
                "a.ipc-metadata-list-item__list-content-item--link"
            )]
        except:
            pass

        return {
            "Title": title,
            "Director": ", ".join(directors),
            "AirDate": air_date,
            "Rating": rating,
            "Votes": votes
        }

    except Exception as e:
        print(f"爬取 {tt_id} 失败: {str(e)}")
        return None

# ================== 主程序 ==================
def main():
    driver = init_driver()
    all_data = []

    for season in SEASONS:
        season_num = season["season"]
        print(f"正在处理第 {season_num} 季...")

        for ep_num, tt_id in enumerate(season["tt_ids"], start=1):
            print(f"正在抓取 S{season_num:02}E{ep_num:02} ({tt_id})...")

            if data := get_episode_data(driver, tt_id):
                data.update({
                    "Season": season_num,
                    "Episode": ep_num,
                    "EpisodeID": f"S{season_num:02d}E{ep_num:02d}",
                    "TTID": tt_id
                })
                all_data.append(data)

            time.sleep(random.uniform(1.5, 3.5))

    driver.quit()

    # 生成数据表
    df = pd.DataFrame(all_data)
    column_order = [
        "Season", "Episode", "EpisodeID", "TTID",
        "Title", "Director", "AirDate", "Rating", "Votes"
    ]
    df[column_order].to_csv(OUTPUT_FILE, index=False)
    print(f"数据已保存至 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()