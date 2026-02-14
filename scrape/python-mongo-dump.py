import requests
import time
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ColombiaResearch"
COLLECTION_NAME = "works"
META_COLLECTION = "metadata"
MAILTO = "agomeza2@academia.usbbog.edu.co"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COLLECTION_NAME]
meta = db[META_COLLECTION]

# Índices
col.create_index("id", unique=True)

# Recuperar cursor guardado
cursor_doc = meta.find_one({"_id": "openalex_cursor"})
cursor = cursor_doc["value"] if cursor_doc else "*"

base_url = "https://api.openalex.org/works"

while cursor:
    response = requests.get(
        base_url,
        params={
            "filter": "institutions.country_code:CO",
            "per-page": 200,
            "cursor": cursor,
            "mailto": MAILTO
        }
    )

    if response.status_code == 429:
        time.sleep(10)
        continue

    data = response.json()

    for work in data["results"]:
        col.update_one(
            {"id": work["id"]},
            {"$set": work},
            upsert=True
        )

    cursor = data["meta"]["next_cursor"]

    # Guardar cursor actual en Mongo
    meta.update_one(
        {"_id": "openalex_cursor"},
        {"$set": {"value": cursor}},
        upsert=True
    )

    print("Cursor guardado:", cursor)
    time.sleep(0.3)

print("Descarga completa.")
