<?php
$dir = isset($_GET['dir']) ? $_GET['dir'] : '.';
echo "<pre>";
print_r(scandir($dir));
echo "</pre>";
?>
