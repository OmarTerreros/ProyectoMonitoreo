from flask import Flask, request, jsonify
from pymongo import MongoClient
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
client = MongoClient("mongodb://monguito:27017/")
db = client.test

#Metrica personalizada
contador_insert = Counter("insert_total", "Número total de inserts en Mongo")

@app.route("/")
def index():
    return "Bienvenido a tu app Flask + Mongo + Métricas"

@app.route("/add", methods=["POST"])
def add():
    data = request.json
    db.devops.insert_one(data)
    contador_insert.inc()  # incrementa la métrica
    return jsonify({"status": "ok"}), 201

@app.route("/all")
def all():
    docs = list(db.devops.find({}, {"_id": 0}))
    return jsonify(docs)

#Endpoint de Prometheus
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)