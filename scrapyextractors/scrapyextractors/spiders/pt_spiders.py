from asyncio import constants
import scrapy
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import soupsieve

from sqlalchemy import engine, create_engine
from decouple import config

DEV_POSTGRES_HOST = config('DEV_POSTGRES_HOST')
DEV_DATABASE_NAME = config('DEV_DATABASE_NAME')
POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_PASS = config('POSTGRES_PASS')
POSTGRES_PORT = config('POSTGRES_PORT')

conn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES_HOST, port=POSTGRES_PORT, database=DEV_DATABASE_NAME)
cursor = conn.cursor()
conn.autocommit = True

query = ''' SELECT * from articles where lang like 'pt' and name is null and urls like '%%observador%%' '''

querlist = [query]
for q in querlist:
    cursor.execute(q)
    dat = sqlio.read_sql_query(q, conn)
    links = (dat["urls"].values)
print(querlist)

class MainSpider(scrapy.Spider):
    name = "pt_spiders"
    start_urls = [l for l in links] 

    def parse(self, response):
        try : 
            urlsite = response.request.url
        except Exception as e :
            print(e)
            pass

        if "observador" in urlsite :
            title = response.css('header > div.article-head-content-headline > h1').extract()
            description = response.css("div.article-body-wrapper > div > div > div.fbg-col-4.fbg-col-lg-2.center-column > div").extract()
            devimages = response.css("header > figure > picture > img").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
            
