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

$query = "select * from user_picks u where pickDate = DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)) and username = '".$username."';";
$result = $mysqli->query($query);
$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}


if (sizeof($rows) != 5) {
    $d['message'] = "Picks were not found.";
    echo json_encode($d);
    exit(1);
}

$res = [];
for ($i = 0; $i < 5; $i++) {
    $query = "select *, (d.pts+d.fg3PtMade*0.5+(d.offReb+d.defReb)*1.25+d.ast*1.5+d.stl*2+d.blk*2+d.tov*-0.5) as fpts, (d.offReb+d.defReb) as reb from daily_player_box_stats d inner join player p on d.playerId = p.id where d.playerId =".$rows[$i]['playerId']." and DATE(DATE_SUB(d.startTime, INTERVAL 6 HOUR)) = DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR))";
    $result = $mysqli->query($query);

    $t = mysqli_fetch_assoc($result);

    if (!$t) {
        $query = "select * from player p inner join player_season_totals s on p.id = s.playerId where s.playerId =".$rows[$i]["playerId"];
    }

    $result = $mysqli->query($query);
    if (!$result) {
	$d['message'] = "Something went wrong with the query.";
        echo json_encode($d);
        exit(1);
    }

    $row = mysqli_fetch_assoc($result);
    if (!$5) $row["isSeason"] = true;
    else $row["isSeason"] = false;
    $res[] = $row;
}

echo json_encode($res);

?>
