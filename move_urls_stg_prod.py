import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
from decouple import config

STG_POSTGRES_HOST = config('STG_POSTGRES_HOST')
PRD_POSTGRES_HOST = config('PRD_POSTGRES_HOST')
STG_DATABASE_NAME = config('STG_DATABASE_NAME')
PRD_DATABASE_NAME = config('PRD_DATABASE_NAME')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASS = config('POSTGRES_PASS')
POSTGRES_PORT = config('POSTGRES_PORT')

stg_pgconn = psycopg2.connect(user=POSTGRES_USER,password=POSTGRES_PASS,
                              host=STG_POSTGRES_HOST,port=POSTGRES_PORT,database=STG_DATABASE_NAME)
stg_pgcursor = stg_pgconn.cursor()
stg_pgconn.autocommit = True

prod_pgconn = psycopg2.connect(user=POSTGRES_USER,password=POSTGRES_PASS,
                               host=PRD_POSTGRES_HOST,port=POSTGRES_PORT,database=PRD_DATABASE_NAME)

prod_pgcursor = prod_pgconn.cursor()
prod_pgconn.autocommit = True

selectall = ''' select * from articles where name is not null and description is not null and devimages is not null and prod_ok is null '''
stg_records = sqlio.read_sql_query(selectall, stg_pgconn)

print ("TOTAL STG RECORDS TO BE MOVED TO PROD :::  {} ::: RECORDS".format(len(stg_records.index)),)
for row, index in stg_records.iterrows():
    print ("MOVING/ MARKING STG URLS TO PROD : {}".format(index["urls"]))
    send_to_prod = ''' insert into articles (urls) values (%s) on conflict do nothing '''
    query_prod_pgcursor = prod_pgcursor.execute(send_to_prod,[index["urls"]])
    
    addattributes = ''' update articles set name =%s, description =%s , devimages =%s where urls =%s '''
    query_prod_pgcursor_attributes = prod_pgcursor.execute(addattributes,[index["name"].encode('ascii', 'ignore').decode('ascii'),index["description"].encode('ascii', 'ignore').decode('ascii'),
                                                                        index["devimages"].encode('ascii', 'ignore').decode('ascii'),index["urls"]])
    mark_prod_ok = ''' update articles set prod_ok=TRUE where urls =%s '''
    query_mark_prod_ok = stg_pgcursor.execute(mark_prod_ok,[index["urls"]])
    print ("PROD RECORDS MOVED : {}".format(index["urls"]))
