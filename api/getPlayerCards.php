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
    // echo "set";
    
    $id = $_GET['teamId'];
    if (is_numeric($id)){

        //pts+ast*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+to*-0.5

        //$query = "select *, (pts+fg3PtMade*0.5+(offReb+defReb)*1.25+ast*1.5+stl*2+blk*2+tov*-0.5) as fpts, (offReb+defReb) as reb from daily_player_box_stats d inner join player p on p.id = d.playerId where DATE(DATE_SUB(now(), INTERVAL 6 HOUR)) = DATE(DATE_SUB(startTime, INTERVAL 6 HOUR)) AND playerTeamId = ".((int)$id)." ORDER BY fpts desc";
        $query = "select p.*, t.abbreviation, r.* from player_ranking r inner join player p on r.playerId = p.id inner join team t on t.id = p.currentTeamId WHERE r.rankingDate = (select max(rankingDate) from player_ranking) AND p.currentTeamId = ".((int)$id)."  order by overallRating desc;";
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
// echo "not set";
$query = "select p.*, t.abbreviation, r.* from player_ranking r inner join player p on r.playerId = p.id inner join team t on t.id = p.currentTeamId WHERE r.rankingDate = (select max(rankingDate) from player_ranking) order by overallRating desc limit 10;";
        
// echo $query;
// exit(0);

$result = $mysqli->query($query);

$rows = [];
while ($row = mysqli_fetch_assoc($result)) {
    $rows[] = $row;
}
echo json_encode($rows);


?>