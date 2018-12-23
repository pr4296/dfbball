<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$conditions = array();

$id = "";
if (isset($_GET['id'])) {
    
    $id = $_GET['id'];
    if (is_numeric($id)){
        $conditions[] = " t.id = ".((int)$_GET['id'])." ";
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}

$teamName = "";
if (isset($_GET['teamName'])) {
    $teamName = $_GET['teamName'];
    $conditions[] = " t.teamName = '".preg_replace("/[^A-Za-z0-9 ]/", '', $teamName)."' ";
}

$city = "";
if (isset($_GET["city"])) {
    $city = $_GET["city"];
    $conditions[] = " t.city = '".preg_replace("/[^A-Za-z0-9 ]/", '', $city)."' ";
}

$conditions[] = " ts.statusDate = (select max(statusDate) from team_standings) ";

$where = "";
// echo json_encode($conditions)."\n";
// echo count($conditions)."\n";
if (count($conditions) > 0) {
    $count = 0;
    foreach ($conditions as $cond) {
        $count .= 1;
        if ($count == 1) {
            $where .= " WHERE ".$cond;
        }
        else {
            $where .=" AND ".$cond;
        }
    }
}

$mysqli = new mysqli($host, $user, $passwd, $db);

$columns = " * ";
if (isset($_GET["namesOnly"])) {
    $columns = " t.id, t.city, t.teamName ";
}

$query = "SELECT ".$columns." FROM team t inner join team_standings ts on t.id = ts.id ".$where;
// echo $query."\n";
$result = $mysqli->query($query);
$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>