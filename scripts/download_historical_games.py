import requests
import json
import sys
from datetime import date, timedelta

# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

import api_utils as apiUtils

from download_daily_games import download

# 2015-2016-regular 10-27-2015 to 4-15-2016
# 2016-playoff 4-16-2016 to 6-19-2016

start = date(2015, 10, 27)
end = date(2016, 4, 15)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2015-2016-regular", str(currDate))
    currDate += day

start = date(2016, 4, 16)
end = date(2016, 6, 19)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2016-playoff", str(currDate))
    currDate += day

# 2016-2017-regular 10-25-2016 to 4-14-2017
# 2017-playoff 4-15-2017 to 6-12-2017

start = date(2016, 10, 25)
end = date(2017, 4, 14)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2016-2017-regular", str(currDate))
    currDate += day

start = date(2017, 4, 15)
end = date(2017, 6, 12)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2017-playoff", str(currDate))
    currDate += day

# 2017-18-regular 10-17-2017 to 4-13-2018
# 2018-playoff 4-14-2018 to 6-17-2018

start = date(2017, 10, 17)
end = date(2018, 4, 13)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2017-2018-regular", str(currDate))
    currDate += day

start = date(2018, 4, 14)
end = date(2018, 6, 17)
day = timedelta(days=1)
currDate = start
while currDate <= end:  
    download("2018-playoff", str(currDate))
    currDate += day