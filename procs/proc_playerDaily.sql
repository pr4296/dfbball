use basketbrief;

-- insert the new data with the uploadDate timestamp
insert into player_daily(playerId, gameId, startTime, awayTeamAbbreviation, homeTeamAbbreviation, playerTeamId, position, fg2PtAtt, fg2PtMade, fg3PtAtt, fg3PtMade, ftAtt, ftMade, offReb, defReb, ast, pts, tov, stl, blk, blkAgainst, fouls, foulsDrawn, foulPers, foulPersDrawn, foulTech, foulTechDrawn, foulFlag1, foulFlag1Drawn, foulFlag2, foulFlag2Drawn, ejections, plusMinus, minSeconds, startedGame, uploadDate, fpts)
select 
    *, 
    NOW() as uploadDate,
    (pts+fg3PtMade*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+tov*-0.5) as fpts
    from daily_player_box_stats d 
    where DATE(DATE_SUB(now(), INTERVAL 6 HOUR)) = DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) 
    ORDER BY fpts desc, minSeconds asc, plusMinus desc, fouls asc;

SET @maxDate := (select max(uploadDate) from player_daily);
-- delete the old data
delete 
    from player_daily 
    where uploadDate != @maxDate;