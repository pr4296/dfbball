<?php
header("Access-Control-Allow-Origin: *");

// make sure username and passwordHash were passed
if (!isset($_GET['username']) || !isset($_GET['passwordHash'])) {
    echo "Invalid data.";
    exit(1);
}

$username = $_GET['username'];
$passwordHash = $_GET['passwordHash'];
$d = [];

// check the validity of the username and password hash
if (!ctype_alnum($username) || strlen($username) < 4 || strlen($username) > 32) {
    $d['message'] = "Invalid username.";
    echo json_encode($d);
    exit(1);
}
if (!ctype_alnum($passwordHash) || strlen($passwordHash) != 64) {
    $d['message'] = "Invalid password.";
    echo json_encode($d);
    exit(1);
}

// generate a salt and the encrypted password 
$salt = bin2hex(openssl_random_pseudo_bytes(32));
$password_encrypted = hash('sha256', $salt.''.$passwordHash);

// connect to database
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$host = $creds['host'];
$user = $creds['user'];
$passwd = $creds['passwd'];
$db = $creds['db'];
$mysqli = new mysqli($host, $user, $passwd, $db);

// insert the new login
$query = "INSERT INTO login_info (username, passwordHash, salt) VALUES ('".$username."', '".$password_encrypted."', '".$salt."')";
$result = $mysqli->query($query);

// make sure the login was inserted correctly
if ($result) {
    $d['message'] = "success";
    echo json_encode($d);
}
else {
    $d['message'] = "That username is unavailable.";
    echo json_encode($d);
}

?>