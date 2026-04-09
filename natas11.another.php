<?php
function xor_encrypt($in) {
    $key = 'eDWo';
    $text = $in;
    $outText = '';
    for($i = 0; $i < strlen($text); $i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }
    return $outText;
}

$data = array("showpassword"=>"yes", "bgcolor"=>"#ffffff");
echo base64_encode(xor_encrypt(json_encode($data)));
// Output: ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK
?>
