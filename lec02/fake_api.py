from flask import Flask, request, jsonify

app = Flask(__name__)

# фейковый токен, который мы проверяем
FAKE_TOKEN = "2b8d97ce57d401abd89f45b0079d8790edd940e6"

# наши фейковые продажи
FAKE_SALES_DATA = [
    {
        "client": "Kelly Gomez",
        "purchase_date": "2022-08-09",
        "product": "coffee machine",
        "price": 1088
    },
    {
        "client": "Daisy Mcfarland",
        "purchase_date": "2022-08-09",
        "product": "Laptop",
        "price": 2767
    },
    {
        "client": "Ashley Schneider",
        "purchase_date": "2022-08-09",
        "product": "Vacuum cleaner",
        "price": 690
    }
]

@app.route("/sales", methods=["GET"])
def sales():
    # Проверка токена
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {FAKE_TOKEN}":
        return jsonify({"message": "Authorization token not set properly. You are not authorised to use this resource"}), 403

    # Получаем дату и страницу
    date = request.args.get("date")
    page = request.args.get("page", "1")

    if date != "2022-08-09":
        return jsonify([])

    if page == "1":
        return jsonify(FAKE_SALES_DATA)
    else:
        return jsonify([])  # только одна страница

if __name__ == "__main__":
    app.run(port=5000)
