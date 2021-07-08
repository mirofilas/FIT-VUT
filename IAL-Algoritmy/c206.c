
/* c206.c **********************************************************}
{* Téma: Dvousměrně vázaný lineární seznam
**
**                   Návrh a referenční implementace: Bohuslav Křena, říjen 2001
**                            Přepracované do jazyka C: Martin Tuček, říjen 2004
**                                            Úpravy: Kamil Jeřábek, září 2020
**
** Implementujte abstraktní datový typ dvousměrně vázaný lineární seznam.
** Užitečným obsahem prvku seznamu je hodnota typu int.
** Seznam bude jako datová abstrakce reprezentován proměnnou
** typu tDLList (DL znamená Double-Linked a slouží pro odlišení
** jmen konstant, typů a funkcí od jmen u jednosměrně vázaného lineárního
** seznamu). Definici konstant a typů naleznete v hlavičkovém souboru c206.h.
**
** Vaším úkolem je implementovat následující operace, které spolu
** s výše uvedenou datovou částí abstrakce tvoří abstraktní datový typ
** obousměrně vázaný lineární seznam:
**
**      DLInitList ...... inicializace seznamu před prvním použitím,
**      DLDisposeList ... zrušení všech prvků seznamu,
**      DLInsertFirst ... vložení prvku na začátek seznamu,
**      DLInsertLast .... vložení prvku na konec seznamu,
**      DLFirst ......... nastavení aktivity na první prvek,
**      DLLast .......... nastavení aktivity na poslední prvek,
**      DLCopyFirst ..... vrací hodnotu prvního prvku,
**      DLCopyLast ...... vrací hodnotu posledního prvku,
**      DLDeleteFirst ... zruší první prvek seznamu,
**      DLDeleteLast .... zruší poslední prvek seznamu,
**      DLPostDelete .... ruší prvek za aktivním prvkem,
**      DLPreDelete ..... ruší prvek před aktivním prvkem,
**      DLPostInsert .... vloží nový prvek za aktivní prvek seznamu,
**      DLPreInsert ..... vloží nový prvek před aktivní prvek seznamu,
**      DLCopy .......... vrací hodnotu aktivního prvku,
**      DLActualize ..... přepíše obsah aktivního prvku novou hodnotou,
**      DLPred .......... posune aktivitu na předchozí prvek seznamu,
**      DLSucc .......... posune aktivitu na další prvek seznamu,
**      DLActive ........ zjišťuje aktivitu seznamu.
**
** Při implementaci jednotlivých funkcí nevolejte žádnou z funkcí
** implementovaných v rámci tohoto příkladu, není-li u funkce
** explicitně uvedeno něco jiného.
**
** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam 
** předá někdo jako parametr hodnotu NULL.
**
** Svou implementaci vhodně komentujte!
**
** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
** Proto zde používáme pojem funkce i pro operace, které by byly
** v algoritmickém jazyce Pascalovského typu implemenovány jako
** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
**/

#include "c206.h"

int solved;
int errflg;

void DLError() {
/*
** Vytiskne upozornění na to, že došlo k chybě.
** Tato funkce bude volána z některých dále implementovaných operací.
**/	
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;             /* globální proměnná -- příznak ošetření chyby */
    return;
}

