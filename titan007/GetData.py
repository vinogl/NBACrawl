from datetime import datetime
from .GetSoup import get_soup
from .GetTrend import get_trend


def resolve_score_table(soup_table) -> list:
    t_all = soup_table.find('tbody').find_all('tr')  # 获取表格的所有的行

    headers = [th.text for th in t_all[0] if th.text not in ['\n', '完']]  # 获取表头
    c_quarter = [i for i, header in enumerate(headers) if '节' in header]  # 每节得分列
    c_ot = [i for i, header in enumerate(headers) if "'OT" in header]  # 加时赛列

    # 获取主队和客队的得分数据
    home_scores = [int(cell.text) for cell in t_all[1].find_all('td')]
    guest_scores = [int(cell.text) for cell in t_all[2].find_all('td')]

    # 提取每节得分
    home_quarter = [home_scores[index] for index in c_quarter]
    guest_quarter = [guest_scores[index] for index in c_quarter]

    # 提取加时赛得分
    home_ot = sum(home_scores[i] for i in c_ot)
    guest_ot = sum(guest_scores[i] for i in c_ot)

    return [*home_quarter, home_ot, *guest_quarter, guest_ot]


def resolve_odds_table(soup_table) -> dict:
    url_dict = {}
    tr_all = soup_table.find_all('tr')  # 获取表格的所有的行
    for tr in tr_all:
        tr_a = tr.find('a', title='指数走势')
        if tr_a:
            trend_co = tr.find_all('td')[0].text.strip()
            if trend_co:
                trend_index = tr_a.get('href').split('?')[1]
                temp_dict = {"ZF": "/odds/OverDownChart.aspx?%s" % trend_index, "RF": "/odds/handicap.aspx?%s" % trend_index}
                url_dict[trend_co] = temp_dict

    return url_dict


def get_data(game_id: int) -> dict:
    url = 'https://nba.titan007.com/odds/OverDown_n.aspx?id=%d&l=0' % game_id
    soup = get_soup(url)

    _home = soup.find('div', class_='home').find('img')['alt']
    _guest = soup.find('div', class_='guest').find('img')['alt']

    time_info = soup.find('div', class_='vs').find_all('div')[0].text.strip().split()
    _date = time_info[1]
    _time = time_info[2]
    _weekday = time_info[3]

    score_table = soup.find('span', id='scoreData').find('table')
    _score_list = resolve_score_table(score_table)

    odds_table = soup.find('table', id='odds')
    trend_url_dict = resolve_odds_table(odds_table)
    zf_trend = []
    rf_trend = []
    game_time = datetime.strptime("%s %s" % (_date, _time), "%Y-%m-%d %H:%M")
    for co, trend_url in trend_url_dict.items():
        zf_trend.extend(get_trend(trend_url["ZF"], game_time, game_id, co))
        rf_trend.extend(get_trend(trend_url["RF"], game_time, game_id, co))

    game_dict = {
        "NBAInfo": [game_id, _date, _weekday, _time, _home, _guest, *_score_list],
        "ZFInfo": zf_trend,
        "RFInfo": rf_trend
    }

    return game_dict
