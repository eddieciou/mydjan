#!/usr/bin/env bash

# if there is an initial database, load the initial db automatically
# put the backup in db/pgsql_backup
# the backup can be created by running "pg_dump -Fc mydjan_db > pgsql_backup"

DB_NAME=mydjan_db

echo "###";
echo "# Create DB";
echo "###";
createdb -U postgres ${DB_NAME}
