<?php
header("Access-Control-Allow-Origin: *");

// make sure username and passwordHash were passed
if (!isset($_GET['username']) || !isset($_GET['passwordHash'])) {
    echo "invalid data.";
    exit(1);
}

$username = $_GET['username'];
$passwordHash = $_GET['passwordHash'];

// response object
$d = [];

// check the validity of the username and password hash
if (!ctype_alnum($username) || strlen($username) < 4 || strlen($username) > 32) {
    $d['message'] = "invalid username";
    echo json_encode($d);
    exit(1);
}
if (!ctype_alnum($passwordHash) || strlen($passwordHash) != 64) {
    $d['message'] = "invalid password hash";
    echo json_encode($d);
    exit(1);
}

// generate a salt and the encrypted password 
$salt = bin2hex(openssl_random_pseudo_bytes(32));
$password_encrypted = hash('sha256', $salt.''.$passwordHash);

// connect to database
$creds = json_decode(file_get_contents('../auth/mysql_auth.json'), true);
$mysqli = new mysqli($creds['host'], $creds['user'], $creds['passwd'], $creds['db']);

// insert the new login
$query = "SELECT passwordHash, salt from login_info where username = '".$username."'";
$result = $mysqli->query($query);
$row = mysqli_fetch_assoc($result);
$ph = $row['passwordHash'];
$salt = $row['salt'];
if (hash('sha256', $salt.$passwordHash) == $ph) {
    // correct log in
    // generate a token and send it to the user
    $token = bin2hex(openssl_random_pseudo_bytes(16));

    $query = "INSERT INTO login_token (username, token) VALUES ('".$username."', '".$token."')";
    $result = $mysqli->query($query);

    if ($result) {
        $d['message'] = "successful login";
        $d['token'] = $token;
        echo json_encode($d);
	exit(0);
    }
    else {
        $d['message'] = "something went wrong while generating a token";
        echo json_encode($d);
	exit(1);
    }
}

echo json_encode("Invalid login.");
exit(1);
?>
