#!/bin/bash

echo "🔁 Остановка предыдущих процессов..."
pkill -f "airflow webserver"
pkill -f "airflow scheduler"
sleep 2

echo "✅ Активация виртуального окружения..."
source venv/bin/activate

# 📥 Загрузка переменных из .env
if [ -f .env ]; then
    echo "📥 Загрузка переменных из .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️ Файл .env не найден. SMTP и окружение могут не работать."
fi

echo "🚀 Запуск webserver на фоне (порт 8080)..."
airflow webserver --port 8080 > /dev/null 2>&1 &
sleep 5

echo "🧠 Запуск scheduler на фоне..."
airflow scheduler > /dev/null 2>&1 &
sleep 5

echo "📋 Проверка DAG'ов..."
airflow dags list | grep iris_pipeline && echo "✅ DAG 'iris_pipeline' загружен!" || echo "❌ DAG 'iris_pipeline' не найден."

echo -e "\n📈 Отображение структуры DAG:"
airflow dags show iris_pipeline || echo "❌ Ошибка при отображении DAG"

echo -e "\n🌐 Теперь ты можешь открыть браузер: http://localhost:8080"
