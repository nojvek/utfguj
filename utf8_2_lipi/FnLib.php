<?php

/** 
 * @author Naran
 * 
 */
class FnLib {
	
	/**
	 */
	function __construct() {
	}
	


	function sentence_case($string) {
		$sentences = preg_split('/([.?!]+)/', $string, -1, PREG_SPLIT_NO_EMPTY|PREG_SPLIT_DELIM_CAPTURE);
		$new_string = '';
		foreach ($sentences as $key => $sentence) {
			$new_string .= ($key & 1) == 0?
			ucfirst(strtolower(trim($sentence))) :
			$sentence.' ';
		}
		return trim($new_string);
	}
	
	function chr2ord($array){
		$ordArray = array();
		foreach($array as $chr){
			$uniord = $this->uniord($chr);
			if($uniord<=50000){
				$ordArray[] = "&#".$uniord.";";
			}
		}
		return $ordArray;
	}
	
	function utf8_str_split($str='',$len=1){
		preg_match_all("/./u", $str, $arr);
		$arr = array_chunk($arr[0], $len);
		$arr = array_map('implode', $arr);
		return $arr;
	}
	
	
	function uniord($c) {
		$h = ord($c{0});
		if ($h <= 0x7F) {
			return $h;
		} else if ($h < 0xC2) {
			return false;
		} else if ($h <= 0xDF) {
			return ($h & 0x1F) << 6 | (ord($c{1}) & 0x3F);
		} else if ($h <= 0xEF) {
			return ($h & 0x0F) << 12 | (ord($c{1}) & 0x3F) << 6
			| (ord($c{2}) & 0x3F);
		} else if ($h <= 0xF4) {
			return ($h & 0x0F) << 18 | (ord($c{1}) & 0x3F) << 12
			| (ord($c{2}) & 0x3F) << 6
			| (ord($c{3}) & 0x3F);
		} else {
			return false;
		}
	}
	
}

?>