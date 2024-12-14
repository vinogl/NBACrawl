from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def get_data(game_id: str, game_date: str) -> list:
    url = "https://china.nba.cn/game/%s/box-score" % game_id  # 0022400333
    page_source = {}

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    page_source["away"] = driver.page_source

    button = driver.find_element(By.XPATH, "//div[@class='button-group flex']/button[2]")
    button.click()
    time.sleep(1)

    page_source["home"] = driver.page_source

    info_list = []
    for home_away, html in page_source.items():
        soup = BeautifulSoup(html, "html.parser")

        # 获取class为summary的div标签下的所有class为summary-item的div标签的内容
        summary = soup.find('div', class_='summary')
        summary_items = [item.get_text() for item in summary.find_all('div', class_='summary-item')]

        temp_list = [
            game_id,
            game_date,
            soup.find('div', class_='title-left').find('div', class_='title').get_text().strip(),
            home_away,
            *[int(summary_items[i]) for i in [4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 18, 19, 20, 21]]
        ]
        info_list.append(temp_list)

    return info_list
