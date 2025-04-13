import sys
import os
import requests
import json
import shutil



from lec02.dal.json_loader import load_json_files_from_dir
from lec02.dal.avro_saver import save_records_to_avro


def save_sales_to_local_disk(date: str, raw_dir: str):
    """
    Сохраняет данные продаж за указанную дату в директорию raw_dir.
    Делает джобу идемпотентной: очищает папку перед сохранением.
    Каждая страница сохраняется в отдельный файл: sales_<date>_1.json и т.д.
    """
    token = os.getenv("AUTH_TOKEN") or "2b8d97ce57d401abd89f45b0079d8790edd940e6"
    headers = {"Authorization": f"Bearer {token}"}

    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
    os.makedirs(raw_dir, exist_ok=True)

    print(f"📦 Сохраняем данные продаж за {date} в: {raw_dir}")

    page = 1
    while True:
        url = f"http://127.0.0.1:5000/sales?date={date}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Ошибка запроса: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        if not data:
            print("✅ Нет новых данных — конец пагинации.")
            break

        file_name = f"sales_{date}_{page}.json"
        file_path = os.path.join(raw_dir, file_name)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"📁 Сохранено: {file_path}")
        page += 1


def json_to_avro(raw_dir: str, stg_dir: str):
    """
    Загружает JSON из raw_dir и сохраняет в Avro в stg_dir.
    """
    records = load_json_files_from_dir(raw_dir)
    save_records_to_avro(records, stg_dir)
