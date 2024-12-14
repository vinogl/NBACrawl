import re
from selenium import webdriver
from bs4 import BeautifulSoup


def get_id(year: int, month: int, season: str) -> dict:

    url = "https://nba.titan007.com/cn/Normal.aspx?y=%d&m=%d&matchSeason=%s&SclassID=1" % (year, month, season)

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)  # 等待页面加载完成

    # 获取页面源码
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find(id='scheTab')  # 找到id为scheTab的表格

    id_dict = {}  # 创建一个字典来存储比赛id与比赛日期的映射
    for row in table.find_all('tr'):

        a_tag = row.find('a', string='[欧]')  # 找到该行中的<a>标签

        if a_tag:  # 如果找到了包含"[欧]"的<a>标签
            game_info = row.find_all('td')[1].text
            game_date = int(re.split('[- ]', game_info)[1])

            match = re.search(r'/oddslist/(\d+)', a_tag['href'])
            if match:
                id_dict[match.group(1)] = game_date

    return id_dict
