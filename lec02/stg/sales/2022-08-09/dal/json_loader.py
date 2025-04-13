import os
import json

def load_json_files_from_dir(raw_dir: str) -> list:
    """
    Загружает все JSON-файлы из raw_dir и возвращает список всех записей.
    """
    all_records = []

    for filename in sorted(os.listdir(raw_dir)):
        if filename.endswith(".json"):
            full_path = os.path.join(raw_dir, filename)
            with open(full_path, "r") as f:
                records = json.load(f)
                all_records.extend(records)

    return all_records
