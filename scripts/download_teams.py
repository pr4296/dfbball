import requests
import json

# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

import api_utils as apiUtils

conn, db = apiUtils.getDbConnection('team')
response = apiUtils.getSportsFeed('team')
teamArr = json.loads(response.text)['teams']

print(len(teamArr))
for tData in teamArr:
    t = tData["team"]
    teamId = t["id"]
    city = t["city"]
    name = t["name"]
    abbreviation = t["abbreviation"]
    homeVenueId = t["homeVenue"]["id"]
    homeVenueName = t["homeVenue"]["name"]

    insertStatement = """INSERT INTO team (id, city, teamName, abbreviation, venueId, venueName) VALUES ({teamId}, '{city}', '{name}', '{abbreviation}', {homeVenueId}, '{homeVenueName}');""".format(teamId=teamId, city=city, name=name, abbreviation=abbreviation, homeVenueId=homeVenueId, homeVenueName=homeVenueName)

    try:
        db.execute(insertStatement)
        conn.commit()
        # print('inserted '+firstName+' '+lastName)
    except:
        print('failed inserting '+name)
        print(insertStatement)
        conn.rollback()

conn.close()
