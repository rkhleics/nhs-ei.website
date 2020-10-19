#!/bin/sh
if [ ${AUTO_MIGRATE:-0} -eq 1 ]; then
    echo "migrating"
    python manage.py migrate --noinput
fi

exec "$@"
