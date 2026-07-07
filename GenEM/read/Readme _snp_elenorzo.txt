


**Egyszerű, offline eszköz rsID ellenőrzésre MyHeritage CSV RAW fájlokból.**

Ez az első GitHub változat — minimális, jól dokumentált, könnyen használható.  
A projekt célja: gyorsan és biztonságosan előkészíteni egy adott **rsID** környezetét ellenőrzésre (AI-hoz vagy manuális vizsgálathoz), anélkül,
 hogy a RAW fájlok módosulnának vagy adat kikerülne az internetre.

---

## Fő funkciók
- **Kiválaszt egy `.csv` RAW fájlt** a munkamappából.  
- **Megkeres egy megadott rsID**-t (egyet).  
- Kiírja a keresett sort   
- A keresett sort **`>>`** jellel kiemeli.  
- A kimenetet **dátumos `.txt` fájlba menti** (a RAW fájl neve és az rsID szerepel a fájlnévben).  
- A kimenetet **automatikusan a vágólapra másolja**, hogy azonnal be tudd illeszteni bármely AI chatbe.  
- **Nem módosítja** a RAW fájlt; minden művelet offline történik.

---

## Gyors kezdés

1. Helyezd a `Snp_ellenorzo_panel.py` fájlt ugyanabba a mappába, ahol a RAW `.csv` található.  
2. Nyisd meg a terminált a mappában.  
3. Futtasd:
   ```bash
   python Snp_ellenorzo_panel.py
