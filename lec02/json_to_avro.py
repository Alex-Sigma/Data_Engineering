import os
import json
import shutil
from fastavro import writer, parse_schema

def json_to_avro(raw_dir: str, stg_dir: str):
    """
    Читает JSON-файлы из raw_dir и сохраняет в Avro-формате в stg_dir.
    """
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"❌ raw_dir не существует: {raw_dir}")

    # Очистка stg_dir (идемпотентность)
    if os.path.exists(stg_dir):
        shutil.rmtree(stg_dir)
    os.makedirs(stg_dir, exist_ok=True)

    for filename in os.listdir(raw_dir):
        if filename.endswith(".json"):
            with open(os.path.join(raw_dir, filename), "r") as f:
                records = json.load(f)

            if not records:
                continue

            # Автоматически построим схему из первой записи
            example = records[0]
            schema = {
                "doc": "Sales records",
                "name": "Sale",
                "namespace": "sales.avro",
                "type": "record",
                "fields": [{"name": key, "type": ["null", "string", "int"]} for key in example]
            }
            parsed_schema = parse_schema(schema)

            avro_filename = filename.replace(".json", ".avro")
            avro_path = os.path.join(stg_dir, avro_filename)

            with open(avro_path, "wb") as out:
                writer(out, parsed_schema, records)

            print(f"✅ Avro saved: {avro_path}")
