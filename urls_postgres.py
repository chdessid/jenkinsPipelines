from utils import *
from sqlite import *

sitelistpd = pd.read_sql_query("SELECT * from sitelist", sqliteconn)
def urls_from_sitemap():
    for row, index in sitelistpd.iterrows():
        subsitemappath = "collected/{}/subsitemap/".format(index["sitename"])
        if "wikihow" not in subsitemappath:
            files = (glob.glob("{}/{}".format(subsitemappath,"*.xml")))
            for f in files:
                try:
                    f = open(f, 'r', encoding='UTF-8')
                    res = f.readlines()
                    for d in res:
                        data = getUrl(str(d))
                        for i in data:
                            cleanurl = excludepatter(i)
                            if (cleanurl) is not None:
                                query = '''insert into articles (urls,sitename,lang) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING'''
                                pgcursor.execute(query, [str(cleanurl),  str(index["sitename"]), str(index["lang"])])
                                print ("Submitted :: " , cleanurl)

                except Exception as e :
                    print(e)
                    pass
                
                
urls_from_sitemap()
