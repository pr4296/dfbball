#!/usr/bin/python3
import requests
import json
import sys
import datetime
from datetime import timedelta
import time

# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

import api_utils as apiUtils

def download(season, gameDate='', clearTable=False):
    conn, db = apiUtils.getDbConnection('game', clearTable)
    if gameDate == '':
        response = apiUtils.getGames(season)
    else:
        response = apiUtils.getDailyGames(season, gameDate)
    if response.status_code != 200:
        print('request status code '+str(response.status_code))
        exit(1)

    resp = json.loads(response.text)
    if "games" not in resp:
        return
    gameArr = resp['games']

    deleteStatement = "DELETE FROM game WHERE DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) = '"+gameDate+"'";
    
    try:
        db.execute(deleteStatement)
        conn.commit()
    except:
        print(deleteStatement)
        conn.rollback()

    print(season, gameDate, len(gameArr))
    for gData in gameArr:

        s = gData["schedule"]
        gameId = s["id"]
        startTimeUnformatted = s["startTime"]
        startTime = startTimeUnformatted[:-5].replace('T', ' ')
        
        # "2018-05-16T00:30:00.000Z"" to 2018-05-16 00:30:00
        awayTeamId = s["awayTeam"]["id"]
        awayTeamAbbreviation = s["awayTeam"]["abbreviation"]
        homeTeamId = s["homeTeam"]["id"]
        homeTeamAbbreviation = s["homeTeam"]["abbreviation"]
        venueId = s["venue"]["id"]
        venueName = s["venue"]["name"]
        scheduleStatus = s["scheduleStatus"]
        delayedOrPostponedReason = s["delayedOrPostponedReason"]
        playedStatus = s["playedStatus"]
        
        sc = gData["score"]
        currentQuarter = sc["currentQuarter"] if isinstance(sc["currentQuarter"], (int)) else "NULL"
        currentQuarterSecondsRemaining = sc["currentQuarterSecondsRemaining"] if isinstance(sc["currentQuarterSecondsRemaining"], (int)) else "NULL"
        currentIntermission = sc["currentIntermission"] if isinstance(sc["currentIntermission"], (int)) else "NULL"
        awayScoreTotal = sc["awayScoreTotal"] if isinstance(sc["awayScoreTotal"], (int)) else "NULL"
        homeScoreTotal = sc["homeScoreTotal"] if isinstance(sc["homeScoreTotal"], (int)) else "NULL"

        q = sc["quarters"] if "quarters" in sc else ""
        quarter1awayScore = q[0]["awayScore"] if len(q) > 0 else 0
        quarter1homeScore = q[0]["homeScore"] if len(q) > 0 else 0
        quarter2awayScore = q[1]["awayScore"] if len(q) > 1 else 0
        quarter2homeScore = q[1]["homeScore"] if len(q) > 1 else 0
        quarter3awayScore = q[2]["awayScore"] if len(q) > 2 else 0
        quarter3homeScore = q[2]["homeScore"] if len(q) > 2 else 0
        quarter4awayScore = q[3]["awayScore"] if len(q) > 3 else 0
        quarter4homeScore = q[3]["homeScore"] if len(q) > 3 else 0
        overtime1homeScore = q[4]["awayScore"] if len(q) > 4 else 0
        overtime1awayScore = q[4]["homeScore"] if len(q) > 4 else 0
        overtime2homeScore = q[5]["awayScore"] if len(q) > 5 else 0
        overtime2awayScore = q[5]["homeScore"] if len(q) > 5 else 0
        overtime3homeScore = q[6]["awayScore"] if len(q) > 6 else 0
        overtime3awayScore = q[6]["homeScore"] if len(q) > 6 else 0
        overtime4homeScore = q[7]["awayScore"] if len(q) > 7 else 0
        overtime4awayScore = q[7]["homeScore"] if len(q) > 7 else 0
        overtime5homeScore = q[8]["awayScore"] if len(q) > 8 else 0
        overtime5awayScore = q[8]["homeScore"] if len(q) > 8 else 0
        overtime6homeScore = q[9]["awayScore"] if len(q) > 9 else 0
        overtime6awayScore = q[9]["homeScore"] if len(q) > 9 else 0
        
        insertStatement = """INSERT INTO game (id, startTime, awayTeamId, awayTeamAbbreviation, homeTeamId, homeTeamAbbreviation, venueId, venueName, scheduleStatus, delayedOrPostponedReason, playedStatus, currentQuarter, currentQuarterSecondsRemaining, currentIntermission, awayScoreTotal, homeScoreTotal, quarter1awayScore, quarter1homeScore, quarter2awayScore, quarter2homeScore, quarter3awayScore, quarter3homeScore, quarter4awayScore, quarter4homeScore, overtime1awayScore, overtime1homeScore, overtime2awayScore, overtime2homeScore, overtime3awayScore, overtime3homeScore, overtime4awayScore, overtime4homeScore, overtime5awayScore, overtime5homeScore, overtime6awayScore, overtime6homeScore) VALUES ({gameId}, '{startTime}', {awayTeamId}, '{awayTeamAbbreviation}', {homeTeamId}, '{homeTeamAbbreviation}', {venueId}, '{venueName}', '{scheduleStatus}', '{delayedOrPostponedReason}', '{playedStatus}', {currentQuarter}, {currentQuarterSecondsRemaining}, '{currentIntermission}', {awayScoreTotal}, {homeScoreTotal}, {quarter1awayScore}, {quarter1homeScore}, {quarter2awayScore}, {quarter2homeScore}, {quarter3awayScore}, {quarter3homeScore}, {quarter4awayScore}, {quarter4homeScore}, {overtime1awayScore}, {overtime1homeScore}, {overtime2awayScore}, {overtime2homeScore},{overtime3awayScore}, {overtime3homeScore},{overtime4awayScore}, {overtime4homeScore},{overtime5awayScore}, {overtime5homeScore},{overtime6awayScore}, {overtime6homeScore});""".format(gameId=gameId, startTime=startTime, awayTeamId=awayTeamId, awayTeamAbbreviation=awayTeamAbbreviation, homeTeamId=homeTeamId, homeTeamAbbreviation=homeTeamAbbreviation, venueId=venueId, venueName=venueName, scheduleStatus=scheduleStatus, delayedOrPostponedReason=delayedOrPostponedReason, playedStatus=playedStatus, currentQuarter=currentQuarter, currentQuarterSecondsRemaining=currentQuarterSecondsRemaining, currentIntermission=currentIntermission, awayScoreTotal=awayScoreTotal, homeScoreTotal=homeScoreTotal, quarter1awayScore=quarter1awayScore, quarter1homeScore=quarter1homeScore, quarter2awayScore=quarter2awayScore, quarter2homeScore=quarter2homeScore, quarter3awayScore=quarter3awayScore, quarter3homeScore=quarter3homeScore, quarter4awayScore=quarter4awayScore, quarter4homeScore=quarter4homeScore, overtime1awayScore=overtime1awayScore, overtime1homeScore=overtime1homeScore, overtime2awayScore=overtime2awayScore, overtime2homeScore=overtime2homeScore, overtime3awayScore=overtime3awayScore, overtime3homeScore=overtime3homeScore, overtime4awayScore=overtime4awayScore, overtime4homeScore=overtime4homeScore, overtime5awayScore=overtime5awayScore, overtime5homeScore=overtime5homeScore, overtime6awayScore=overtime6awayScore, overtime6homeScore=overtime6homeScore)

        try:
            db.execute(insertStatement)
            conn.commit()
        except:
            print('failed inserting '+str(gameId)+' for date '+gameDate)
            print(insertStatement)
            conn.rollback()

    conn.close()
    time.sleep(10)

def main():
    if len(sys.argv) <= 3:
        print('using today\'s date')
        season = '2018-2019-regular'
        gameDate = (datetime.datetime.today()-timedelta(hours=6)).strftime('%Y%m%d')
    else:
        season = sys.argv[1]
        gameDate = sys.argv[2]
        print(season+", "+gameDate+": ", end='')

    download(season, gameDate)

# import doesn't run here
if __name__ == "__main__":
   main()
