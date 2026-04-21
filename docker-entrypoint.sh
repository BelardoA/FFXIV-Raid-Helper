#!/bin/sh
set -e
cd /app/backend
python manage.py migrate --noinput
python manage.py seed_mechanics

gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3 &
gunicorn_pid=$!

# If gunicorn dies, take the whole container down so the platform can restart it.
( wait "$gunicorn_pid"; echo "gunicorn exited with $?, terminating container" >&2; kill -TERM 1 ) &

cd /app/frontend
exec ./node_modules/.bin/next start -H 0.0.0.0 -p 3000
