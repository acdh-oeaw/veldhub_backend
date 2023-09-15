#!/bin/bash
source ./envvars.sh
cd ..
docker compose run veldhub_backend_with_db psql "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_DATABASE}"
