<?php
header("Access-Control-Allow-Origin: *");
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];

$conditions = array();

$teamId = "";
if (isset($_GET['teamId'])) {
    $teamId = $_GET['teamId'];
    if (is_numeric($teamId)){
        $sql = "select p.firstName, 
        p.lastName, 
        p.jerseyNumber, 
        p.primaryPosition, 
        p.id, 
        avg(d.pts) as ppg,
        avg(d.offReb)+avg(d.defReb) as rpg,
        avg(d.ast) as apg,
        avg(d.pts)+avg(d.defReb)+avg(d.offReb)+avg(d.ast) as tot
        from daily_player_box_stats d 
        inner join player p on p.id = d.playerId 
        where p.currentTeamId=".((int)$_GET['teamId'])." 
        and p.jerseyNumber <> 'None'
        group by d.playerId
        order by tot desc;";
        $mysqli = new mysqli($host, $user, $passwd, $db);
        $mysqli->query("SET NAMES 'utf8'");
        $result = $mysqli->query($sql);
        $rows = [];
        while ($row = mysqli_fetch_assoc($result)) {
            $rows[] = $row;
        }
        echo json_encode($rows);
        exit(0);
    }
    else {
        echo json_encode("Invalid team id");
        exit(1);
    }
}

$id = "";
if (isset($_GET['id'])) {
    
    $id = $_GET['id'];
    if (is_numeric($id)){
        $conditions[] = " id = ".((int)$_GET['id'])." ";
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}

$lastName = "";
if (isset($_GET['lastName'])) {
    $lastName = $_GET['lastName'];
    $conditions[] = " lastName = '".preg_replace("/[^A-Za-z0-9 ]/", '', $lastName)."' ";
}

$firstName = "";
if (isset($_GET["firstName"])) {
    $firstName = $_GET["firstName"];
    $conditions[] = " firstName = '".preg_replace("/[^A-Za-z0-9 ]/", '', $firstName)."' ";
}


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
$mysqli->query("SET NAMES 'utf8'");
$columns = " * ";
if (isset($_GET["namesOnly"])) {
    $columns = " id, firstName, lastName ";
}

$query = "SELECT ".$columns." FROM player ".$where;
// echo $query."\n";
$result = $mysqli->query($query);
$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>