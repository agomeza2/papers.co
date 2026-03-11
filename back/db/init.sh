#!/bin/bash

# Cargar variables del .env
ENV_FILE="/docker-entrypoint-initdb.d/.env"
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo ".env no encontrado en $ENV_FILE"
fi

echo "Esperando a Mongo..."
sleep 5
echo "Restaurando dump..."

mongosh <<EOF
use ${MONGO_DB}
db.createUser({
  user: "${MONGO_USER}",
  pwd: "${MONGO_PASSWORD}",
  roles: [{ role: "readWrite", db: "${MONGO_DB}" }]
})
EOF

mongorestore \
  --username "${MONGO_USER}" \
  --password "${MONGO_PASSWORD}" \
  --db "${MONGO_DB}" \
  /dump/ColombiaResearch

echo "Restauración finalizada"
