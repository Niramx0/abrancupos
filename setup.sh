#!/bin/bash
set -e
echo "Iniciando setup del proyecto..."
# - 0. Cargar variables del entorno(.env)
ENV_FILE="Proyecto/.env"
if [ -f "$ENV_FILE" ]; then
  echo "Cargando variables desde Proyecto/.env"
  set -a
  source "$ENV_FILE"
  set +a
else
  echo "No se encontró el archivo .env. Asegúrate de tenerlo antes de continuar"
  exit 1
fi

# - 1. Levantar Base de datos con docker compose 
cd Proyecto 
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
else
  docker compose up -d
fi
MYSQL_CONTAINER="mysql-dev"

# - 2. Verificar si MySQL esta listo
echo "Esperando a que MySQL acepte conexiones"
until docker exec "$MYSQL_CONTAINER" mysqladmin ping -h "localhost" -p"$MYSQL_ROOT_PASSWORD" --silent; do
  sleep 2
done
echo "MySQL está listo para aceptar conexiones."

# - 3. Estado final de los contenedores
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose ps
else
  docker compose ps
fi
 
cd ..
echo "Setup finalizado correctamente..."
