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
        $query = "SELECT t.abbreviation, d.*, g.awayScoreTotal, g.homeScoreTotal, g.homeTeamId, g.awayTeamId FROM daily_player_box_stats d inner join team t on d.playerTeamId = t.id inner join game g on g.id = d.gameId WHERE d.playerId = ".((int)$id)." and d.startTime > '2018-08-01 00:00:00'  ORDER BY d.startTime desc";

        // echo $query;
        // exit(0);

        $result = $mysqli->query($query);
        
        $rows = [];
        while ($row = mysqli_fetch_assoc($result)) {
            $rows[] = $row;
        }
        echo json_encode($rows);
    }
    else {
        echo json_encode("Invalid id");
        exit(1);
    }
}

?>
