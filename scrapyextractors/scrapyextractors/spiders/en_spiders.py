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

query = '''SELECT * from articles where lang like 'en' and name is null '''

querlist = [query]
for q in querlist:
    cursor.execute(q)
    dat = sqlio.read_sql_query(q, conn)
    links = (dat["urls"].values)
print(querlist)

class MainSpider(scrapy.Spider):
    name = "en_spiders"
    start_urls = [l for l in links] 

    def parse(self, response):
        try : 
            urlsite = response.request.url
        except Exception as e :
            print(e)
            pass
        
        if "linuxhint" in urlsite :
            title = response.css('h1').extract()
            description = response.css("#wpbody").extract()
            #devimages = response.css("div.single-featured > img").extract()
            query = '''update articles set name =%s , description =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description),str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
            
        elif "makeuseof" in urlsite :
            title = response.css('body > div.w-website > div.w-content > article > header > h1').extract()
            description = response.css("#article-body").extract()
            devimages = response.css("body > div.w-website > div.w-content > article > header > div.heading_image.responsive-img.img-size-heading-image.expandable > figure").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
            
        elif "wikihow" in urlsite :
            title = response.css('#section_0 > a').extract()
            description = response.css("#mw-content-text > div").extract()
            devimages = response.css("#step-id-00 > div.mwimg.largeimage.floatcenter").extract()
            query = '''update articles set name =%s , description =%s , devimages =%s where urls like %s '''
            cursor.execute(query, [str(title), str(description), str(devimages), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
        else  :
            title = response.css(' h1').extract()
            #description = response.css("#mw-content-text > div").extract()
            #devimages = response.css("#step-id-00 > div.mwimg.largeimage.floatcenter").extract()
            query = '''update articles set name =%s where urls like %s '''
            cursor.execute(query, [str(title), str(urlsite)])
            print ("SUBMITTED : {}".format(urlsite))
