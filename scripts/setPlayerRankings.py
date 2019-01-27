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

# act as a procedure
def main():
    # connect to the db
    conn, db = apiUtils.getDbConnection('player_season_totals', False)

    # columns for all the rankable stats
    columns = ['gameCount', 'fg2PtAtt', 'fg2PtMade', 'fg3PtAtt', 'fg3PtMade', 'ftAtt', 'ftMade', 'offReb', 'defReb', 'ast', 'pts', 'tov', 'stl', 'blk', 'blkAgainst', 'fouls', 'foulsDrawn', 'foulPers', 'foulPersDrawn', 'foulTech', 'foulTechDrawn', 'foulFlag1', 'foulFlag1Drawn', 'foulFlag2', 'foulFlag2Drawn', 'ejections', 'plusMinus', 'minSeconds', 'fpts']

    # build query using columns
    query = """select 
        p.firstName, 
        p.lastName, 
        pst.playerId,
        pst.uploadDate,
        """
    for i in range(len(columns)):
        query+= "pst."+columns[i]+", "
    query += "(offReb+defReb) as reb "
    query += """
        from player_season_totals pst 
        inner join player p 
        on p.id = pst.playerId;""";

    # store the query result in a 2d list
    db.execute(query)
    result = list(db)

    # rankings is a dictionary
    # {playerId: {stat1: rank, stat2: rank ... }}
    rankings = {}

    # rankable columns indexed starting at 4
    for colIndex in range(4, len(result[0])):

        columnName = 'reb' if colIndex == len(result[0])-1 else columns[colIndex-4]

        # all columns are per game except for gameCount
        if colIndex == 4:
            result.sort(key=lambda x: int(x[colIndex]), reverse=True)
        else:
            result.sort(key=lambda x: float(x[colIndex])/float(x[4]), reverse=True)

        rankIndex = 1 # i.e. rankIndex of 4 means player was the 4th highest

        # set the rankings in the rankings dictionary
        for playerRow in result:
            playerId = playerRow[2]
            if playerId not in rankings:
                rankings[playerId] = {}
            rankings[playerId][columnName] = rankIndex
            rankIndex += 1

    # the first part of the insert
    insert = "INSERT INTO player_ranking (playerId, uploadDate, "
    for i in range(len(columns)):
        insert += "rank_"+columns[i]+", "
    insert+= "rank_reb) VALUES "

    # add insert values for each player
    count = 0
    for playerId in rankings:
        insert += "("+str(playerId)+", NOW(), "
        for i in range(len(columns)):
            insert += str(rankings[playerId][columns[i]])+", "
        insert += str(rankings[playerId]['reb'])+")"

        # all except last should have a following comma
        if count < len(rankings)-1:
            insert += ", "
        count += 1
    db.execute(insert)
    deleteQuery = "delete from player_ranking where uploadDate < date_sub(now(), interval 1 minute)"
    db.execute(deleteQuery)
    conn.commit()

if __name__ == "__main__":
   main()
