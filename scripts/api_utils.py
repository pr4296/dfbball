import requests
import json

# This is because MySQLdb only works for python2 
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def stringHeightToInches(val):
    if type(val) != str or val == "null":
        return "NULL"
    feet = val.split("'")[0].strip()
    inches = val.split("'")[1].split("\"")[0].strip()
    return int(feet)*12+int(inches)

def getDbConnection(tableName, clearFromTable=True):
    # local MySQL connection
    with open('../mysql_auth.json') as authFile:
        mysql_auth_data = json.load(authFile)
    conn = MySQLdb.connect(host=mysql_auth_data["host"],
                        user=mysql_auth_data["user"],
                        passwd=mysql_auth_data["passwd"],
                        db=mysql_auth_data["db"])
    db = conn.cursor()
    if clearFromTable:
        clearTable = "DELETE FROM "+tableName+";"
        db.execute(clearTable)
    return (conn, db)

def getSportsFeed(feed):
    with open('../mysportsfeeds_auth.json') as authFile:
        api_auth_data = json.load(authFile)
    apiUrl = api_auth_data[feed+'url']
    authValues = (api_auth_data['username'], api_auth_data['password'])
    response = requests.get(apiUrl, auth=authValues)
    return response

def getDailyStandings(season):
    with open('../mysportsfeeds_auth.json') as authFile:
        api_auth_data = json.load(authFile)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    apiUrl = 'https://api.mysportsfeeds.com/v2.0/pull/nba/'+season+'/standings.json'
    print(apiUrl)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    response = requests.get(apiUrl, auth=authValues)
    return response

def getDailyBoxScore(season, date):
    date = date.replace('-','')
    with open('../mysportsfeeds_auth.json') as authFile:
        api_auth_data = json.load(authFile)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    apiUrl = 'https://api.mysportsfeeds.com/v2.0/pull/nba/'+season+'/date/'+date+'/player_gamelogs.json'
    print(apiUrl)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    response = requests.get(apiUrl, auth=authValues)
    return response

def getDailyGames(season, date):
    date = date.replace('-','')
    with open('../mysportsfeeds_auth.json') as authFile:
        api_auth_data = json.load(authFile)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    apiUrl = 'https://api.mysportsfeeds.com/v2.0/pull/nba/'+season+'/date/'+date+'/games.json'
    print(apiUrl)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    response = requests.get(apiUrl, auth=authValues)
    return response

def getGames(season):
    with open('../mysportsfeeds_auth.json') as authFile:
        api_auth_data = json.load(authFile)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    apiUrl = 'https://api.mysportsfeeds.com/v2.0/pull/nba/'+season+'/games.json'
    print(apiUrl)
    authValues = (api_auth_data['username'], api_auth_data['password'])
    response = requests.get(apiUrl, auth=authValues)
    return response