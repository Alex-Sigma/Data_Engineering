from flask import Flask, request, jsonify
from json_to_avro import json_to_avro

app = Flask(__name__)

@app.route("/", methods=["POST"])
def run_job():
    data = request.get_json()
    raw_dir = data.get("raw_dir")
    stg_dir = data.get("stg_dir")

    if not raw_dir or not stg_dir:
        return jsonify({"message": "❌ Missing parameters: raw_dir and stg_dir are required"}), 400

    try:
        json_to_avro(raw_dir, stg_dir)
        return jsonify({"message": "✅ Data successfully converted to Avro"}), 201
    except Exception as e:
        return jsonify({"message": f"❌ Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=8082)
