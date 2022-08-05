from utils import *


def getSubSitemap():
    for row, index in sitelistpd.iterrows():
        dds =  (index["subSitemap_extracted_at"])
        lastupdatedate = (str(str(dds).split(" ")[0]))
        if (index["subSitemap_extracted_at"]) is None or days_between(str(TodayDate),str(lastupdatedate) ) > 6  :
            mainsitemappath = "collected/{}/mainsitemap".format(index["sitename"])
            fl = (glob.glob("{}/{}".format(mainsitemappath,"*.xml")))
            for f in fl :
                try:
                    f = open(f, 'r', encoding='UTF-8')
                    res = f.readlines()
                    for d in res:
                        data = getUrl(str(d))
                        for i in data:
                            if str(i).endswith(".xml"):
                                request = Request((i), headers=headers)
                                try:
                                    subsitemappath = "collected/{}/subsitemap/".format(index["sitename"])
                                    os.makedirs(subsitemappath, exist_ok = True)
                                    _request = urlopen(request, timeout=30)
                                    update = ''' update sitelist set subSitemap_extracted_at = ? WHERE urls like ? '''
                                    sqlitecursor.execute(update,[TodayDate,index['urls']])
                                    sqliteconn.commit()
                                    with open("{}/{}".format(subsitemappath,str(i).split("/")[-1]) , 'wb') as _outfile:
                                        try:
                                            shutil.copyfileobj(_request, _outfile)
                                            print("FINISH -- DOWNLOADING SUB-SITEMAP FILE: {}".format(_outfile.name))
                                        except Exception as e:
                                            print(e)
                                            continue
                                except Exception as e:
                                    print(e)
                                    continue
                except Exception as e:
                    print(e)
                    continue
                
getSubSitemap()
