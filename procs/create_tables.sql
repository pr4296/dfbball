USE basketbrief;

CREATE TABLE player(
    id INT NOT NULL,
    firstName VARCHAR(30),
    lastName VARCHAR(30),
    primaryPosition VARCHAR(2),
    jerseyNumber VARCHAR(4),
    currentTeamId TINYINT,
    isOnRoster BOOLEAN NOT NULL,
    heightInches TINYINT,
    weightPounds INT,
    birthDate DATE,
    birthCity VARCHAR(50),
    birthCountry VARCHAR(50),
    isRookie BOOLEAN NOT NULL,
    highSchool VARCHAR(100),
    college VARCHAR(100),
    shootingHand VARCHAR(4),
    imgUrl VARCHAR(200),
    twitterHandle VARCHAR(15),
    capHit INT,
    fullNoTradeClause BOOLEAN,
    modifiedNoTradeClause BOOLEAN,
    noMovementClause BOOLEAN,
    contractSigningTeamId TINYINT,
    contractYearsCount TINYINT,
    contractTotalSalary INT,
    draftedYear INT,
    draftedTeamId TINYINT,
    draftedPickTeamId TINYINT,
    draftedRound TINYINT,
    draftedRoundPick TINYINT,
    PRIMARY KEY (id)
);

