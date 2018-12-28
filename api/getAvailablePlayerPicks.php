<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$mysqli = new mysqli($host, $user, $passwd, $db);

$query = "select p.firstName, p.lastName, pst.* from available_players a inner join player p on a.playerId = p.id inner join player_season_totals pst on a.playerId = pst.playerId order by fpts desc;";
//echo $query."</br>";

$result = $mysqli->query($query);

$rows = [];
$count = 0;
echo "[";
while ($row = mysqli_fetch_assoc($result)) {
    if ($count > 0) echo ",";
    echo json_encode($row);
    $count++;
}
echo "]";
//echo json_encode($rows);

?>
