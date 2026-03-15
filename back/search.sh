#!/bin/bash

echo "Bienvenido al buscador interactivo. Escribe '/bye' para salir."

while true; do
    # Leer input del usuario
    read -p "Buscar: " texto

    # Salir si el usuario escribe /bye
    if [[ "$texto" == "/bye" ]]; then
        echo "Saliendo..."
        break
    fi

    # Escapar el texto para JSON
    texto_escapado=$(printf '%s' "$texto" | jq -R .)

    # Hacer la consulta a la API Flask
    curl -s -X POST "http://localhost:5000/search" \
         -H "Content-Type: application/json" \
         -d "{\"query\": $texto_escapado}" | jq
done
