<?php

$nodecode = '';

header ('Content-Type: text/plain; charset=utf-8');

$q = $_GET['q'];

$opts = explode('/',$q);

function fe($s) { return preg_replace("/[^a-z0-9!_.-]+/", "", $s); }
function fm($s) { return preg_replace("/[^a-zA-Z0-9]+/", "", $s);   }


function getmsg($t) { return @file_get_contents ("msg/" . fm($t)); }
function getecho($t) { return @file_get_contents ("echo/" . fe($t)); }

function savemsg($h,$e,$t) {
$fp = fopen('msg/' . fm($h), 'wb'); fwrite($fp, $t); fclose($fp);
$fp = fopen('echo/' . fe($e), 'ab'); fwrite($fp, "$h\n"); fclose($fp);
}


if (!empty($_POST['upush'])) {
$upush = $_POST['upush']; $nauth = $_POST['nauth']; $echoarea = $_POST['echoarea'];
if ($auth != $nodecode) { die('auth error'); }
$lines = explode("\n",$upush);

for ($x=0;$x<count($lines);$x++) {
$a = explode(":",$lines[$x]);
savemsg($a[0],$echoarea,base64_decode($a[1]));
}
} # upush


if ($opts[1] == 'e') {
echo getecho($opts[2]);
} # e

if ($opts[1] == 'm') {
echo getmsg($opts[2]);
} # m

if ($opts[1] == 'u' and $opts[2] == 'm') {
for ($x=3;$x<count($opts);$x++) { 
$hash = base64_encode(getmsg($opts[$x]));
echo "$opts[$x]:$hash\n";
}
} # um

if ($opts[1] == 'u' and $opts[2] == 'e') {
for ($x=3;$x<count($opts);$x++) { 
echo $opts[$x] . "\n";
echo getecho($opts[$x]);
}
} # ue

?>