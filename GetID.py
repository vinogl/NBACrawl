from selenium import webdriver
from bs4 import BeautifulSoup
import re


def get_id(year: int, month: int, season: str) -> list:
    id_list = []

    url = "https://nba.titan007.com/cn/Normal.aspx?y=%d&m=%d&matchSeason=%s&SclassID=1" % (year, month, season)
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)  # 等待页面加载完成

    # 获取页面源码
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有<a>标签
    a_tags = soup.find_all('a')

    # 从<a>标签中提取出每场比赛ID添加到返回列表
    for tag in a_tags:
        if tag.text.strip() == '[欧]':
            match = re.search(r'/oddslist/(\d+)', tag.get('href'))
            if match:
                id_list.append(match.group(1))

    return id_list
