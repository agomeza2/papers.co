import os
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017"

BATCH_SIZE = 2000

print("Esperando servicios...")
time.sleep(10)

print("Conectando a MongoDB...")
mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB]

print("Conectando a Elasticsearch...")
es = Elasticsearch("http://elasticsearch:9200")

collections = db.list_collection_names()

print("Colecciones encontradas:", collections)


def generate_actions(collection):

    cursor = db[collection].find({}, no_cursor_timeout=True)

    for doc in cursor:

        doc_id = str(doc["_id"])
        doc["_id"] = doc_id

        yield {
            "_index": collection,
            "_id": doc_id,
            "_source": doc
        }


for col in collections:

    print(f"Indexando colección: {col}")

    helpers.bulk(
        es,
        generate_actions(col),
        chunk_size=BATCH_SIZE,
        request_timeout=120
    )

    print(f"Colección {col} indexada")

print("Indexación completa")
