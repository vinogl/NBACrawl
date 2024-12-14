from datetime import datetime
from .GetSoup import get_soup


def get_trend(trend_route: str, game_time: datetime, game_id: int, co: str) -> list:
    url = 'https://nba.titan007.com%s' % trend_route
    soup = get_soup(url)

    trend_table = soup.find('span', id='odds2').find('table')
    trend_all = trend_table.find_all('tr')  # 提取表格中的所有行

    # 取出表格的第一行日期作为基准日期，表格中的所有日期均不大于第一行的日期
    row_base_time = datetime.strptime("%d-%s" % (game_time.year, trend_all[1].find_all('td')[-1].get_text().replace("(走地)", "").strip()), "%Y-%m-%d %H:%M")

    trend_list = []
    for row in trend_all[1:]:
        row_data = [cell.get_text() for cell in row.find_all('td')]

        # 补全日期年份
        row_time = datetime.strptime("%d-%s" % (game_time.year, row_data[-1].replace("(走地)", "").strip()), "%Y-%m-%d %H:%M")
        if row_time > row_base_time or row_time.month > game_time.month:
            # 日期若大于第一行或者日期月份比比赛时间月份大，则说明这个日期应该是前一年的日期
            row_time = row_time.replace(year=game_time.year - 1)

        if row_time < game_time:
            row_data.pop()
            row_data.insert(0, row_time.strftime("%H:%M"))
            row_data.insert(0, row_time.strftime("%Y-%m-%d"))
            row_data.insert(0, co)
            row_data.insert(0, game_id)
            trend_list.append(row_data)

    return trend_list
