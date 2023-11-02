#!/bin/sh
set -e

echo "Waiting for database..."
  wait-for vietis_chatbot_mysql:3306 -t 60 -- echo "Done"

echo "Applying migrations..."
python /src/manage.py makemigrations
python /src/manage.py migrate

exec "$@"
