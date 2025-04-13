import os
import requests
import json
import shutil

def save_sales_to_local_disk(date: str, raw_dir: str):
    """
    Сохраняет данные продаж за указанную дату в директорию raw_dir.
    Делает джобу идемпотентной: очищает папку перед сохранением.
    Каждая страница сохраняется в отдельный файл: sales_<date>_1.json и т.д.
    """

    # Чтение токена из окружения или дефолт (для локального теста)
    token = os.getenv("AUTH_TOKEN") or "2b8d97ce57d401abd89f45b0079d8790edd940e6"
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Очистить папку raw_dir (идемпотентность)
    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
    os.makedirs(raw_dir, exist_ok=True)

    print(f"📦 Сохраняем данные продаж за {date} в: {raw_dir}")

    # 2. Цикл по страницам API
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

        # 3. Имя файла: sales_YYYY-MM-DD_<page>.json
        file_name = f"sales_{date}_{page}.json"
        file_path = os.path.join(raw_dir, file_name)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"📁 Сохранено: {file_path}")
        page += 1
