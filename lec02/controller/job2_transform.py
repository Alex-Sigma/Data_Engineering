from flask import Flask, request, jsonify
from lec02.bll.sales_pipeline import json_to_avro



app = Flask(__name__)

@app.route("/", methods=["POST"])
def run_avro_job():
    data = request.get_json()
    raw_dir = data.get("raw_dir")
    stg_dir = data.get("stg_dir")

    if not raw_dir or not stg_dir:
        return jsonify({"message": "❌ Missing parameters"}), 400

    try:
        json_to_avro(raw_dir=raw_dir, stg_dir=stg_dir)
        return jsonify({"message": "✅ Converted to Avro"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8082)
