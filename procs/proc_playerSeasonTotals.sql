use basketbrief;

-- insert the new data with the uploadDate timestamp
insert into player_season_totals(playerId, uploadDate, gameCount, fg2PtAtt, fg2PtMade, fg3PtAtt, fg3PtMade, ftAtt, ftMade, offReb, defReb, ast, pts, tov, stl, blk, blkAgainst, fouls, foulsDrawn, foulPers, foulPersDrawn, foulTech, foulTechDrawn, foulFlag1, foulFlag1Drawn, foulFlag2, foulFlag2Drawn, ejections, plusMinus, minSeconds, startedGame, fpts)
select 
    p.id as playerId,
    NOW() as uploadDate,
    count(*) as gameCount,
    sum(d.fg2PtAtt) as fg2PtAtt,
    sum(d.fg2PtMade) as fg2PtMade,
    sum(d.fg3PtAtt) as fg3PtAtt,
    sum(d.fg3PtMade) as fg3PtMade,
    sum(d.ftAtt) as ftAtt,
    sum(d.ftMade) as ftMade,
    sum(d.offReb) as offReb,
    sum(d.defReb) as defReb,
    sum(d.ast) as ast,
    sum(d.pts) as pts,
    sum(d.tov) as tov,
    sum(d.stl) as stl,
    sum(d.blk) as blk,
    sum(d.blkAgainst) as blkAgainst,
    sum(d.fouls) as fouls,
    sum(d.foulsDrawn) as foulsDrawn,
    sum(d.foulPers) as foulPers,
    sum(d.foulPersDrawn) as foulPersDrawn,
    sum(d.foulTech) as foulTech,
    sum(d.foulTechDrawn) as foulTechDrawn,
    sum(d.foulFlag1) as foulFlag1,
    sum(d.foulFlag1Drawn) as foulFlag1Drawn,
    sum(d.foulFlag2) as foulFlag2,
    sum(d.foulFlag2Drawn) as foulFlag2Drawn,
    sum(d.ejections) as ejections,
    sum(d.plusMinus) as plusMinus,
    sum(d.minSeconds) as minSeconds,
    sum(d.startedGame) as startedGame,
    (sum(d.pts)+sum(d.fg3PtMade)*0.5+(sum(d.offReb)+sum(d.defReb))*1.25+sum(d.ast)*1.5+sum(d.stl)*2+sum(d.blk)*2+sum(d.tov)*-0.5) as fpts
    from daily_player_box_stats d 
    inner join player p on p.id = d.playerId 
    inner join game g on g.id = d.gameId
    where d.startTime > '2018-08-01 00:00:00' 
    and d.minSeconds > 0 
    and g.playedStatus = 'COMPLETED'
    group by d.playerId 
    order by fpts desc;

SET @maxDate := (select max(uploadDate) from player_season_totals);
-- delete the old data
delete 
    from player_season_totals 
    where uploadDate != @maxDate;