import requests
import time


def get_id(start_date: str, end_date: str) -> dict:
    url = "https://api.nba.cn/sib/v2/game/schedule"

    params = {
        "app_key": "tiKB2tNdncnZFPOi",
        "app_version": "1.1.0",
        "channel": "NBA",
        "device_id": "b541f059b3c3aba34de8ccebef3ecdfd",
        "install_id": "2678915310",
        "network": "N/A",
        "os_type": 3,
        "os_version": "1.0.0",
        "sign": "sign_v2",
        "sign2": "A52C19211F1207B974456E8C9CEEFE5A64D9FBF69D39F3D84ADF0E0F4AA5224D",
        "start": start_date,
        "end": end_date,
        "t": int(time.time())
    }

    response = requests.get(url, params=params)
    groups = response.json()["data"]["groups"]

    id_dict = {}
    for group in groups:
        id_dict[group["date"]] = [item["gameId"] for item in group["games"] if item["seasonName"] == "常规赛"]

    return id_dict
