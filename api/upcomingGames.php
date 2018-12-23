<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$mysqli = new mysqli($host, $user, $passwd, $db);

$and = "";
$id = "";
if (isset($_GET['id'])) {
    
    $id = $_GET['id'];
    if (is_numeric($id)){
        $and = "AND (awayTeamId = ".((int)$id)." OR homeTeamId = ".((int)$id).") ";
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}

$numRows = "";
if (isset($_GET['numRows'])) {
    $numRows = $_GET['numRows'];
    if (is_numeric($numRows)){
        $and = ((int)$numRows)." = ".((int)$id);
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}
else {
    $numRows = 5;
}

$query = "SELECT * FROM game WHERE startTime > DATE_SUB(now(), INTERVAL 24 HOUR)  ".$and." AND playedStatus='UNPLAYED' ORDER BY startTime asc, awayTeamId asc limit ".$numRows;
// echo $query."\n";
$result = $mysqli->query($query);
$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>