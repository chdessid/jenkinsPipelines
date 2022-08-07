from utils import * 
import scrapy
import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import soupsieve

from sqlalchemy import engine, create_engine

conn = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASS,
                        host=DEV_POSTGRES, port=POSTGRES_PORT, database=DEV_POSTGRES)
cursor = conn.cursor()
conn.autocommit = True

query = '''SELECT * from articles where lang like 'ar' and name is null '''

querlist = [query]
for q in querlist:
    cursor.execute(q)
    dat = sqlio.read_sql_query(q, conn)
    links = (dat["urls"].values)
print(querlist)

class MainSpider(scrapy.Spider):
    name = "ar_spiders"
    start_urls = [l for l in links] 

    def parse(self, response):
        urlsite = response.request.url
        if "zyadda" in urlsite :
            title = response.css('article > header > h1').extract()
            description = response.css("div.entry-content.clearfix.single-post-content").extract()
            devimages = response.css("div.single-featured > img").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
            
        elif "almrsal" in urlsite :
            title = response.css('h1').extract()
            description = response.css("div.entry-content.entry.clearfix").extract()
            devimages = response.css("figure > img").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
            
        elif "mosoah" in urlsite :
            title = response.css('h1').extract()
            description = response.css("body > div.mainContentWrap > div > div > div.contentWrap > div.content-post > div:nth-child(5)").extract()
            devimages = response.css("div.content-post > img").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))