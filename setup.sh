#!/bin/bash

echo "Iniciando setup del proyecto..."
# - 0. Cargar variables del entorno(.env)
ENV_FILE="Proyecto/.env"
if [ -f "$ENV_FILE" ]; then
  echo "Cargando variables desde Proyecto/.env..."
  set -a
  source "$ENV_FILE"
  set +a
else
  echo "No se encontró el archivo .env. Asegúrate de tenerlo antes de continuar"
  exit 1
fi

# - 1. Levantar Base de datos con docker compose 
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
else
  docker compose up -d
fi

echo "Setup finalizado correctamente..."
