# Data_Engineering

# 📚 Homework: Sales Data Pipeline (lec02)

## ✅ Цель

Создать ETL-конвейер для получения продаж через API, сохранения в JSON (в raw), и преобразования в Avro (в stg).

---

## 🔢 Структура

```bash
lec02/
├── bll/                   # Business logic
│   └── sales_pipeline.py  # Основные функции save_sales_to_local_disk, json_to_avro
│
├── controller/            # Джобы запуска
│   ├── job1_extract.py    # Сохраняет JSON из API в raw
│   └── job2_transform.py  # POST-сервер: преобразует JSON в Avro
│
├── dal/                   # Data access layer
│   ├── avro_saver.py
│   └── json_loader.py
│
├── raw/                  # Результаты job1
│   └── sales/YYYY-MM-DD/sales_YYYY-MM-DD_1.json
│
├── stg/                  # Результаты job2
│   └── sales/YYYY-MM-DD/sales.avro
│
├── fake_api.py           # Локальный фейковый API
├── requirements.txt
└── README.md             # Этот файл
```

---

## 🔧 1. Запуск job1 (извлечь JSON)

### Команда:

```bash
cd ~/Desktop/Data_Engineering
export PYTHONPATH=.
python3 -m lec02.controller.job1_extract
```

### Результат:

- Папка `raw/sales/2022-08-09/`
- Файл: `sales_2022-08-09_1.json`

---

## 🚀 2. Запуск job2 (POST сервер Flask)

### Команда:

```bash
cd ~/Desktop/Data_Engineering
export PYTHONPATH=.
python3 -m lec02.controller.job2_transform
```

### Пример запроса:

```bash
curl -X POST http://localhost:8082 \
  -H "Content-Type: application/json" \
  -d '{"raw_dir": "raw/sales/2022-08-09", "stg_dir": "stg/sales/2022-08-09"}'
```

### Результат:

- Папка `stg/sales/2022-08-09/`
- Файл: `sales.avro`

---

## 📂 Idempotency (идемпотентность)

- job1 очищает `raw_dir` перед сохранением новых JSON.
- job2 очищает `stg_dir` перед записью `.avro`

---

## 📊 Проверка .avro

> _Можно дописать скрипт чтения .avro при необходимости:_

```python
from fastavro import reader
with open("stg/sales/2022-08-09/sales.avro", "rb") as f:
    for record in reader(f):
        print(record)
```

---

## 📁 requirements.txt

```txt
requests
flask
fastavro
dotenv
```

---
