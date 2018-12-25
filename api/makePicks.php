<?php
header("Access-Control-Allow-Origin: *");

// make sure username and passwordHash were passed
if (!isset($_GET['username']) || !isset($_GET['passwordHash'])) {
    echo "Invalid data.";
    exit(1);
}

$username = $_GET['username'];
$token = $_GET['token'];
$arr = $_GET['arrPlayerIds'];
$d = [];

if (!json_decode($arr)) {
    $d['message'] = "Invalid playerid array.";
    echo json_encode($d);
    exit(1);
}

$arr = json_decode($arr);

for ($i = 0; $i < 5; $i++) {
    if (!ctype_alnum($arr[$i])) {
        $d['message'] = "Invalid playerid array.";
        echo json_encode($d);
        exit(1);
    }
}

// check the validity of the username and password hash
if (!ctype_alnum($token) || !ctype_alnum($username) || strlen($$token) < 4 || sizeof(json_decode($arr)) == 0) {
    $d['message'] = "Invalid parameters.";
    echo json_encode($d);
    exit(1);
}

$query = "SELECT * FROM login_token where username='".$username."' and token='".$token."';";
$result = $mysqli->query($query);
$row = mysqli_fetch_assoc($result);
if (!$row) {
    $d['message'] = "Invalid token.";
    echo json_encode($d);
    exit(1);
}

// connect to database
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$mysqli = new mysqli($creds['host'], $creds['user'], $creds['passwd'], $creds['db']);

$query = "DELETE FROM user_picks where username = '".$username."' and pickDate = DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR))";
$result = $mysqli->query($query);
if (!result) {
    $d['message'] = "Error trying to clear existing picks.";
    echo json_encode($d);
    exit(1);
}

$query = "INSERT INTO user_picks (username, pickDate, playerId) VALUES ";
for ($i = 0; $i < 5; $i++) {
    $query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$arr[$i]."')";
    if ($i < 4) {
        $query .=",";
    }
}
$query .=";";

$result = $mysqli->query($query);
// make sure the picks were made correctly
if ($result) {
    $d['message'] = "success";
    echo json_encode($d);
}
else {
    $d['message'] = "User picks were not saved.";
    echo json_encode($d);
}
?>