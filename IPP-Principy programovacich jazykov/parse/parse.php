<?php
//autor: Miroslav Filas
//login: xfilas00

ini_set('display_errors', 'stderr');

//spracovanie vstupnych argumentov
if($argc == 2 && $argv[1] == "--help"){
    echo "pouzite: php7.4 parse.php < vstupnySubor > vystupnySubor\n";
    exit(0);
} else if($argc > 1) {
    exit(10);
}

$xw = xmlwriter_open_memory();

xmlwriter_set_indent($xw, 1); 
xmlwriter_start_document($xw, '1.0', 'UTF-8');

$validHeader = false;
//kontrola ci existuje .IPPcode21 hlavicka a nachadza sa pred instrukciami 
while($header = fgets(STDIN)) {
    $header = preg_replace('/#.*/', "", $header); //odstranenie komentarov
    $header = trim($header);
    if($header == ""){
        continue;
    }
    else if(strtoupper($header) == ".IPPCODE21"){
        xmlwriter_start_element($xw, "program");
        xmlwriter_start_attribute($xw, "language");
        xmlwriter_text($xw, "IPPcode21");
        xmlwriter_end_attribute($xw);
        $validHeader = true;
        break;
    } else {
        exit(21);
    }
}

if(!$validHeader) {
    exit(21);
}


$order = 1;
//spracovanie instrukcii a ich argumentov
while($input = fgets(STDIN)){
    $text = preg_replace('/#.*/', "", $input); //odstranenie komentarov
    $text = preg_replace('/\s+/', " ", $text); //nahradenie whitespace medzi argumentami za jednu medzeru
    $text = explode(" ", trim($text)); //odstranenie \n + whitespace z konca riadku a rozdelenie vstupneho textu na celky oddelene medzerou
    $opcode = strtoupper($text[0]);
    switch($opcode) {
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            if(count($text) != 1) {
                exit(23);
            }
            instruction();
            
            xmlwriter_end_element($xw);
            break;
        case "DEFVAR":
        case "POPS":
            if(count($text) != 2) {
                exit(23);
            }
            instruction();
            checkVar($text[1], 1);

            xmlwriter_end_element($xw);
            break;
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            if(count($text) != 2) {
                exit(23);
            }
            instruction();
            checkSymb($text[1], 1);

            xmlwriter_end_element($xw);
            break;
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            if(count($text) != 4) {
                exit(23);
            }
            instruction();
            checkVar($text[1], 1);
            checkSymb($text[2], 2);
            checkSymb($text[3], 3);

            xmlwriter_end_element($xw);
            break;
        case "READ":
            if(count($text) != 3) {
                exit(23);
            }
            instruction();
            checkVar($text[1], 1);
            checkType($text[2], 2);

            xmlwriter_end_element($xw);
            break;
        case "STRLEN":
        case "TYPE":
        case "INT2CHAR":
        case "MOVE":
        case "NOT":
            if(count($text) != 3) {
                exit(23);
            }
            instruction();
            checkVar($text[1], 1);
            checkSymb($text[2], 2);
            
            xmlwriter_end_element($xw);
            break;
        case "LABEL":
        case "JUMP":
        case "CALL":
            if(count($text) != 2) {
                exit(23);
            }
            instruction();
            checkLabel($text[1], 1);

            xmlwriter_end_element($xw);
            break;
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            if(count($text) != 4) {
                exit(23);
            }
            instruction();
            checkLabel($text[1], 1);
            checkSymb($text[2], 2);
            checkSymb($text[3], 3);

            xmlwriter_end_element($xw);
            break;

        case "": //prazdny riadok/riadok s komentarom preskoci
            if(count($text) != 1) {
                exit(22);
            }
            break;
        default:
            //chybny operacny kod
            exit(22);
            break;
    }
}


//koniec xml elementu <program>
xmlwriter_end_element($xw);
//vypisanie vytvoreneho xml na stdout
echo xmlwriter_output_memory($xw);
exit(0);

//pomocne funkcie:

//kontrola ci sa <var> sklada iba z povolenych znakov a je v spravnom formate
//$argNum = poradie argumentu
//$name = string ktory sa kontroluje ci odpoveda <var>
function checkVar ($name, $argNum){
    $valid = preg_match('/^(LF|TF|GF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $name);
    if(!$valid){
        exit(23);
    }

    arguments ($argNum, "var", $name);
}

//kontrola ci sa <symb> sklada iba z povolenych znakov a je v spravnom formate
//$argNum = poradie argumentu
//$name = string ktory sa kontroluje ci odpoveda <symb>
function checkSymb ($name, $argNum){
    
    if(preg_match('/^int@[+-]?[0-9]+$/', $name)){
       $name = preg_replace('/int@/', "", $name);
        arguments ($argNum, "int", $name);

    } else if(preg_match('/^bool@(true|false)$/', $name)){
        $name =  preg_replace('/bool@/', "", $name);
        arguments ($argNum, "bool", $name);

    } else if(preg_match('/^nil@nil$/', $name)){
        $name =  preg_replace('/nil@/', "", $name);
        arguments ($argNum, "nil", $name);

    } else if(preg_match('/^string@/', $name)){
        $name =  preg_replace('/string@/', "", $name);
        checkString($name, $argNum);
       

    } else if(preg_match('/^(LF|TF|GF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $name)){

        arguments ($argNum, "var", $name);

    } else {
        exit(23);
    }
}

//kontrola ci sa <string> sklada iba z povolenych znakov a je v spravnom formate
//$argNum = poradie argumentu
//$name = string ktory sa kontroluje ci odpoveda <string>
function checkString ($string, $argNum) {
    //kontrola ci su ciselne sekvencie zacianjuce s \ v spravnom formate a nenachadza sa v string \ samostatne 
    if(preg_match_all('/\\\/', $string) == preg_match_all('/\\\[0-9][0-9][0-9]/', $string)){ //pocet \ odpoveda poctu \ciselnych sekvencii

        arguments ($argNum, "string", $string);
    } else {
        exit(23);
    }
    
}

//kontrola ci sa <label> sklada iba z povolenych znakov a je v spravnom formate
//$argNum = poradie argumentu
//$name = string ktory sa kontroluje ci odpoveda <label>
function checkLabel ($name, $argNum){
    if(preg_match('/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $name)){
        arguments($argNum, "label", $name);
    } else {
        exit(23);
    }
}

//kontrola ci sa <type> sklada iba z povolenych znakov a je v spravnom formate
//$argNum = poradie argumentu
//$name = string ktory sa kontroluje ci odpoveda <type>
function checkType ($name, $argNum) {
    if(preg_match('/^(int|string|bool)$/', $name)){
        arguments ($argNum, "type", $name);
    } else {
        exit(23);
    }
 
}


//funkcia generuje xml kod pre instrukcie
function instruction (){
    global $xw;
    global $order;
    global $opcode;

    xmlwriter_start_element($xw, "instruction");

    xmlwriter_start_attribute($xw, "order");
    xmlwriter_text($xw, "$order");
    xmlwriter_end_attribute($xw);

    xmlwriter_start_attribute($xw, "opcode");
    xmlwriter_text($xw, "$opcode");
    xmlwriter_end_attribute($xw);

    $order++;
}

//funkcia generuje xml kod pre argumenty
function arguments ($argNum, $type, $name){
    global $xw;

    xmlwriter_start_element($xw, "arg$argNum");

    xmlwriter_start_attribute($xw, "type");
    xmlwriter_text($xw, "$type");
    xmlwriter_end_attribute($xw);

    xmlwriter_text($xw, "$name");

    xmlwriter_end_element($xw); 
}

?>