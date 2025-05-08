# SQL Homework — Lecture 03

## Student: Oleksii Astakhov  
## Date: 03.05.2025

## Завдання

Метою було:
- Підняти демо-базу Pagila на EC2-інстансі за допомогою Docker Compose;
- Під'єднатися до бази через pgAdmin;
- Написати SQL-запити для виконання аналітичних завдань.

---

## Хід виконання

### 1. Інфраструктура

- За допомогою **Terraform** створено EC2-інстанс у регіоні `eu-north-1` (Stockholm).
- Використано офіційний **AMI Ubuntu 22.04** (`ami-04a5f55f5196f401f`).
- Налаштовано ключ SSH (`dataops-key`) та Security Group (`de-sg`) з дозволом на порти **22, 5432, 5050**.
- Після створення, автоматично було встановлено:
  - Docker
  - Docker Compose

---

### 2. Деплой демо-бази Pagila

- Репозиторій [devrimgunduz/pagila](https://github.com/devrimgunduz/pagila) клоновано на інстанс.
- Створено `.env` файл із налаштуваннями:
  ```env
  POSTGRES_DB=pagila
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=123456
  POSTGRES_PORT=5432
  ```
- Виконано `docker-compose up -d`, після чого база PostgreSQL та pgAdmin були успішно запущені.

---

### 3. Підключення до pgAdmin

- Веб-інтерфейс pgAdmin став доступним за адресою `http://<public_ip>:5050`.
- Авторизація в pgAdmin:
  - Email: `admin@admin.com`
  - Password: `root`
- Додано новий сервер `pagila`, підключено до бази `postgres` з логіном `postgres` та паролем `123456`.

---

### 4. Структура БД

- Було досліджено структуру таблиць: `film`, `category`, `film_category`, `actor`, `film_actor`, `inventory`, `rental`, `payment`.

---

### 5. Виконання SQL-запитів

У файлі `home_task_queries.sql` реалізовано всі п’ять запитів:

1. Кількість фільмів у кожній категорії.
2. Топ-10 акторів, чиї фільми найбільше брали в прокат.
3. Категорія фільмів із найбільшими витратами в прокаті.
4. Назви фільмів, яких немає в inventory (без `IN`).
5. Топ-3 актори за кількістю фільмів у категорії "Children".

---

## Висновки

- Завдання виконано повністю.
- Навички: робота з Terraform, Docker, PostgreSQL, pgAdmin, написання SQL-запитів.
- Отримано цілісне уявлення про деплой демо-баз та аналітику даних на SQL.
