from sqlite import sqliteconn
import pandas as pd
import os
from urllib.request import Request, urlopen
import shutil
import glob
from datetime import datetime

sitelistpd = pd.read_sql_query("SELECT * from sitelist", sqliteconn)
def getMainSitemap():
    for row, index in sitelistpd.iterrows():
        dds =  (index["mainSitemap_extracted_at"])
        lastupdatedate = (str(str(dds).split(" ")[0]))
        if (index["mainSitemap_extracted_at"]) is None or days_between(str(TodayDate),str(lastupdatedate) ) > 6  :
            mainsitemappath = "collected/{}/mainsitemap".format(index["sitename"])
            os.makedirs(mainsitemappath,exist_ok=True)
            try : 
                request = Request((index["sitemapurl"]),headers=headers)
                _request = urlopen(request, timeout=10)
                mainSitemapFile = ("{}/{}".format(mainsitemappath,"{}_main_sitemap.xml".format(TodayString)))
                with open(mainSitemapFile, 'wb') as _outfile:
                    try:
                        shutil.copyfileobj(_request, _outfile)
                        print("FINISH -- DOWNLOADING SITEMAP FILE: {}".format(_outfile.name))
                        update = ''' update sitelist set mainSitemap_extracted_at = ? WHERE urls like ? '''
                        sqlitecursor.execute(update,[TodayDate,index['urls']])
                        sqliteconn.commit()
                        
                    except Exception as e:
                        pass
                        print(e,index['urls'])
                    
            except Exception as e :
                print(e,index['urls'])
                pass
getMainSitemap()
