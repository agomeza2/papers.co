from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASSWORD")
MONGO_DB   = os.getenv("MONGO_DB")
MONGO_COLLECTION = "works"

uri = "mongodb://"+MONGO_USER+":"+MONGO_PASS+"@mongo:27017/"+MONGO_DB
client = MongoClient(uri)
db = client.get_database()
collection = db.get_collection(MONGO_COLLECTION)

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query")
    if not query:
        return {"error": "No query provided"}, 400

    # Regex search on multiple fields (case-insensitive)
    search_filter = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"raw_author_name": {"$regex": query, "$options": "i"}},
            {"keywords.display_name": {"$regex": query, "$options": "i"}},
            {"concepts.display_name": {"$regex": query, "$options": "i"}},
            {"raw_affiliation_strings": {"$regex": query, "$options": "i"}}
        ]
    }

    results = list(collection.find(search_filter).limit(50))

    # Convert ObjectId to string
    for r in results:
        r["_id"] = str(r["_id"])

    return jsonify(results)

@app.route("/")
def home():
    return {"status": "API running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
