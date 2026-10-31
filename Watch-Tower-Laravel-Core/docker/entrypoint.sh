#!/bin/sh
set -e

if [ -z "$APP_KEY" ]; then
  APP_KEY="base64:$(php -r 'echo base64_encode(random_bytes(32));')"
  export APP_KEY
  echo "entrypoint: generated an APP_KEY for this container (set APP_KEY to keep it stable)"
fi

php artisan config:clear >/dev/null 2>&1 || true

attempt=1
until php artisan migrate --force; do
  if [ "$attempt" -ge 20 ]; then
    echo "entrypoint: migrations still failing after $attempt attempts, giving up" >&2
    exit 1
  fi
  attempt=$((attempt + 1))
  echo "entrypoint: waiting for MongoDB (attempt $attempt)..."
  sleep 3
done

exec "$@"
