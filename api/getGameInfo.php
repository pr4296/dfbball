<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$id = $_GET['id'];

if (!ctype_alnum($id)) {
    echo "Invalid game id.";
}

$res = [];

$mysqli = new mysqli($host, $user, $passwd, $db);

$query = "select *, a.city as awayCity, a.teamName as awayTeamName, h.city as homeCity, h.teamName as homeTeamName from game g inner join team a on a.id = g.awayTeamId inner join team h on h.id = g.homeTeamId where g.id = ".$id.";";
//echo $query."</br>";

$result = $mysqli->query($query);

$rows = [];
$row = mysqli_fetch_assoc($result);
$res["gameInfo"] = $row;

$query = "select *, (pts+fg3PtMade*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+tov*-0.5) as fpts from daily_player_box_stats d inner join player p on p.id = d.playerId inner join team t on t.id = d.playerTeamId where gameId = ".$id." and d.minSeconds > 0 order by fpts desc;";

$result = $mysqli->query($query);

$rows2 = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows2[] = $row;
}

$res["players"] = $rows2;

echo json_encode($res);

?>
