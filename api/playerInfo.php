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
        $query = "SELECT p.*, t.abbreviation from player p inner join team t on p.currentTeamId = t.id WHERE p.id = ".((int)$id);

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