from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pandas as pd
import time
import random

# ================== 数据配置区 ==================
SEASONS = [
    {
        "season": 1,
        "tt_ids": [
            "tt3464768", "tt3857028", "tt3858672", "tt3864892",
            "tt3876380", "tt3866650", "tt3884286", "tt3895284",
            "tt3895286", "tt3895288"
        ]
    },
    {
        "season": 2,
        "tt_ids": [
            "tt3824148", "tt4462674", "tt4462676", "tt4462678",
            "tt4462682", "tt4462680", "tt4462684", "tt4462686",
            "tt4462688", "tt4462690"
        ]
    },
    {
        "season": 3,
        "tt_ids": [
            "tt5554490", "tt5579594", "tt5719532", "tt5719534",
            "tt5719536", "tt5719540", "tt5719542", "tt5719546",
            "tt5719544", "tt5570804"
        ]
    },
    {
        "season": 4,
        "tt_ids": [
            "tt7073996", "tt7073998", "tt7074002", "tt7074006",
            "tt7074010", "tt7074012", "tt7074020", "tt7074022",
            "tt7074032", "tt7074030"
        ]
    },
    {
        "season": 5,
        "tt_ids": [
            "tt8772146", "tt8772148", "tt8772190", "tt8772192",
            "tt8772194", "tt8772196", "tt8772216", "tt8772218",
            "tt8772220", "tt8772224"
        ]
    },
    {
        "season": 6,
        "tt_ids": [
            "tt11630814", "tt12187028", "tt12187032", "tt12187036",
            "tt12187034", "tt12187038", "tt12187040", "tt12187044",
            "tt12187042", "tt12187048", "tt12188568", "tt12188572",
            "tt11630828"
        ]
    }
]

OUTPUT_FILE = "better_call_saul_episodes_full.csv"
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