Zadanie projektu:

Triviální distribuovaný souborový systém

Cílem projektu je implementovat klienta pro triviální (read-only) distribuovaný souborový systém. Tento systém používá zjednodušenou verzi URL pro identifikaci souborů a jejich umístění. Systém pro přístup k souborům používá File Service Protocol (FSP). V projektu bude stačit implementovat pouze jeden typ požadavku, kterým je příkaz GET. Systém používá symbolických jmen, které jsou překládány na IP adresy pomocí protokolu Name Service Protocol (NSP). Tento protokol umožňuje získat IP adresu a číslo portu, kde daný souborový server běží.

Specifikace protokolů a detailní popis požadavků na implementaci naleznete na uvedeném URL. 

Klient bude nazván fileget, popřípadě fileget.py.