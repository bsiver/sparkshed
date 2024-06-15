#!/bin/bash

username="root"
host="${SPARKSHED_DB_HOST}"
database_name="${SPARKSHED_DB_NAME}"
password="${SPARKSHED_DB_PASSWORD}"

output_file="output.sql"

export PGPASSWORD="$password"

pg_dump -U "$username" -h "$host" -d "$database_name" -Fc -f "$output_file"

echo "Schema and data dumped to $output_file"
