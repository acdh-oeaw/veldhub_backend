#!/bin/bash
source ./db_creds.sh
psql "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB=}"
