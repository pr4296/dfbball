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

        //pts+ast*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+to*-0.5

        $query = "select * from player_daily d inner join player p on p.id = d.playerId inner join team t on t.id = d.playerTeamId where playerTeamId = ".((int)$id)." ORDER BY fpts desc, minSeconds asc, plusMinus desc, fouls asc limit 10";

        // echo $query;
        // exit(0);

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

$query = "select * from player_daily d inner join player p on p.id = d.playerId inner join team t on t.id = d.playerTeamId ORDER BY fpts desc, minSeconds asc, plusMinus desc, fouls asc limit 10";

// echo $query;
// exit(0);

$result = $mysqli->query($query);

$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);


?>