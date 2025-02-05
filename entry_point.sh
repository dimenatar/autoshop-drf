#!/bin/sh

counter=0
while ! nc -z "$DB_HOST" "$DB_PORT" && [ $counter -lt 100 ]; do
  sleep 0.1
  counter=$((counter + 1))
done

exec "$@"