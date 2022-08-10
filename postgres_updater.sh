#!/bin/bash
echo '///////////////// BULK POSTGRES UPDATE /////////////'
echo '/////                  JARIDAA_STG              ////'

export PGPASSWORD='Cc.09275920'

while read p; do
  echo "$p"
  psql -h '192.168.1.76' -U 'sqladmin' -d 'jaridaa_stg' \
     -c "$p"
done <postgres_statements.sql

echo '///////////////// COMPLETED :: BULK POSTGRES UPDATE /////////////'



