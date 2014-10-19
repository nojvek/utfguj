<?php

header("Content-Type: text/html; charset=utf-8");
//header("Content-Type: text/plain; charset=utf-8");
include_once 'Rules.php';
include_once 'FnLib.php';
$fnLib = new FnLib();

$dataFile = fopen("ekadashi-guj.txt", "r");
while(($lines[]=fgets($dataFile,4096))!== false){}
fclose($dataFile);

$charsFile = fopen("utf-8 data.csv", "r");
while(($chr=fgetcsv($charsFile))!== false){
	if($chr[1] <> ""){
		$chrSourceArr[] = "&#".$chr[0].";";
		$chrTargetArr[] = $chr[1];
	}
}
fclose($charsFile);

$no_lines = count($lines);

//$no_lines = 5;
for($i=0;$i<$no_lines;$i++){
	echo $lines[$i]."";
	$rules = new Rules();
	$ordLine = "";
	$arr = $fnLib->utf8_str_split($lines[$i]);
	$ordArray = $fnLib->chr2ord($arr);
	foreach ($ordArray as $ordChr){
		$ordLine = $ordLine.$ordChr;
	}
	$newOrdLine = str_replace($chrSourceArr, $chrTargetArr, $ordLine);
	$newOrdLine = $rules->runRules($newOrdLine);

	echo $fnLib->sentence_case($newOrdLine)."\n\n";
}

?>
