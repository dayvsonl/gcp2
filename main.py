from flask import Flask, request, jsonify
from google.cloud import bigquery
import uuid
import datetime

app = Flask(__name__)

# Função para inserir dados no BigQuery
def insert_event_to_bigquery(event_type):
    client = bigquery.Client()
    table_id = "project__id.lab_dataset.events"  # Substitua com seu projeto e dataset
    rows_to_insert = [{
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "event_timestamp": datetime.datetime.now().isoformat()  # Converte datetime para string
    }]
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise RuntimeError(f"Erro ao inserir dados: {errors}")

@app.route("/events", methods=["GET"])  # Alterei para GET, pois o parâmetro está na URL
def event():
    event_type = request.args.get("event_type", "default_event")  # Pega o parâmetro da URL
    try:
        insert_event_to_bigquery(event_type)
        response = {
            "status": "success",
            "timestamp": datetime.datetime.now().isoformat()  # Converte datetime para string
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
