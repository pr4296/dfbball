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

def download(season, gameDate):
    conn, db = apiUtils.getDbConnection('daily_player_box_stats', False)
    response = apiUtils.getDailyBoxScore(season, gameDate)
    if response.status_code != 200:
        print('request status code '+str(response.status_code))
        return

    resp = json.loads(response.text)
    if "gamelogs" not in resp:
        return
    playerArr = resp['gamelogs']

    print(season, gameDate, len(playerArr))

    deleteStatement = "DELETE FROM daily_player_box_stats WHERE DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) = '"+gameDate+"'";

    try:
        db.execute(deleteStatement)
        conn.commit()
    except:
        print(deleteStatement)
        conn.rollback()

    for pData in playerArr:

        playerId = pData["player"]["id"]

        g = pData["game"]
        gameId = g["id"]

        startTimeUnformatted = g["startTime"]
        startTime = startTimeUnformatted[:-5].replace('T', ' ')
        # "2018-05-16T00:30:00.000Z"" to 2018-05-16 00:30:00

        awayTeamAbbreviation = g["awayTeamAbbreviation"]
        homeTeamAbbreviation = g["homeTeamAbbreviation"]
        
        playerTeamId = pData["team"]["id"]

        position = pData["player"]["position"]

        s = pData["stats"]

        fg = s["fieldGoals"]
        fg2PtAtt = fg["fg2PtAtt"]
        fg2PtMade = fg["fg2PtMade"]
        fg3PtAtt = fg["fg3PtAtt"]
        fg3PtMade = fg["fg3PtMade"]
        
        ft = s["freeThrows"]
        ftAtt = ft["ftAtt"]
        ftMade = ft["ftMade"]

        reb = s["rebounds"]
        offReb = reb["offReb"]
        defReb = reb["defReb"]

        ast = s["offense"]["ast"]
        pts = s["offense"]["pts"]

        de = s["defense"]
        tov = de["tov"]
        stl = de["stl"]
        blk = de["blk"]
        blkAgainst = de["blkAgainst"]

        msc = s["miscellaneous"]
        fouls = msc["fouls"] if "fouls" in msc else 0
        foulsDrawn = msc["foulsDrawn"] if "foulsDrawn" in msc else 0
        foulPers = msc["foulPers"] if "foulPers" in msc else 0
        foulPersDrawn = msc["foulPersDrawn"] if "foulPersDrawn" in msc else 0
        foulTech = msc["foulTech"] if "foulTech" in msc else 0
        foulTechDrawn = msc["foulTechDrawn"] if "foulTechDrawn" in msc else 0
        foulFlag1 = msc["foulFlag1"] if "foulFlag1" in msc else 0
        foulFlag1Drawn = msc["foulFlag1Drawn"] if "foulFlag1Drawn" in msc else 0
        foulFlag2 = msc["foulFlag2"] if "foulFlag2" in msc else 0
        foulFlag2Drawn = msc["foulFlag2Drawn"] if "foulFlag2Drawn" in msc else 0
        ejections = msc["ejections"] if "ejections" in msc else 0
        plusMinus = msc["plusMinus"]
        minSeconds = msc["minSeconds"]
        startedGame = "true" if "startedGame" in msc and msc["startedGame"] != 0 else "false"

        

        insertStatement = """INSERT INTO daily_player_box_stats (playerId, gameId, startTime, awayTeamAbbreviation, homeTeamAbbreviation, playerTeamId, position, fg2PtAtt, fg2PtMade, fg3PtAtt, fg3PtMade, ftAtt, ftMade, offReb, defReb, ast, pts, tov, stl, blk, blkAgainst, fouls, foulsDrawn, foulPers, foulPersDrawn, foulTech, foulTechDrawn, foulFlag1, foulFlag1Drawn, foulFlag2, foulFlag2Drawn, ejections, plusMinus, minSeconds, startedGame) VALUES ({playerId}, {gameId}, '{startTime}', '{awayTeamAbbreviation}', '{homeTeamAbbreviation}', {playerTeamId}, '{position}', {fg2PtAtt}, {fg2PtMade}, {fg3PtAtt}, {fg3PtMade}, {ftAtt}, {ftMade}, {offReb}, {defReb}, {ast}, {pts}, {tov}, {stl}, {blk}, {blkAgainst}, {fouls}, {foulsDrawn}, {foulPers}, {foulPersDrawn}, {foulTech}, {foulTechDrawn}, {foulFlag1}, {foulFlag1Drawn}, {foulFlag2}, {foulFlag2Drawn}, {ejections}, {plusMinus}, {minSeconds}, {startedGame});""".format(playerId=playerId, gameId=gameId, startTime=startTime, awayTeamAbbreviation=awayTeamAbbreviation, homeTeamAbbreviation=homeTeamAbbreviation, playerTeamId=playerTeamId, position=position, fg2PtAtt=fg2PtAtt, fg2PtMade=fg2PtMade, fg3PtAtt=fg3PtAtt, fg3PtMade=fg3PtMade, ftAtt=ftAtt, ftMade=ftMade, offReb=offReb, defReb=defReb, ast=ast, pts=pts, tov=tov, stl=stl, blk=blk, blkAgainst=blkAgainst, fouls=fouls, foulsDrawn=foulsDrawn, foulPers=foulPers, foulPersDrawn=foulPersDrawn, foulTech=foulTech, foulTechDrawn=foulTechDrawn, foulFlag1=foulFlag1, foulFlag1Drawn=foulFlag1Drawn, foulFlag2=foulFlag2, foulFlag2Drawn=foulFlag2Drawn, ejections=ejections, plusMinus=plusMinus, minSeconds=minSeconds, startedGame=startedGame)

        try:
            db.execute(insertStatement)
            conn.commit()
            # print('inserted '+firstName+' '+lastName)
        except:
            print('failed inserting '+playerId+' for date '+gameDate)
            print(insertStatement)
            conn.rollback()

    conn.close()
    #if len(playerArr) > 0:
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
