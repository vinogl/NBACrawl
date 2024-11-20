import sys

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    else:
        print(f"请求失败，状态码：{response.status_code}")
        sys.exit()


def get_trend(trend_route: str) -> list:
    url = 'https://nba.titan007.com%s' % trend_route
    soup = get_soup(url)

    trend_table = soup.find('span', id='odds2').find('table')

    # 提取表格中的所有行
    trend_all = trend_table.find_all('tr')
    trend_list = []

    for row in trend_all[1:]:
        row_data = [cell.get_text() for cell in row.find_all('td')]
        if "走地" not in row_data[-1]:
            row_info = row_data[-1].split()
            row_data.pop()
            row_data.append(row_info[0])
            row_data.append(row_info[1])
            trend_list.append(row_data)

    return trend_list
