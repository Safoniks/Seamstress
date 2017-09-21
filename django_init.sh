#!/bin/sh
# wait-for-postgres.sh

set -e

host=${POSTGRESQL_DB}
user=${POSTGRES_USER}
password=${POSTGRES_PASSWORD}

until PGPASSWORD="$password" psql -h "$host" -U "$user" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
mkdir -p /app/media/product-photos /app/logs/nginx /app/logs/uwsgi
make -C /app/docs/ html
python /app/src/manage.py collectstatic --noinput
python /app/src/manage.py migrate
uwsgi --ini /app/uwsgi.ini
exec "$@"
