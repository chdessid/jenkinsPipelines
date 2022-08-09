import psycopg2
import pandas as pd
import pandas.io.sql as sqlio
from decouple import config
import math
LIMIT_SELECT = 1000

DEV_POSTGRES_HOST = config('DEV_POSTGRES_HOST')
DEV_DATABASE_NAME = config('DEV_DATABASE_NAME')
STG_DATABASE_NAME = config('STG_DATABASE_NAME')
BCP_DATABASE_NAME = config('BCP_DATABASE_NAME')

POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASS = config('POSTGRES_PASS')
POSTGRES_PORT = config('POSTGRES_PORT')


stg_pgconn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES_HOST, port=POSTGRES_PORT, database=STG_DATABASE_NAME)
stg_pgcursor = stg_pgconn.cursor()
stg_pgconn.autocommit = True

bcp_pgconn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES_HOST, port=POSTGRES_PORT, database=BCP_DATABASE_NAME)
bcp_pgcursor = bcp_pgconn.cursor()
bcp_pgconn.autocommit = True

_countrecords = sqlio.read_sql_query(''' select count (*) from articles''', stg_pgconn)
countrecords = (_countrecords["count"].values)[0]
iteration = int(math.modf((countrecords/LIMIT_SELECT))[1])
for i in range(1,(iteration)) :
    selectall = ''' select * from articles limit {}'''.format(LIMIT_SELECT)
    stg_records = sqlio.read_sql_query(selectall, stg_pgconn)
    for row, index in stg_records.iterrows():
        print ("MOVING/ MARKING STG URLS TO BCP : {}".format(index["urls"]))
        send_to_bcp = ''' insert into articles (urls) values (%s) on conflict do nothing '''
        query_stg_pgcursor = bcp_pgcursor.execute(send_to_bcp,[index["urls"]])
        
        addattributes = ''' update articles set name =%s, description =%s , devimages =%s where urls =%s '''
        query_bcp_pgcursor_attributes = bcp_pgcursor.execute(addattributes,[index["name"],index["description"],
                                                                            index["devimages"],index["urls"]])
        
        mark_stg_ok = ''' update articles set bcp_ok=TRUE where urls =%s '''
        query_mark_stg_ok = stg_pgcursor.execute(mark_stg_ok,[index["urls"]])
        print ("BCP RECORDS OK : {}".format(index["urls"]))
