import os
import time
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "http://elasticsearch:9200")
INDEX_NAME = "documents"

app = Flask(__name__)

def wait_for_elasticsearch():
    while True:
        try:
            es = Elasticsearch(ES_HOST)
            if es.ping():
                print("Elasticsearch listo")
                return es
        except Exception as e:
            print("Esperando Elasticsearch...", e)
        time.sleep(3)

es = wait_for_elasticsearch()


@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")

    if not query:
        return {"error": "No query provided"}, 400

    es_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "title",
                    "raw_author_name",
                    "keywords.display_name",
                    "concepts.display_name",
                    "raw_affiliation_strings"
                ]
            }
        },
        "size": 50
    }

    response = es.search(index=INDEX_NAME, body=es_query)

    results = []
    for hit in response["hits"]["hits"]:
        doc = hit["_source"]
        results.append(doc)

    return jsonify(results)


@app.route("/")
def home():
    return {"status": "API running with Elasticsearch"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
