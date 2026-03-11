from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://elasticsearch:9200")

@app.route("/search", methods=["POST"])
def search():

    query = request.json.get("query")

    result = es.search(
        index="_all",
        query={
            "multi_match": {
                "query": query,
                "fields": ["*"]
            }
        }
    )

    return jsonify(result["hits"]["hits"])

@app.route("/")
def home():
    return {"status": "API running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
