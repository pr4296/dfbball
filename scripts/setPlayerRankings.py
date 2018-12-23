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

def main():
    conn, db = apiUtils.getDbConnection('player', False)
    query = "SELECT distinct id from player";
    playerRankings = []
    db.execute(query)
    result = db.fetchall()
    for playerTuple in result:
        playerId = playerTuple[0]

        query = "SELECT (pts+0.5*fg3PtMade+offReb*1.25-0.5*tov) as offScore, (defReb*1.25+stl*2+blk*2) as defScore from daily_player_box_stats d inner join game g on g.id = d.gameId where d.playerId="+str(playerId)+" and playedStatus='COMPLETED' order by g.startTime desc limit 25"

        db.execute(query)
        bs = db.fetchall()

        offTotal = 0
        defTotal = 0
        count = 0
        for row in bs:
            # pts+ast*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+to*-0.5
            count += 1
            offTotal += row[0]
            defTotal += row[1]
        if count > 0:
            playerRankings.append({'id':playerId, 'offScore': round(offTotal/count), 'defScore': round(defTotal/count)})
    
    playerRankings.sort(key=lambda x: x['offScore'], reverse=True)
    maxOff = playerRankings[0]['offScore']
    for obj in playerRankings:
        obj['offRating'] = round((obj['offScore']*50)/maxOff)+49
    
    playerRankings.sort(key=lambda x: x['defScore'], reverse=True)
    maxDef = playerRankings[0]['defScore']
    for obj in playerRankings:
        obj['defRating'] = round(obj['defScore']*50/maxDef)+49
    
    playerRankings.sort(key=lambda x: x['offScore']+x['defScore'], reverse=True)
    maxOverall = playerRankings[0]['offScore']+playerRankings[0]['defScore']
    for obj in playerRankings:
        obj['overallRating'] = round((obj['offScore']+obj['defScore'])*50/maxOverall)+49

    for obj in playerRankings:
        query = "INSERT INTO player_ranking (rankingDate, playerId, overallRating, offRating, defRating) VALUES (DATE(DATE_SUB(now(), INTERVAL 6 HOUR)), "+str(obj['id'])+", "+str(obj['overallRating'])+", "+str(obj['offRating'])+", "+str(obj['defRating'])+")"

        db.execute(query)
        conn.commit()
    # CREATE TABLE player_ranking (
    # rankingDate DATETIME NOT NULL,
    # playerId INT NOT NULL,
    # overallRating INT,
    # offRating INT,
    # defRating INT,
    # PRIMARY KEY (playerId, rankingDate)


# import doesn't run here
if __name__ == "__main__":
   main()
