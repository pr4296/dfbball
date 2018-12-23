#!/usr/bin/python3
import requests
import json
# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import api_utils as apiUtils
from datetime import date

conn, db = apiUtils.getDbConnection('team_standings')
response = apiUtils.getDailyStandings('2018-2019-regular')
standingsArr = json.loads(response.text)['teams']

statusDate = str(date.today())

print(len(standingsArr))
for s in standingsArr:
    teamId = s["team"]["id"]
    overallRank = s["overallRank"]["rank"]
    overallGamesBack = s["overallRank"]["gamesBack"]
    conferenceRank = s["conferenceRank"]["rank"]
    conferenceGamesBack = s["conferenceRank"]["gamesBack"]
    conferenceName = s["conferenceRank"]["conferenceName"]
    divisionRank = s["divisionRank"]["rank"]
    divisionGamesBack = s["divisionRank"]["gamesBack"]
    divisionName = s["divisionRank"]["divisionName"]
    wins = s["stats"]["standings"]["wins"]
    losses = s["stats"]["standings"]["losses"]
    winPct = s["stats"]["standings"]["winPct"]
    gamesBack = s["stats"]["standings"]["gamesBack"]

    insertStatement = """INSERT INTO team_standings (id, statusDate, overallRank, overallGamesBack, conferenceRank, conferenceGamesBack, conferenceName, divisionRank, divisionGamesBack, divisionName, wins, losses, winPct, gamesBack) VALUES ({teamId}, '{statusDate}', {overallRank}, {overallGamesBack}, {conferenceRank}, {conferenceGamesBack}, '{conferenceName}', {divisionRank}, {divisionGamesBack}, '{divisionName}', {wins}, {losses}, {winPct}, {gamesBack});""".format(teamId=teamId, statusDate=statusDate, overallRank=overallRank, overallGamesBack=overallGamesBack, conferenceRank=conferenceRank, conferenceGamesBack=conferenceGamesBack, conferenceName=conferenceName, divisionRank=divisionRank, divisionGamesBack=divisionGamesBack, divisionName=divisionName, wins=wins, losses=losses, winPct=winPct, gamesBack=gamesBack)

    try:
        db.execute(insertStatement)
        conn.commit()
        # print('inserted '+firstName+' '+lastName)
    except:
        print('failed inserting '+name)
        print(insertStatement)
        conn.rollback()

conn.close()
