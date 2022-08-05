import os
import pandas as pd
import sqlite3

sitelistcsv = pd.read_csv("sitelist.csv")
file = "main.db"

try:
    sqliteconn = sqlite3.connect(file)
    sqlitecursor= sqliteconn.cursor()
    print("Database main.db CREATED OR UPDATED .")
except:
    print("Database main.db NOT CREATED OR UPDATED.")
    
    
def create_sqlite_table():
    table = """ CREATE TABLE IF NOT EXISTS sitelist (
                id integer PRIMARY KEY,
                urls VARCHAR(255)  UNIQUE NOT NULL ,
                sitename VARCHAR(255),
                lang VARCHAR(255) ,
                roboturl VARCHAR(255) ,
                sitemapurl VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                mainSitemap_extracted_at DATETIME,
                subSitemap_extracted_at DATETIME ,
                urlpostgres_extracted_at DATETIME 
            ); """
    print("TABLE sitelist CREATED ")
    return sqlitecursor.execute(table)



def save_sites_sqlite():
    for row, index in sitelistcsv.iterrows():
        roboturl = "{}{}".format(index["urls"],"/robots.txt")
        sitename = 'collected/{}'.format(index["sitename"])
        os.makedirs(sitename, exist_ok = True)
        print("SQLITE CREATED OR UPDATED :::: {}".format(sitename))
        sql = '''INSERT INTO sitelist (urls,sitename,lang,roboturl,sitemapurl) VALUES(?,?,?,?,?) ON CONFLICT( urls) DO NOTHING; '''
        sqlitecursor.execute(sql,(index["urls"],index["sitename"],index["lang"],str(roboturl),str(index["sitemapurl"])))
        sqliteconn.commit()
        updatesql = '''update sitelist  set sitemapurl = ? where urls like ?; '''
        sqlitecursor.execute(updatesql,(index["sitemapurl"],str(index["urls"])))
        sqliteconn.commit()
        
        
