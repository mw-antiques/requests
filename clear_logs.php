<?php
$logFile = 'requests.txt';

// Clear the log file by truncating it
file_put_contents($logFile, '');

// Return a response indicating success
http_response_code(200);
echo 'Logs cleared successfully';
?>