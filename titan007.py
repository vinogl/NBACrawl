from titan007 import get_id, get_data
import yaml
import pyodbc


with open("config.yaml", "r", encoding="utf-8") as f:
    _config = yaml.load(f, Loader=yaml.FullLoader)

# 根据日期筛选比赛id列表
id_dict = get_id(_config['year'], _config['month'], _config['season'])
if isinstance(_config['date'], list):
    id_list = [key for key, val in id_dict.items() if val in _config['date']]
elif _config['date'] == 'all':
    id_list = list(id_dict.keys())
else:
    id_list = []

# 连接数据库
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER={%s};DATABASE={%s};UID={%s};PWD={%s}' % (_config["Server"], _config["Database"], _config["UID"], _config["PWD"])
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# 循环爬取每场比赛数据存入数据库
print("total: %d" % len(id_list))
for i, item in enumerate(id_list):
    print("%d: %s (%d-%d-%d)" % (i+1, item, _config['year'], _config['month'], id_dict[item]))
    _json = get_data(int(item))

    insert_main = '''insert into dbo.NBAInfo (NBAID, rq, xq, sj, zd, kd, z1, z2, z3, z4, zj, k1, k2, k3, k4, kj) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    insert_zf = '''insert into dbo.ZFInfo (NBAID, gs, rq, sj, df, pk, xf) values (?, ?, ?, ?, ?, ?, ?)'''
    insert_rf = '''insert into dbo.RFInfo (NBAID, gs, rq, sj, zp, pk, kp) values (?, ?, ?, ?, ?, ?, ?)'''

    try:
        cursor.execute(insert_main, _json["NBAInfo"])
        cursor.executemany(insert_zf, _json["ZFInfo"])
        cursor.executemany(insert_rf, _json["RFInfo"])
        conn.commit()
        print("数据插入成功")
    except Exception as error:
        conn.rollback()
        print("数据插入失败：", error)

cursor.close()
conn.close()