CREATE TABLE team(
    id TINYINT NOT NULL,
    city VARCHAR(20) NOT NULL,
    teamName VARCHAR(20) NOT NULL,
    abbreviation VARCHAR(3) NOT NULL,
    venueId INT,
    venueName VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE daily_player_box_stats(
    playerId INT NOT NULL,
    gameId INT NOT NULL,
    startTime DATETIME,
    awayTeamAbbreviation VARCHAR(3),
    homeTeamAbbreviation VARCHAR(3),
    playerTeamId TINYINT NOT NULL,
    position VARCHAR(2),
    fg2PtAtt TINYINT,
    fg2PtMade TINYINT,
    fg3PtAtt TINYINT,
    fg3PtMade TINYINT,
    ftAtt TINYINT,
    ftMade TINYINT,
    offReb TINYINT,
    defReb TINYINT,
    ast TINYINT,
    pts TINYINT,
    tov TINYINT,
    stl TINYINT,
    blk TINYINT,
    blkAgainst TINYINT,
    fouls TINYINT,
    foulsDrawn TINYINT,
    foulPers TINYINT,
    foulPersDrawn TINYINT,
    foulTech TINYINT,
    foulTechDrawn TINYINT,
    foulFlag1 TINYINT,
    foulFlag1Drawn TINYINT,
    foulFlag2 TINYINT,
    foulFlag2Drawn TINYINT,
    ejections TINYINT,
    plusMinus TINYINT,
    minSeconds INT,
    startedGame BOOLEAN,
    PRIMARY KEY (playerId, gameId)
);

CREATE TABLE player_season_totals (
    playerId INT NOT NULL,
    uploadDate DATETIME NOT NULL,
    gameCount INT,
    fg2PtAtt INT,
    fg2PtMade INT,
    fg3PtAtt INT,
    fg3PtMade INT,
    ftAtt INT,
    ftMade INT,
    offReb INT,
    defReb INT,
    ast INT,
    pts INT,
    tov INT,
    stl INT,
    blk INT,
    blkAgainst INT,
    fouls INT,
    foulsDrawn INT,
    foulPers INT,
    foulPersDrawn INT,
    foulTech INT,
    foulTechDrawn INT,
    foulFlag1 INT,
    foulFlag1Drawn INT,
    foulFlag2 INT,
    foulFlag2Drawn INT,
    ejections INT,
    plusMinus INT,
    minSeconds INT,
    startedGame INT,
    fpts FLOAT,
    PRIMARY KEY (playerId, uploadDate)
);

CREATE TABLE player_daily (
    playerId INT NOT NULL,
    uploadDate DATETIME,
    gameId INT NOT NULL,
    startTime DATETIME,
    awayTeamAbbreviation VARCHAR(3),
    homeTeamAbbreviation VARCHAR(3),
    playerTeamId TINYINT,
    position VARCHAR(2),
    fg2PtAtt INT,
    fg2PtMade INT,
    fg3PtAtt INT,
    fg3PtMade INT,
    ftAtt INT,
    ftMade INT,
    offReb INT,
    defReb INT,
    ast INT,
    pts INT,
    tov INT,
    stl INT,
    blk INT,
    blkAgainst INT,
    fouls INT,
    foulsDrawn INT,
    foulPers INT,
    foulPersDrawn INT,
    foulTech INT,
    foulTechDrawn INT,
    foulFlag1 INT,
    foulFlag1Drawn INT,
    foulFlag2 INT,
    foulFlag2Drawn INT,
    ejections INT,
    plusMinus INT,
    minSeconds INT,
    startedGame INT,
    fpts FLOAT,
    PRIMARY KEY (playerId, uploadDate)
);

CREATE TABLE game(
    id INT NOT NULL,
    startTime DATETIME,
    awayTeamId TINYINT,
    awayTeamAbbreviation VARCHAR(3),
    homeTeamId TINYINT,
    homeTeamAbbreviation VARCHAR(3),
    venueId INT,
    venueName VARCHAR(50),
    scheduleStatus VARCHAR(20),
    delayedOrPostponedReason VARCHAR(50),
    playedStatus VARCHAR(50),
    currentQuarter TINYINT,
    currentQuarterSecondsRemaining INT,
    currentIntermission VARCHAR(10),
    awayScoreTotal INT,
    homeScoreTotal INT,
    quarter1awayScore TINYINT,
    quarter1homeScore TINYINT,
    quarter2awayScore TINYINT,
    quarter2homeScore TINYINT,
    quarter3awayScore TINYINT,
    quarter3homeScore TINYINT,
    quarter4awayScore TINYINT,
    quarter4homeScore TINYINT,
    overtime1awayScore TINYINT,
    overtime1homeScore TINYINT,
    overtime2awayScore TINYINT,
    overtime2homeScore TINYINT,
    overtime3awayScore TINYINT,
    overtime3homeScore TINYINT,
    overtime4awayScore TINYINT,
    overtime4homeScore TINYINT,
    overtime5awayScore TINYINT,
    overtime5homeScore TINYINT,
    overtime6awayScore TINYINT,
    overtime6homeScore TINYINT,
    PRIMARY KEY (id)
);

CREATE TABLE injuries(
    playerId INT NOT NULL,
    statusDate DATE NOT NULL,
    injuryDescription VARCHAR(50),
    playingProbability VARCHAR(20),
    PRIMARY KEY (playerId, statusDate)
);

CREATE TABLE team_standings (
    id TINYINT NOT NULL,
    statusDate DATE NOT NULL,
    overallRank TINYINT,
    overallGamesBack FLOAT,
    conferenceRank TINYINT,
    conferenceGamesBack FLOAT,
    conferenceName VARCHAR(10),
    divisionRank TINYINT,
    divisionGamesBack FLOAT,
    divisionName VARCHAR(15),
    wins TINYINT,
    losses TINYINT,
    winPct FLOAT,
    gamesBack FLOAT,
    PRIMARY KEY (id, statusDate)
);

CREATE TABLE game_lineup (
    gameId INT,
    awayExpectedStarter1id INT,
    awayExpectedStarter2id INT,
    awayExpectedStarter3id INT,
    awayExpectedStarter4id INT,
    awayExpectedStarter5id INT,
    awayExpectedBench1id INT,
    awayExpectedBench2id INT,
    awayExpectedBench3id INT,
    awayExpectedBench4id INT,
    awayExpectedBench5id INT,
    awayExpectedBench6id INT,
    awayExpectedBench7id INT,
    awayExpectedBench8id INT,
    awayExpectedBench9id INT,
    awayExpectedBench10id INT,
    homeExpectedStarter1id INT,
    homeExpectedStarter2id INT,
    homeExpectedStarter3id INT,
    homeExpectedStarter4id INT,
    homeExpectedStarter5id INT,
    homeExpectedBench1id INT,
    homeExpectedBench2id INT,
    homeExpectedBench3id INT,
    homeExpectedBench4id INT,
    homeExpectedBench5id INT,
    homeExpectedBench6id INT,
    homeExpectedBench7id INT,
    homeExpectedBench8id INT,
    homeExpectedBench9id INT,
    homeExpectedBench10id INT,
    awayActualStarter1id INT,
    awayActualStarter2id INT,
    awayActualStarter3id INT,
    awayActualStarter4id INT,
    awayActualStarter5id INT,
    awayActualBench1id INT,
    awayActualBench2id INT,
    awayActualBench3id INT,
    awayActualBench4id INT,
    awayActualBench5id INT,
    awayActualBench6id INT,
    awayActualBench7id INT,
    awayActualBench8id INT,
    awayActualBench9id INT,
    awayActualBench10id INT,
    homeActualStarter1id INT,
    homeActualStarter2id INT,
    homeActualStarter3id INT,
    homeActualStarter4id INT,
    homeActualStarter5id INT,
    homeActualBench1id INT,
    homeActualBench2id INT,
    homeActualBench3id INT,
    homeActualBench4id INT,
    homeActualBench5id INT,
    homeActualBench6id INT,
    homeActualBench7id INT,
    homeActualBench8id INT,
    homeActualBench9id INT,
    homeActualBench10id INT
);

CREATE TABLE player_ranking (
    playerId INT NOT NULL,
    uploadDate DATE NOT NULL,
    rank_gameCount INT,
    rank_fg2PtAtt INT,
    rank_fg2PtMade INT,
    rank_fg3PtAtt INT,
    rank_fg3PtMade INT,
    rank_ftAtt INT,
    rank_ftMade INT,
    rank_offReb INT,
    rank_defReb INT,
    rank_ast INT,
    rank_pts INT,
    rank_tov INT,
    rank_stl INT,
    rank_blk INT,
    rank_blkAgainst INT,
    rank_fouls INT,
    rank_foulsDrawn INT,
    rank_foulPers INT,
    rank_foulPersDrawn INT,
    rank_foulTech INT,
    rank_foulTechDrawn INT,
    rank_foulFlag1 INT,
    rank_foulFlag1Drawn INT,
    rank_foulFlag2 INT,
    rank_foulFlag2Drawn INT,
    rank_ejections INT,
    rank_plusMinus INT,
    rank_minSeconds INT,
    rank_fpts INT,
    rank_reb INT,
    PRIMARY KEY (playerId, uploadDate)
);

CREATE TABLE play_by_play (
    thp1 INT NOT NULL, /* in ascending order */
    thp2 INT NOT NULL, /* the home and away team players*/
    thp3 INT NOT NULL,
    thp4 INT NOT NULL,
    thp5 INT NOT NULL,
    tap1 INT NOT NULL,
    tap2 INT NOT NULL,
    tap3 INT NOT NULL,
    tap4 INT NOT NULL,
    tap5 INT NOT NULL,
    quarter TINYINT NOT NULL,
    secondsElapsed INT NOT NULL,
    awayScore INT NOT NULL,
    homeScore INT NOT NULL,
    playerId INT NOT NULL
);

CREATE TABLE login_info (
    username VARCHAR(32) NOT NULL,
    passwordHash CHAR(64) NOT NULL,
    salt CHAR(64) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE login_token (
    username VARCHAR(32) NOT NULL,
    token VARCHAR(32) NOT NULL,
    PRIMARY KEY(username, token)
);

CREATE TABLE user_picks (
    username VARCHAR(32) NOT NULL,
    pos VARCHAR(2) NOT NULL,
    pickDate DATE NOT NULL,
    playerId INT NOT NULL
);

CREATE TABLE available_players (
    playerId INT NOT NULL,
    uploadDate DATETIME NOT NULL,
    primaryPosition VARCHAR(2) NOT NULL
);