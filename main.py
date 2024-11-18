from GetID import get_id
from GetData import get_data
import yaml
import pyodbc


with open("config.yaml", "r", encoding="utf-8") as f:
    _config = yaml.load(f, Loader=yaml.FullLoader)


conn_str = f'DRIVER={{SQL Server}};SERVER={_config["Server"]};DATABASE={_config["Database"]};UID={_config["UID"]};PWD={_config["PWD"]}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

id_list = get_id(2024, 10, "2024-2025")


print("total: %d" % len(id_list))
for i, item in enumerate(id_list):
    print("%d: %s" % (i+1, item))

    _json = get_data(int(item))

    insert_main = '''insert into dbo.NBAInfo (NBAID, rq, xq, sj, zd, kd, z1, z2, z3, z4, zj, k1, k2, k3, k4, kj) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    insert_zf = '''insert into dbo.ZFInfo (NBAID, gs, df, pk, xf, rq, sj) values (?, ?, ?, ?, ?, ?, ?)'''
    insert_rf = '''insert into dbo.RFInfo (NBAID, gs, zp, pk, kp, rq, sj) values (?, ?, ?, ?, ?, ?, ?)'''

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
