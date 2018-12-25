<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$mysqli = new mysqli($host, $user, $passwd, $db);

$query = "select * from available_players a inner join player p on a.playerId = p.id inner join player_season_totals pst on a.playerId = pst.playerId order by fpts desc;";

$result = $mysqli->query($query);

$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>