from NBAcn import get_id, get_data
import yaml
import pyodbc


with open("config.yaml", "r", encoding="utf-8") as f:
    _config = yaml.load(f, Loader=yaml.FullLoader)

# 根据日期获取比赛id列表
id_dict = get_id(_config["Start"], _config["End"])

# 连接数据库
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER={%s};DATABASE={%s};UID={%s};PWD={%s}' % (_config["Server"], _config["Database"], _config["UID"], _config["PWD"])
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 循环爬取每场比赛数据存入数据库
for game_date, id_list in id_dict.items():
    print("%s total %d games" % (game_date, len(id_list)))
    for i, game_id in enumerate(id_list):
        print("%d: %s" % (i+1, game_id))
        _data = get_data(game_id, game_date)

        insert_zf = '''
        insert into dbo.NBAStatistics (
        GameID, GameDate, TeamName, ZK, 
        score, rebounds, assists, steals, blocks,
        field_goals_made, field_goals_attempted,
        three_points_made, three_points_attempted,
        free_throws_made, free_throws_attempted,
        offensive_rebounds, defensive_rebounds,
        turnovers, personal_fouls
        ) 
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        try:
            cursor.executemany(insert_zf, _data)
            conn.commit()
            print("数据插入成功")
        except Exception as error:
            conn.rollback()
            print("数据插入失败：", error)
