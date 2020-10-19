#!/bin/sh
if [ ${AUTO_MIGRATE:-0} -eq 1 ]; then
    echo "migrating"
    python manage.py migrate --noinput
fi
if [ ${AUTO_COLLECTSTATIC:-0} -eq 1 ]; then
    python manage.py collectstatic --noinput
fi

exec "$@"
