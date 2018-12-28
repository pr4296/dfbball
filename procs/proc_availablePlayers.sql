use basketbrief;

-- insert the new data with the uploadDate timestamp
insert into available_players(uploadDate, playerId, primaryPosition)
select 
    NOW() as uploadDate,
    playerId, 
    primaryPosition 
    from player_season_totals pst 
    inner join player p 
        on p.id = pst.playerId 
    where p.currentTeamId in (
        select awayTeamId as teamId 
            from game 
            where DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) = DATE(DATE_SUB((select min(startTime) from game where playedStatus = 'UNPLAYED'), INTERVAL 6 HOUR)) 
        union 
        select homeTeamId as teamId 
            from game 
            where DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) = DATE(DATE_SUB((select min(startTime) from game where playedStatus = 'UNPLAYED'), INTERVAL 6 HOUR)));

SET @maxDate := (select max(uploadDate) from available_players);
-- delete the old data
delete 
    from available_players 
    where uploadDate != @maxDate;