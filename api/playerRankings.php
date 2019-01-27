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
if (isset($_GET['teamId'])) {
    
    $id = $_GET['teamId'];
    if (is_numeric($id)){

        $query = "select * from player_ranking r inner join player p on p.id = r.playerId where p.currentTeamId = ".((int)$id);

        $result = $mysqli->query($query);
        
        $rows = [];
        while ($row = mysqli_fetch_assoc($result)) {
            $rows[] = $row;
        }
        echo json_encode($rows);
        exit(0);
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}

$query = "select * from player_ranking r inner join player p on p.id = r.playerId";

$result = $mysqli->query($query);

$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);

?>