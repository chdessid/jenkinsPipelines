import pandas as pd
import sqlite3
from urllib.request import Request, urlopen
import os 
import re
import shutil
import glob
from datetime import datetime
from urllib.parse import urlparse, urlunparse

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
