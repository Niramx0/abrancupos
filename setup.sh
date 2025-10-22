#!/bin/bash

echo "Iniciando setup del proyecto..."
# - 0. 

# - 1. Levantar Base de datos con docker compose 
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
else
  docker compose up -d
fi

echo "Setup finalizado correctamente..."
