from GetID import get_id
from GetData import get_data
import json


json_save = {}
id_list = get_id(2024, 10, "2024-2025")

print("total: %d" % len(id_list))
for i, item in enumerate(id_list):
    print("%d: %s" % (i+1, item))
    data_json = get_data(int(item))
    json_save.update({data_json["id"]: data_json})

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(json_save, f, ensure_ascii=False, indent=2)
