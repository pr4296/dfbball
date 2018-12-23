#!/usr/bin/python3
import requests
import json
# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import api_utils as apiUtils
from datetime import date

conn, db = apiUtils.getDbConnection('injuries')
response = apiUtils.getSportsFeed('injury')
injuriesArr = json.loads(response.text)['players']

statusDate = str(date.today())

print(len(injuriesArr))
for p in injuriesArr:
    playerId = p["id"]
    injuryDescription = p["currentInjury"]["description"]
    playingProbability = p["currentInjury"]["playingProbability"]

    insertStatement = """INSERT INTO injuries (playerId, statusDate, injuryDescription, playingProbability) VALUES ({playerId}, '{statusDate}', '{injuryDescription}', '{playingProbability}');""".format(playerId=playerId, statusDate=statusDate, injuryDescription=injuryDescription, playingProbability=playingProbability)

    try:
        db.execute(insertStatement)
        conn.commit()
    except:
        print('failed inserting '+name)
        print(insertStatement)
        conn.rollback()

conn.close()
