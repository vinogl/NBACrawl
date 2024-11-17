import requests
from bs4 import BeautifulSoup


def resolve_score_table(soup_table) -> dict:
    t_all = soup_table.find('tbody').find_all('tr')  # 获取表格的所有的行

    # 获取OT列的索引
    headers = [th.text for th in t_all[0] if th.text not in ['\n', '完']]
    c_quarter = [i for i, header in enumerate(headers) if '节' in header]  # 每节得分列
    c_ot = [i for i, header in enumerate(headers) if "'OT" in header]  # 加时赛列

    # 获取主队和客队的得分数据
    home_scores = [int(cell.text) for cell in t_all[1].find_all('td')]
    guest_scores = [int(cell.text) for cell in t_all[2].find_all('td')]

    # 提取每节得分
    home_quarter = {f'home_{i + 1}': home_scores[index] for i, index in enumerate(c_quarter)}
    guest_quarter = {f'guest_{i + 1}': guest_scores[index] for i, index in enumerate(c_quarter)}

    # 提取加时赛得分
    home_ot = sum(home_scores[i] for i in c_ot)
    guest_ot = sum(guest_scores[i] for i in c_ot)

    # 存储数据到指定字段
    score_dict = {
        **home_quarter,
        **guest_quarter,
        'home_ot': home_ot,
        'guest_ot': guest_ot
    }

    return score_dict


def resolve_odds_table(soup_table) -> dict:
    url_dict = {}
    tr_all = soup_table.find_all('tr')  # 获取表格的所有的行
    for tr in tr_all:
        tr_a = tr.find('a', title='指数走势')
        if tr_a:
            trend_co = tr.find_all('td')[0].text.strip()
            trend_url = tr_a.get('href')
            url_dict.update({trend_co: trend_url})

    return url_dict


def get_trend(trend_route: str) -> list:
    url = 'https://nba.titan007.com%s' % trend_route

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        trend_table = soup.find('span', id='odds2').find('table')

        # 提取表格中的所有行
        trend_all = trend_table.find_all('tr')
        trend_key = [cell.get_text() for cell in trend_all[0].find_all('td')]
        trend_list = []

        for row in trend_all[1:]:
            row_data = {trend_key[k]: cell.get_text() for k, cell in enumerate(row.find_all('td'))}
            trend_list.append(row_data)

        return trend_list


def get_data(game_id: int) -> dict:
    game_data = {"id": game_id, "trend": {}}

    url = 'https://nba.titan007.com/odds/OverDown_n.aspx?id=%d&l=0' % game_id

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        game_data["home_name"] = soup.find('div', class_='home').find('img')['alt']
        game_data["guest_name"] = soup.find('div', class_='guest').find('img')['alt']
        game_data["game_time"] = soup.find('div', class_='vs').find_all('div')[0].text.strip().replace("NBA", "")

        score_table = soup.find('span', id='scoreData').find('table')
        game_data["score_info"] = resolve_score_table(score_table)

        odds_table = soup.find('table', id='odds')
        trend_url_dict = resolve_odds_table(odds_table)
        for co, trend_url in trend_url_dict.items():
            game_data["trend"][co] = get_trend(trend_url)
    else:
        print(f"请求失败，状态码：{response.status_code}")

    return game_data
