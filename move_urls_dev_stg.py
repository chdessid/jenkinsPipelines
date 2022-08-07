import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

DEV_POSTGRES_HOST = config('DEV_POSTGRES_HOST')
DEV_DATABASE_NAME = config('DEV_DATABASE_NAME')
STG_DATABASE_NAME = config('STG_DATABASE_NAME')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASS = config('POSTGRES_PASS')
POSTGRES_PORT = config('POSTGRES_PORT')

dev_pgconn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES_HOST, port=POSTGRES_PORT, database=DEV_DATABASE_NAME)
dev_pgcursor = dev_pgconn.cursor()
dev_pgconn.autocommit = True

stg_pgconn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES_HOST, port=POSTGRES_PORT, database=STG_DATABASE_NAME)
stg_pgcursor = stg_pgconn.cursor()
stg_pgconn.autocommit = True

selectall = ''' select * from articles where name is not null and description is not null and devimages is not null and stg_ok is null '''
dev_records = sqlio.read_sql_query(selectall, dev_pgconn)
print ("TOTAL DEV RECORDS TO BE MOVED TO STG :::  {} ::: RECORDS".format(len(dev_records.index)),)
for row, index in dev_records.iterrows():
    print ("MOVING/ MARKING DEV URLS TO STG : {}".format(index["urls"]))
    send_to_stg = ''' insert into articles (urls) values (%s) on conflict do nothing '''
    query_stg_pgcursor = stg_pgcursor.execute(send_to_stg,[index["urls"]])
    
    addattributes = ''' update articles set name =%s, description =%s , devimages =%s where urls =%s '''
    query_stg_pgcursor_attributes = stg_pgcursor.execute(addattributes,[index["name"],index["description"],
                                                                        index["devimages"],index["urls"]])
    mark_stg_ok = ''' update articles set stg_ok=TRUE where urls =%s '''
    query_mark_stg_ok = dev_pgcursor.execute(mark_stg_ok,[index["urls"]])
    print ("STG RECORDS MOVED : {}".format(index["urls"]))
