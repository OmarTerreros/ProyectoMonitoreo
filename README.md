# Proyecto: Flask + Mongo + Prometheus + Grafana en Docker

## Estructura del proyecto:

```bash
flask-monitoring-stack/
├── flask/
│   ├── app.py
│   └── requerimientos.txt
├── prometheus.yml
├── docker-compose.yml
├── README.md
```

---

## flask/requirements.txt

```
flask
pymongo
prometheus_client
```

---

## flask/app.py

```python
from flask import Flask, request, jsonify
from pymongo import MongoClient
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
client = MongoClient("mongodb://monguito:27017/")
db = client.test

# Métrica personalizada
contador_insert = Counter("insert_total", "Número total de inserts en Mongo")

@app.route("/")
def index():
    return "Bienvenido a tu app Flask + Mongo + Métricas"

@app.route("/add", methods=["POST"])
def add():
    data = request.json
    db.devops.insert_one(data)
    contador_insert.inc()
    return jsonify({"status": "ok"}), 201

@app.route("/all")
def all():
    docs = list(db.devops.find({}, {"_id": 0}))
    return jsonify(docs)

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## prometheus.yml

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['web:5000']
```

---

## docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: ./flask
    ports:
      - "5000:5000"
    depends_on:
      - monguito

  monguito:
    image: mongo:4
    ports:
      - "27017:27017"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

---

## README.md (resumen del proyecto)

```markdown
# Flask + Mongo + Prometheus + Grafana (Docker)

Este proyecto es un stack de monitoreo completo con:

- Flask: backend con endpoints y métricas personalizadas
- MongoDB: base de datos
- Prometheus: monitoreo de métricas
- Grafana: visualización de métricas
- Docker Compose: orquestación de contenedores

## ¿Cómo usar?

1. Clona el repo:
```bash
git clone https://github.com/tu_usuario/Monitoreoflask.git
cd flask-monitoring-stack
```

2. Levanta el entorno:
```bash
docker-compose up -d --build
```

3. Accede a:
- App Flask: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Usuario: `admin`, Contraseña: `admin`

4. Realiza un insert:
```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Omar", "rol":"DevOps"}'
```

5. Mira el dashboard en Grafana con la métrica `insert_total`
```

---
