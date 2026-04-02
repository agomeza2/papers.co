from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
CORS(app)  # 🔥 habilita conexión con el frontend

# Config
ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
INDEX_NAME = "documents"

es = Elasticsearch(ES_HOST)

# =========================
# 🔍 SEARCH
# =========================
@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "title^3",
                    "authors",
                    "keywords",
                    "concepts"
                ],
                "type": "best_fields"
            }
        },
        "size": 50
    }

    response = es.search(index=INDEX_NAME, body=es_query)

    results = []
    for hit in response["hits"]["hits"]:
        results.append(hit["_source"])

    return jsonify(results)


# =========================
# 📄 DOCUMENTO POR ID
# =========================
@app.route("/document/<doc_id>", methods=["GET"])
def get_document(doc_id):
    try:
        response = es.get(index=INDEX_NAME, id=doc_id)
        return jsonify(response["_source"])
    except:
        return jsonify({"error": "Document not found"}), 404


# =========================
# 👤 AUTORES
# =========================
@app.route("/authors", methods=["GET"])
def get_authors():
    es_query = {
        "size": 0,
        "aggs": {
            "authors": {
                "terms": {
                    "field": "authors.keyword",
                    "size": 20
                }
            }
        }
    }

    response = es.search(index=INDEX_NAME, body=es_query)

    authors = [
        bucket["key"]
        for bucket in response["aggregations"]["authors"]["buckets"]
    ]

    return jsonify(authors)


# =========================
# 🏷️ KEYWORDS
# =========================
@app.route("/keywords", methods=["GET"])
def get_keywords():
    es_query = {
        "size": 0,
        "aggs": {
            "keywords": {
                "terms": {
                    "field": "keywords.keyword",
                    "size": 20
                }
            }
        }
    }

    response = es.search(index=INDEX_NAME, body=es_query)

    keywords = [
        bucket["key"]
        for bucket in response["aggregations"]["keywords"]["buckets"]
    ]

    return jsonify(keywords)


# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    return jsonify({"status": "API running 🚀"})


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
