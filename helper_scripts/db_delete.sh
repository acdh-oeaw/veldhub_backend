#!/bin/bash
cd ..
docker compose stop veldhub_db
rm -rf modules/veld_registry/data/*
