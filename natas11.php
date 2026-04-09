<?php
$cookie = base64_decode("HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=");
$known_plaintext = json_encode(array("showpassword"=>"no", "bgcolor"=>"#ffffff"));

$key = '';
for($i = 0; $i < strlen($cookie); $i++) {
    $key .= $cookie[$i] ^ $known_plaintext[$i % strlen($known_plaintext)];
}
echo $key;
// Output: qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq
// The repeating pattern → KEY = "qw8J"
?>
