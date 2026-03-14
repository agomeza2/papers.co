import os
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dotenv import load_dotenv 
from tqdm import tqdm 

print("ENGINE STARTING...", flush=True)

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongo:27017/"
ES_URI = "http://elasticsearch:9200"

INDEX_NAME = "documents"
BATCH_SIZE = 500 

def wait_for_mongo():
    while True:
        try:
            client = MongoClient(MONGO_URI)
            client.admin.command("ping")
            print("MongoDB listo")
            return client
        except Exception as e:
            print("Esperando MongoDB...", e)
            time.sleep(3)


def wait_for_elasticsearch():
    es = Elasticsearch(
    ES_URI,
    request_timeout=60 
    )

    while True:
        try:
            health = es.cluster.health(wait_for_status="yellow", timeout="30s")
            if health:
                print("Elasticsearch listo")
                return es
        except Exception as e:
            print("Esperando Elasticsearch...", e)

        time.sleep(5)

def create_index(es):
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print("Indice creado:", INDEX_NAME)
    else:
        print("Indice ya existe")

def transform(doc):
    return {
        "id": doc.get("id"),
        "title": doc.get("title"),
        "year": doc.get("publication_year"),
        "doi": doc.get("doi"),
        "citations": doc.get("cited_by_count"),
        "authors": [
            a.get("author", {}).get("display_name")
            for a in doc.get("authorships", [])
        ],
        "keywords": [
            k.get("display_name")
            for k in doc.get("keywords", [])
        ],
        "concepts": [
            c.get("display_name")
            for c in doc.get("concepts", [])
        ]
    }
def mongo_to_es(mongo, es):
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]
    collection = db['works']
    total = collection.count_documents({})
    cursor = collection.find({}, no_cursor_timeout=True)
    print("Total documentos:",total)
    actions = []

    with tqdm(total=total, desc="Indexando documentos") as pbar:

        for doc in cursor:

            try:
                doc_id = str(doc["_id"])
                clean_doc = transform(doc)

                actions.append({
                    "_index": INDEX_NAME,
                    "_id": doc_id,
                    "_source": clean_doc
                })

                if len(actions) >= BATCH_SIZE:
                    bulk(es, actions)
                    actions.clear()

                pbar.update(1)

            except Exception as e:
                print("Documento falló:", e)

        if actions:
            bulk(es, actions)
def main():
    mongo = wait_for_mongo()
    es = wait_for_elasticsearch()

    create_index(es)
    mongo_to_es(mongo, es)

    print("Indexación completada")


if __name__ == "__main__":
    main()
