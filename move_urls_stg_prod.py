import psycopg2
import pandas as pd
import pandas.io.sql as sqlio




stg_pgconn = psycopg2.connect(user="sqladmin",password="Cc.09275920",host="192.168.1.73",port="5432",database="jaridaa_stg")
stg_pgcursor = stg_pgconn.cursor()
stg_pgconn.autocommit = True

prod_pgconn = psycopg2.connect(user="sqladmin",password="Cc.09275920",host="93.188.165.190",port="5432",database="productionstrapi")
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
