
**Popis projektu**

Program stahuje seznam obcí z hlavní stránky okresu.
Pro každou obec načte detailní výsledky voleb:
Voliči v seznamu
Vydané obálky
Platné hlasy
Počet hlasů pro každou kandidující stranu
Výsledky se ukládají do CSV, které lze otevřít v Excelu nebo jiných tabulkových editorech.
Kód je napsán v souladu s PEP8, využívá funkce s návratovými hodnotami a nepoužívá globální proměnné.

**Ukázka použití**
Pro okres Prostějov:
python scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
Po spuštění vznikne soubor vysledky_prostejov.csv obsahující výsledky všech obcí okresu Prostějov.

**Argumenty v projektu**

Argument	Popis
URL územního celku	Odkaz na stránku volebního územního celku na volby.cz
Výstupní CSV soubor	Název souboru, kam se uloží výsledky
Pokud nejsou zadány oba argumenty, nebo jsou špatně, program vypíše chybovou hlášku a ukončí se.
URL musí být platný odkaz na stránku volby.cz s výsledky voleb.

**Spuštění projektu**
