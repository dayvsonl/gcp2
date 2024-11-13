from flask import Flask, request, jsonify
from google.cloud import bigquery
import uuid
import datetime

app = Flask(__name__)

# Função para inserir dados no BigQuery
def insert_event_to_bigquery(event_type):
    client = bigquery.Client()
    table_id = "useful-song-441516-t4.lab_dataset.events"  # Substitua com seu projeto e dataset
    rows_to_insert = [{
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "event_timestamp": datetime.datetime.now()
    }]
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise RuntimeError(f"Erro ao inserir dados: {errors}")

@app.route("/event", methods=["POST"])
def event():
    data = request.get_json()
    event_type = data.get("event_type", "default_event")
    try:
        insert_event_to_bigquery(event_type)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
