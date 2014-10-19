<?php

/** 
 * @author Naran
 * 
 */
class Rules {
	
	/**
	 */
	protected  $nonUTFChars = array();
	
	public function __construct() {
		 
	}
	
	public function runRules($string){
		$string =  $this->rule1($string);
		$string = $this->rule2($string);
		$string = $this->rule3($string);
		$string = $this->rule4($string);
		return $string;
	}

	/*
	 * Remove Last "a" Character at end of word and before non utf chars
	 */
	private function rule1($string){
		$nonUTFChars = file("nonIndicChars.txt");
		$replacer = $this->prepareArrayforRule1($nonUTFChars,$nonUTFChars);
		$string = str_replace($replacer['source'], $replacer['target'], $string);
		return $string;
	}
	
	/*
	 * Remove "a" Character before vowel
	 */
	private function rule2($string){
		$vowelsFile = "vowels.csv";
		$replacer = $this->prepareArrayforRule2($vowelsFile);
		$string = str_replace($replacer['source'], $replacer['target'], $string);
		return $string;
	}
	
	/*
	 * Remove special a character for ardhaviram
	*/
	private function rule3($string){
		$vowelsFile = "charRemoval.txt";
		$replacer = $this->prepareArrayforRule3($vowelsFile);
		$string = str_replace($replacer['source'], $replacer['target'], $string);
		return $string;
	}
	
	/*
	 * convert non utf to ascii
	*/
	private function rule4($string){
		$nonUTFChars = file("nonIndicChars.txt");
		$replacer = $this->prepareArrayforRule4($nonUTFChars,$nonUTFChars);
		$string = str_replace($replacer['source'], $replacer['target'], $string);
		return $string;
	}
	
	
	private function prepareArrayforRule4($srcArray,$targetArray){
		//print_r($srcArray);
		for($i=0;$i<count($srcArray);$i++){
			$srcArray[$i] = trim($srcArray[$i]);
			$targetArray[$i] = trim($targetArray[$i]);
			$source[] = "&#".$srcArray[$i].";";
			$target[] = chr($targetArray[$i]);
				
		}
	
		$replacer['source'] = $source;
		$replacer['target'] = $target;
		return $replacer;
	}
	
	private function prepareArrayforRule3($file){
		$charsFile = fopen($file, "r");
		while(($chr=fgetcsv($charsFile))!== false){
				$chrSourceArr[] = "a&#".$chr[0].";";
				$chrTargetArr[] = "";
		}
		fclose($charsFile);
		$replacer['source'] = $chrSourceArr;
		$replacer['target'] = $chrTargetArr;
		return $replacer;
	}
	
	
	private function prepareArrayforRule2($file){
		$charsFile = fopen($file, "r");
		while(($chr=fgetcsv($charsFile))!== false){
			if($chr[1] <> ""){
				$chrSourceArr[] = "a&#".$chr[0].";";
				$chrTargetArr[] = $chr[1];
			}
		}
		fclose($charsFile);
		$replacer['source'] = $chrSourceArr;
		$replacer['target'] = $chrTargetArr;
		return $replacer;
	}
	
	private function prepareArrayforRule1($srcArray,$targetArray){
		//print_r($srcArray);
		for($i=0;$i<count($srcArray);$i++){
			$srcArray[$i] = trim($srcArray[$i]);
			$targetArray[$i] = trim($targetArray[$i]);
			$source[] = "a&#".$srcArray[$i].";";
			$target[] = chr($targetArray[$i]);
			
		}
		
		$replacer['source'] = $source;
		$replacer['target'] = $target;
		return $replacer;
	}
}

?>