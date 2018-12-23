import requests
import json

# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

import api_utils as apiUtils

conn, db = apiUtils.getDbConnection('player')
response = apiUtils.getSportsFeed('player')
playerArr = json.loads(response.text)['players']
  
print(len(playerArr))
for pData in playerArr:
    p = pData["player"]
    playerId = p["id"]
    firstName = p["firstName"].replace("'", "''")
    lastName = p["lastName"].replace("'", "''")
    primaryPosition = p["primaryPosition"]
    jerseyNumber = p["jerseyNumber"]
    currentTeamId = p["currentTeam"]["id"] if p["currentTeam"] is not None and p["currentTeam"]["id"] is not None else "NULL"
    isOnRoster = p["currentRosterStatus"] == "ROSTER"
    heightInches = apiUtils.stringHeightToInches(p["height"]) if p["height"] is not None else "NULL"
    weightPounds = p["weight"] if p["weight"] is not None else "NULL"
    birthDate = "'"+p["birthDate"]+"'" if p["birthDate"] is not None else "NULL"
    birthCity = p["birthCity"].replace("'", "''") if p["birthCity"] is not None else "NULL"
    birthCountry = p["birthCountry"].replace("'", "''") if p["birthCountry"] is not None else "NULL"
    isRookie = p["rookie"] == True
    highSchool = p["highSchool"].replace("'","''") if p["highSchool"] is not None else "NULL"
    college = p["college"].replace("'","''") if p["college"] is not None else "NULL"
    shootingHand = p["handedness"]["shoots"] if p["handedness"] is not None else "NULL"
    imgUrl = p["officialImageSrc"]
    twitterHandle = p["socialMediaAccounts"][0]["value"] if len(p["socialMediaAccounts"]) > 0 else "NULL"

    capHit = "NULL"
    fullNoTradeClause = "NULL"
    modifiedNoTradeClause = "NULL"
    noMovementClause = "NULL"
    contractSigningTeamId = "NULL"
    contractYearsCount = "NULL"
    contractTotalSalary = "NULL"
    draftedYear = "NULL"
    draftedTeamId = "NULL"
    draftedPickTeamId = "NULL"
    draftedRound = "NULL"
    draftedRoundPick = "NULL"

    if p["currentContractYear"] is not None and p["currentContractYear"] != "null":
        ccy = p["currentContractYear"]
        capHit =  ccy["capHit"] if ccy["capHit"] is not None else "NULL"
        fullNoTradeClause = ccy["fullNoTradeClause"] if ccy["fullNoTradeClause"] is not None else "NULL"
        modifiedNoTradeClause = ccy["modifiedNoTradeClause"] if ccy["modifiedNoTradeClause"] is not None else "NULL"
        noMovementClause = ccy["noMovementClause"] if ccy["noMovementClause"] is not None else "NULL"
        if ccy["overallContract"] is not None and ccy["overallContract"] != "null":
            oc = ccy["overallContract"]
            contractSigningTeamId = oc["signingTeam"]["id"] if oc["signingTeam"] is not None and oc["signingTeam"]["id"] is not None else "NULL"
            contractYearsCount = oc["totalYears"] if oc["totalYears"] is not None else "NULL"
            contractTotalSalary = oc["totalSalary"] if oc["totalSalary"] else "NULL"
    if p["drafted"] is not None and p["drafted"] != "null":
        dy = p["drafted"]
        draftedYear = dy["year"] if dy["year"] is not None else "NULL"
        draftedTeamId = dy["team"]["id"] if dy["team"] is not None and dy["team"]["id"] is not None else "NULL"
        draftedPickTeamId = dy["pickTeam"]["id"] if dy["pickTeam"] is not None and dy["pickTeam"]["id"] is not None else "NULL"
        draftedRound = dy["round"] if dy["round"] is not None else "NULL"
        draftedRoundPick = dy["roundPick"] if dy["roundPick"] is not None else "NULL"

    insertStatement = """INSERT INTO player (id, firstName, lastName, primaryPosition, jerseyNumber, currentTeamId, isOnRoster, heightInches, weightPounds, birthDate, birthCity, birthCountry, isRookie, highSchool, college, shootingHand, imgUrl, twitterHandle, capHit, fullNoTradeClause, modifiedNoTradeClause, noMovementClause, contractSigningTeamId, contractYearsCount, contractTotalSalary, draftedYear, draftedTeamId, draftedPickTeamId, draftedRound, draftedRoundPick) VALUES ({playerId}, '{firstName}', '{lastName}', '{primaryPosition}', '{jerseyNumber}', {currentTeamId}, {isOnRoster}, {heightInches}, {weightPounds}, {birthDate}, '{birthCity}', '{birthCountry}', {isRookie}, '{highSchool}', '{college}', '{shootingHand}', '{imgUrl}', '{twitterHandle}', {capHit}, {fullNoTradeClause}, {modifiedNoTradeClause}, {noMovementClause}, {contractSigningTeamId}, {contractYearsCount}, {contractTotalSalary}, {draftedYear}, {draftedTeamId}, {draftedPickTeamId}, {draftedRound}, {draftedRoundPick});""".format(playerId=playerId, firstName=firstName, lastName=lastName, primaryPosition=primaryPosition, jerseyNumber=jerseyNumber, currentTeamId=currentTeamId, isOnRoster=isOnRoster, heightInches=heightInches, weightPounds=weightPounds, birthDate=birthDate, birthCity=birthCity, birthCountry=birthCountry, isRookie=isRookie, highSchool=highSchool, college=college, shootingHand=shootingHand, imgUrl=imgUrl, twitterHandle=twitterHandle, capHit=capHit, fullNoTradeClause=fullNoTradeClause, modifiedNoTradeClause=modifiedNoTradeClause, noMovementClause=noMovementClause, contractSigningTeamId=contractSigningTeamId, contractYearsCount=contractYearsCount, contractTotalSalary=contractTotalSalary, draftedYear=draftedYear, draftedTeamId=draftedTeamId, draftedPickTeamId=draftedPickTeamId, draftedRound=draftedRound, draftedRoundPick=draftedRoundPick)

    try:
        db.execute(insertStatement)
        conn.commit()
        # print('inserted '+firstName+' '+lastName)
    except:
        print('failed inserting '+firstName+' '+lastName)
        print(insertStatement)
        conn.rollback()

conn.close()