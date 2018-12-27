<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$mysqli = new mysqli($host, $user, $passwd, $db);
$username = $_GET['username'];

$d = [];

if (!ctype_alnum($username)) {
    $d['message'] = "Invalid username.";
    echo json_encode($d);
    exit(1);
}

$query = "select * from user_picks u inner join player p on p.id = u.playerId inner join daily_player_box_stats d on d.playerId = u.playerId where DATE(DATE_SUB(d.startTime, INTERVAL 6 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 7 HOUR)) and pickDate = DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)) and username = '".$username."';";

$result = $mysqli->query($query);

$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>