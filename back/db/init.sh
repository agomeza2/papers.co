#!/bin/bash

echo "Esperando a Mongo..."
sleep 5

echo "Restaurando dump..."

mongorestore \
  --username "$MONGO_INITDB_ROOT_USERNAME" \
  --password "$MONGO_INITDB_ROOT_PASSWORD" \
  --db "$MONGO_INITDB_DATABASE" \
  /dump/ColombiaResearch

echo "Restauración finalizada"
