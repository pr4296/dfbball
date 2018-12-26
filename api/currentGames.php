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

$dayDiff = $_GET['dayDiff'];
if (!is_numeric($dayDiff)) {
    echo json_encode("Invalid day difference. Must be an integer.");
}

$query = "SELECT h.teamName as homeTeamName, h.city as homeCity, a.teamName as awayTeamName, a.city as awayCity, g.* FROM game g inner join team h on h.id = g.homeTeamId inner join team a on a.id = g.awayTeamId WHERE DATE(DATE_SUB(startTime, INTERVAL 6 HOUR) = DATE(DATE_SUB(now(), INTERVAL 6+24*(".$dayDiff.") HOUR))  ".$and." ORDER BY startTime asc, awayTeamId asc";
// echo $query."\n";
$result = $mysqli->query($query);
$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>