<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$mysqli = new mysqli($host, $user, $passwd, $db);

$and = "";
$id = "";

$query = "SELECT g.awayTeamId, g.homeTeamId, g.playedStatus, g.id FROM game g inner join team h on h.id = g.homeTeamId inner join team a on a.id = g.awayTeamId WHERE DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) = DATE(DATE_SUB(now(), INTERVAL 6 HOUR)) order by g.startTime asc, g.awayTeamId asc;";


$gameRow = [];
$result = $mysqli->query($query);
while ($row = mysqli_fetch_assoc($result)) {
    $gameRow[] = $row;
}

$rows = [];

foreach ($gameRow as $row) {
    $id = $row["id"];
    $app = "FPPG";
    if ($row["playedStatus"] == "UNPLAYED") {
        $query = "select p.*, round(10*d.fpts/d.gameCount)/10 as statpts from player_season_totals d inner join player p on d.playerId = p.id where (currentTeamId=".$row["awayTeamId"]." or currentTeamId=".$row["homeTeamId"].") order by statpts desc, minSeconds asc, plusMinus desc, fouls asc limit 1;";
    }
    else {
        $query = "select *, fpts as statpts from player_daily d inner join player p on d.playerId = p.id where d.gameId = ".((int)$id)." order by statpts desc, minSeconds asc, plusMinus desc, fouls asc limit 1;";
        $app = "FPTS";
    }
    $result = $mysqli->query($query);
    while ($row = mysqli_fetch_assoc($result)) {
        $row["statpts"] = round($row["statpts"], 2)." ".$app;
        $rows[] = $row;
    }
}

echo json_encode($rows);

?>