Projekty:

parse.php

Skript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPP-code21, zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní výstup XML reprezentaci programu dle specifikace.


interpret.py

Skript (interpret.py v jazyce Python 3.8) načte XML reprezentaci programu a tento program s využitím vstupu dle parametrů příkazové řádky interpretuje a generuje výstup. Vstupní XML reprezentace je např. generována skriptem parse.php (ale ne nutně, takže může obsahovat chyby) ze zdrojového kódu v IPPcode21. Interpret navíc podporuje existenci volitelných dokumentačních textových atributů name a description v kořenovém elementu program. Sémantika jednotlivých instrukcí IPPcode21 je popsána v sekci 6 v specifikaci. Interpretace instrukcí probíhá dle atributu order vzestupně (sekvence nemusí být souvislá).