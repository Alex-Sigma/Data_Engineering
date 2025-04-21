from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔐 Фейковый токен (можно использовать любой — главное, чтобы он совпадал с заголовком Authorization)
FAKE_TOKEN = "2b8d97ce57d401abd89f45b0079d8790edd940e6"

# 📦 Фейковые данные
FAKE_SALES = {
    "2022-08-09": [
        {"client": "Kelly Gomez", "purchase_date": "2022-08-09", "product": "coffee machine", "price": 1088},
        {"client": "Daisy Mcfarland", "purchase_date": "2022-08-09", "product": "Laptop", "price": 2767},
        {"client": "Ashley Schneider", "purchase_date": "2022-08-09", "product": "Vacuum cleaner", "price": 690}
    ]
}

@app.route("/sales")
def get_sales():
    # Проверяем токен
    auth_header = request.headers.get("Authorization", "")
    if f"Bearer {FAKE_TOKEN}" != auth_header:
        return jsonify({"message": "Authorization token not set properly. You are not authorised to use this resource"}), 403

    # Получаем дату и страницу
    date = request.args.get("date")
    page = int(request.args.get("page", 1))

    if not date or date not in FAKE_SALES:
        return jsonify([])

    # Возвращаем данные только на первой странице (эмуляция пагинации)
    if page == 1:
        return jsonify(FAKE_SALES[date])
    else:
        return jsonify([])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
