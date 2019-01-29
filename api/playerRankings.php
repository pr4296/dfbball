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

        $query = "select p.firstName, p.lastName, p.imgUrl, r.*, t.abbreviation, pst.* from player_ranking r inner join player p on p.id = r.playerId inner join team t on t.id = p.currentTeamId inner join player_season_totals pst on pst.playerId = p.id where p.currentTeamId = ".((int)$id)+" and uploadDate = (select max(uploadDate) from player_ranking)";

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

$query = "select p.firstName, p.lastName, p.imgUrl, r.*, t.abbreviation, pst.* from player_ranking r inner join player p on p.id = r.playerId inner join team t on t.id = p.currentTeamId inner join player_season_totals pst on pst.playerId = p.id where uploadDate = (select max(uploadDate) from player_ranking)";
$result = $mysqli->query($query);

$rows = [];
$count = 0;
$s = "[";
while ($row = mysqli_fetch_assoc($result)) {
    $r = json_encode($row);
    if (strlen($r) > 0 && $count > 0) $s .=", ";
    $s .= $r;
    $count++;
}
$s .= "]";
echo $s;
?>
