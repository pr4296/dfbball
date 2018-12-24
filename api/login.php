<?php
header("Access-Control-Allow-Origin: *");

// make sure username and passwordHash were passed
if (!isset($_GET['username']) || !isset($_GET['passwordHash'])) {
    echo "invalid data.";
    exit(1);
}

$username = $_GET['username'];
$passwordHash = $_GET['passwordHash'];

// check the validity of the username and password hash
if (!ctype_alnum($username) || strlen($username) < 4 || strlen($username) > 32) {
    echo "invalid username";
    exit(1);
}
if (!ctype_alnum($passwordHash) || strlen($passwordHash) != 64) {
    echo "invalid password hash";
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
$query = "SELECT passwordHash, salt from login_info where username = '".$username+"'";
$result = $mysqli->query($query);
$row = mysqli_fetch_assoc($result);
$ph = $row['passwordHash'];
$salt = $row['salt'];
if (hash('256', $salt+$passwordHash) == $ph) {
    // correct log in
    // generate a token and send it to the user
    $token = bin2hex(openssl_random_pseudo_bytes(32));
    $dict = [];
    $dict['token'] = $token;

    echo json_encode($dict);
    exit(0);
}

echo json_encode("Invalid login");
exit(1);
?>