void DLInitList (tDLList *L) {
/*
** Provede inicializaci seznamu L před jeho prvním použitím (tzn. žádná
** z následujících funkcí nebude volána nad neinicializovaným seznamem).
** Tato inicializace se nikdy nebude provádět nad již inicializovaným
** seznamem, a proto tuto možnost neošetřujte. Vždy předpokládejte,
** že neinicializované proměnné mají nedefinovanou hodnotu.
**/
    L->First = NULL;
    L->Last = NULL;
    L->Act = NULL;
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLDisposeList (tDLList *L) {
/*
** Zruší všechny prvky seznamu L a uvede seznam do stavu, v jakém
** se nacházel po inicializaci. Rušené prvky seznamu budou korektně
** uvolněny voláním operace free. 
**/
    //free predtym
	tDLElemPtr tmp, next;
    if(L == NULL) {
        return;
    }
    tmp = L->First;
    while(tmp != NULL) {
        next = tmp->rptr; 
        free(tmp);
        tmp = next;
    }

	L->First = NULL;
    L->Last = NULL;
    L->Act = NULL;
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLInsertFirst (tDLList *L, int val) {
/*
** Vloží nový prvek na začátek seznamu L.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	tDLElemPtr ptr = malloc(sizeof(struct tDLElem));
	if(ptr == NULL) { //kontrola uspesnosti malloc
        DLError();
        return;
    }
    ptr->data = val;
    ptr->lptr = NULL;
    ptr->rptr = L->First;
    if(L->First != NULL) { //pokial nie je prazdny zoznam tak prvy bude dolava od povodneho prveho
        L->First->lptr = ptr;  
    } else {
        L->Last = ptr; //pokial je prazdny tak bude prvok prvy aj posledny
    }
    L->First = ptr;

 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLInsertLast(tDLList *L, int val) {
/*
** Vloží nový prvek na konec seznamu L (symetrická operace k DLInsertFirst).
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/ 	
	tDLElemPtr ptr = malloc(sizeof(struct tDLElem));
	if(ptr == NULL) { //kontrola uspesnosti malloc
        DLError();
        return;
    }
    ptr->data = val;
    ptr->rptr = NULL;
    ptr->lptr = L->Last;
    if(L->Last != NULL) {
        L->Last->rptr = ptr; //neprazdny zoznam => novy ptr bude doprava od povodneho posledneho

    } else {
        L->First = ptr; //prazdny zoznam, prvok bude aj prvy aj posledny
    }
    L->Last = ptr;
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLFirst (tDLList *L) {
/*
** Nastaví aktivitu na první prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
	L->Act = L->First;
    return;

 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLLast (tDLList *L) {
/*
** Nastaví aktivitu na poslední prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
	L->Act = L->Last;
    return;
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLCopyFirst (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/

    if(L == NULL || L->First == NULL) {
        DLError();
        return;
    } else {
        *val = L->First->data;
    }
	
	
// solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLCopyLast (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu posledního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/
	
    if(L == NULL || L->Last == NULL) {
        DLError();
        return;
    } else {
        *val = L->Last->data;
    }
	
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLDeleteFirst (tDLList *L) {
/*
** Zruší první prvek seznamu L. Pokud byl první prvek aktivní, aktivita 
** se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
**/
	tDLElemPtr ptr;
    if(L->First != NULL) {
        ptr = L->First;
        if(L->Act == L->First) { //prvy prvok bol aktivny
            L->Act = NULL;  //zrusi sa aktivita
        }
        if(L->First == L->Last) { //zoznam mal iba jeden prvok, vynuluje sa
            L->First = NULL;
            L->Last = NULL;
        } else {
            L->First = L->First->rptr; //zmeni sa zaciatok zoznamu, posunie sa o jeden doprava
            L->First->lptr = NULL; //novemu zaciatku sa nastavi lavy ptr na NULL
        }
        free(ptr);
    }


	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}	

void DLDeleteLast (tDLList *L) {
/*
** Zruší poslední prvek seznamu L.
** Pokud byl poslední prvek aktivní, aktivita seznamu se ztrácí.
** Pokud byl seznam L prázdný, nic se neděje.
**/ 
	tDLElemPtr ptr;
    if(L->Last != NULL) {
        ptr = L->Last;
        if(L->Act == L->Last) { //posledny prvok bol aktivny
            L->Act = NULL;  //zrusi sa aktivita zoznamu
        }
        if(L->First == L->Last) { //zoznam mal iba jeden prvok, vynuluje sa
            L->First = NULL;
            L->Last = NULL;
        } else {
            L->Last = L->Last->lptr; //zmeni sa zaciatok zoznamu, posunie sa o jeden doprava
            L->Last->rptr = NULL; //novemu zaciatku sa nastavi lavy ptr na NULL
        }
        free(ptr);
    }
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLPostDelete (tDLList *L) {
/*
** Zruší prvek seznamu L za aktivním prvkem.
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** posledním prvkem seznamu, nic se neděje.
**/
	if(L->Act != NULL) {
        if(L->Act->rptr != NULL) {
            tDLElemPtr ptr;
            ptr = L->Act->rptr;
            L->Act->rptr = ptr->rptr;

            if(ptr == L->Last) {
                L->Last = L->Act;
            } else {
                ptr->rptr->lptr = L->Act;
            }
            free(ptr);
        }
    }
		
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLPreDelete (tDLList *L) {
/*
** Zruší prvek před aktivním prvkem seznamu L .
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** prvním prvkem seznamu, nic se neděje.
**/
	if(L->Act != NULL) {
        if(L->Act->lptr != NULL) {
            tDLElemPtr ptr;
            ptr = L->Act->lptr;
            L->Act->lptr = ptr->lptr;

            if(ptr == L->First) {
                L->First = L->Act;
            } else {
                ptr->lptr->rptr = L->Act;
            }
            free(ptr);
        }
    }
			
// solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLPostInsert (tDLList *L, int val) {
/*
** Vloží prvek za aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	if(L->Act != NULL) { //kontrola ci je zoznam aktivny
        tDLElemPtr ptr = malloc(sizeof(struct tDLElem));
        if(ptr == NULL) { //kontrola uspesnosti malloc
            DLError();
            return;
        }

        ptr->data = val;
        ptr->rptr = L->Act->rptr;
        ptr->lptr = L->Act;
        L->Act->rptr = ptr;

        if(L->Act == L->Last) { //vklada za posledny clen
            L->Last = ptr; //novy ukazatel na koniec
        } else {
            ptr->rptr->lptr = ptr; //prvok napravo naviaze na novo vlozeny ak nie je posledny
        }

    }
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLPreInsert (tDLList *L, int val) {
/*
** Vloží prvek před aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	if(L->Act != NULL) { //kontrola ci je zoznam aktivny
        tDLElemPtr ptr = malloc(sizeof(struct tDLElem));
        if(ptr == NULL) { //kontrola uspesnosti malloc
            DLError();
            return;
        }

        ptr->data = val;
        ptr->rptr = L->Act;
        ptr->lptr = L->Act->lptr;
        L->Act->lptr = ptr;

        if(L->Act == L->First) { //vklada pred prvy
            L->First = ptr; //novy ukazatel na zaciatok
        } else {
            ptr->lptr->rptr = ptr; //prvok napravo naviaze na novo vlozeny ak nie je posledny
        }

    }
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLCopy (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
** Pokud seznam L není aktivní, volá funkci DLError ().
**/
	if(L == NULL || L->Act == NULL) {
        DLError();
        return;
    } else {
        *val = L->Act->data;
    }	
	
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLActualize (tDLList *L, int val) {
/*
** Přepíše obsah aktivního prvku seznamu L.
** Pokud seznam L není aktivní, nedělá nic.
**/
	if(L == NULL || L->Act == NULL) {
        return;
    } else {
        L->Act->data = val;
    }
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

void DLSucc (tDLList *L) {
/*
** Posune aktivitu na následující prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na posledním prvku se seznam stane neaktivním.
**/
	if(L == NULL || L->Act == NULL) {
        return;
    }
	L->Act = L->Act->rptr;
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}


void DLPred (tDLList *L) {
/*
** Posune aktivitu na předchozí prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na prvním prvku se seznam stane neaktivním.
**/
	if(L == NULL || L->Act == NULL) {
        return;
    }
	L->Act = L->Act->lptr;
	
// solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

int DLActive (tDLList *L) {
/*
** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
** Funkci je vhodné implementovat jedním příkazem return.
**/
	if(L->Act != NULL) {
        return 1;
    } else {
        return 0;
    }
    
	
 //solved = FALSE;                   /* V případě řešení, smažte tento řádek! */
}

/* Konec c206.c*/
