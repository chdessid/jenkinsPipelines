import pandas as pd
import sqlite3
from urllib.request import Request, urlopen
import os 
import re
import shutil
import glob
from datetime import datetime
from urllib.parse import urlparse, urlunparse
from decouple import config

SITEMAP_PATH = config('SITEMAP_PATH')



headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.11 (KHTML, like Gecko) '
                            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Connection': 'keep-alive'}

now = datetime.now()
TodayDate = (now.strftime('%Y-%m-%d'))
TodayString = (now.strftime('%Y%m%d'))

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)
  
def getUrl(string):
    """
    Extract Urls from sitemap xml
    :param string:
    :return:
    """
    try:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)

    except Exception as e :
        print(e)
        pass
    return [x[0] for x in url]
  
  
def excludepatter(str):
    excludestrings = [ ".jpg","wp-content",
                      ".png","cdn","tags","/tag/","category/"
                      "category","http://www.sitemaps.org",
                      "http://www.google.com","http://www.w3.org"]
    isMatch = [True for x in excludestrings if x in str]
    if True in isMatch:
        print ("IGNORED :: ", str)
    else :
        return(str)


