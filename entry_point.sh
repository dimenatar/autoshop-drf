#!/bin/sh

counter=0

echo "DB_HOST:: $POSTGRES_HOST; DB_PORT:: $POSTGRES_PORT"

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" && [ $counter -lt 20 ]; do
  sleep 1
  echo "Waiting for postgres $counter"
  counter=$((counter + 1))
done

exec "$@"