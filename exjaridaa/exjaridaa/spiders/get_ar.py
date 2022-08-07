import scrapy
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import soupsieve

# READ DATABASE
from sqlalchemy import engine, create_engine

conn = psycopg2.connect(user="sqladmin", password="Cc.09275920",
                        host="192.168.1.73", port="5432", database="jaridaa_dev")
cursor = conn.cursor()
conn.autocommit = True

query = '''SELECT * from articles where lang like 'ar'  and name is null '''

querlist = [query]
for q in querlist:
    cursor.execute(q)
    dat = sqlio.read_sql_query(q, conn)
    links = (dat["urls"].values)
print(querlist)

class MainSpider(scrapy.Spider):
    name = "get_ar"
    start_urls = [l for l in links] 

    def parse(self, response):
        page = response.request.url
        title = response.css('h1::text').extract()
        if len(title):
            query = '''update articles set name =%s  where urls like %s '''
            cursor.execute(query, [str(title), str(page)])
            print("records was inserted: {} ".format(page))

        yield {
                "url": page,
                "title": title
                }