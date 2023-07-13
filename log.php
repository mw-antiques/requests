<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

$logFile = 'requests.txt';

$method = $_SERVER['REQUEST_METHOD'];
$uri = $_SERVER['REQUEST_URI'];
$queryString = $_SERVER['QUERY_STRING'];
$loggedParams = $uri . '?' . $queryString;
$ip = $_SERVER['REMOTE_ADDR'];

// Log the request to the file
file_put_contents($logFile, "$method $loggedParams [IP: $ip]\n", FILE_APPEND);

// Alert the logged parameters
echo "<script>alert('ATTACKER SUCCESSFULLY LOGGED YOUR IP AND: " . htmlspecialchars($loggedParams, ENT_QUOTES) . "');</script>";

echo "Log file written:";
?>
