import os
import shutil
from fastavro import writer, parse_schema

def save_records_to_avro(records: list, stg_dir: str, file_name: str = "sales.avro"):
    """
    Сохраняет записи в один Avro-файл.
    """
    if not records:
        raise ValueError("❌ No records to save.")

    if os.path.exists(stg_dir):
        shutil.rmtree(stg_dir)
    os.makedirs(stg_dir, exist_ok=True)

    schema = {
        "doc": "Sales records",
        "name": "Sale",
        "namespace": "sales.avro",
        "type": "record",
        "fields": [{"name": key, "type": ["null", "string", "int"]} for key in records[0]]
    }

    parsed_schema = parse_schema(schema)
    full_path = os.path.join(stg_dir, file_name)

    with open(full_path, "wb") as out:
        writer(out, parsed_schema, records)

    print(f"✅ Avro saved: {full_path}")
