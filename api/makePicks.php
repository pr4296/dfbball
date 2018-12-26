<?php
header("Access-Control-Allow-Origin: *");

// make sure username and passwordHash were passed
if (!isset($_GET['username']) || !isset($_GET['token']) || !isset($_GET['PG']) || !isset($_GET['SG']) || !isset($_GET['SF']) || !isset($_GET['PF']) || !isset($_GET['C'])) {
    $d['message'] = "Invalid data.";
    echo json_encode($d);
    exit(1);
}

$username = $_GET['username'];
$token = $_GET['token'];
$pg_id = $_GET['PG'];
$sg_id = $_GET['SG'];
$sf_id = $_GET['SF'];
$pf_id = $_GET['PF'];
$c_id = $_GET['C'];
$d = [];

if (!ctype_alnum($pg_id) || !ctype_alnum($sg_id) || !ctype_alnum($sf_id) || !ctype_alnum($pf_id) || !ctype_alnum($c_id)) {
    $d['message'] = "Invalid picks.";
    echo json_encode($d);
    exit(1);
}


// check the validity of the username and password hash
if (!ctype_alnum($token) || !ctype_alnum($username)) {
    $d['message'] = "Invalid parameters.";
    echo json_encode($d);
    exit(1);
}

$query = "SELECT * FROM login_token where username='".$username."' and token='".$token."';";

// connect to database
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$mysqli = new mysqli($creds['host'], $creds['user'], $creds['passwd'], $creds['db']);

$result = $mysqli->query($query);
if (!$result) {
    $d['message'] = "Invalid username or token.";
    echo json_encode($d);
    exit(1);
}
$row = mysqli_fetch_assoc($result);
if (!$row) {
    $d['message'] = "Invalid username or token.";
    echo json_encode($d);
    exit(1);
}



$query = "DELETE FROM user_picks where username = '".$username."' and pickDate = DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR))";
$result = $mysqli->query($query);
if (!result) {
    $d['message'] = "Error trying to clear existing picks.";
    echo json_encode($d);
    exit(1);
}

$query = "INSERT INTO user_picks (username, pickDate, playerId) VALUES ";
$query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$pg_id."')";
$query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$sg_id."')";
$query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$sf_id."')";
$query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$pf_id."')";
$query .= "('".$username."', DATE(DATE_SUB(NOW(), INTERVAL 6 HOUR)), '".$c_id."')";
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