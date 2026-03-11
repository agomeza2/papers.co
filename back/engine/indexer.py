#!/usr/bin/env python3
from pymongo import MongoClient, TEXT
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASSWORD")
MONGO_DB   = os.getenv("MONGO_DB")
MONGO_COLLECTION = "works"  # tu colección

# Conexión a Mongo
uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/{MONGO_DB}"
client = MongoClient(uri)
db = client.get_database()
collection = db.get_collection(MONGO_COLLECTION)

# Crear un índice de texto en todos los campos que quieras buscar

# Evitar duplicados: si ya existe, Mongo ignora la creación
existing_indexes = collection.index_information()
if "text_index" not in existing_indexes:
    print("Creando índice de texto en la colección...")
    collection.create_index(
        [
            ("title", "text"),
            ("raw_author_name", "text"),
            ("keywords.display_name", "text"),
            ("concepts.display_name", "text")
        ],
        default_language="spanish",  # safe for mixed/unsupported languages
        name="text_index"
    )
    print("Índice creado.")
else:
    print("El índice de texto ya existe.")

# Imprimir número de documentos (opcional)
count = collection.count_documents({})
print(f"Documentos en la colección '{MONGO_COLLECTION}': {count}")
