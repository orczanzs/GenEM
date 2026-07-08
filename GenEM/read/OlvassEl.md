# 📘 Genetikai  Ellemző Műszerfal 
# 📘 GenEM
# 📘 Genetikai Hajlam  Ellemző Panelrendszer – Háromszintű Tudásrendszer

Ez a program egy teljesen offline működő, magyar nyelvű genetikai
elemző rendszer, amely MyHeritage RAW DNA fájlokból képes különböző
genetikai hajlamokat és tulajdonságokat értelmezni.

A rendszer célja, hogy mindenki számára érthető módon mutassa be,
milyen genetikai mintázatok befolyásolhatják a szervezet működését,
az anyagcserét, a külső tulajdonságokat vagy az életmóddal kapcsolatos
hajlamokat.

A projekt fejlesztése során kiemelt szempont volt:
- a biztonság,
- az átláthatóság,
- a GDPR‑megfelelés,
- és az, hogy a felhasználó adatai soha ne kerüljenek ki a saját gépéről.
A program maradéktalanul megfelel az Európai Unió általános
adatvédelmi rendeletének (GDPR). (Részletesen olvasható  e dokumentáció végén) 

A projekt jelenleg 15 különálló genetikai modult tartalmaz.
Mindegyik egy-egy témakört vizsgál, és érthető módon mutatja be,
milyen genetikai mintázatok befolyásolhatják:

- az egészséggel kapcsolatos hajlamokat,
- a külső tulajdonságokat,
- az anyagcserét,
- az életmóddal összefüggő működéseket,
- vagy a fizikai teljesítményt.

A 15 panel:

1) Allergia hajlam panel
2) Atópiás dermatitis panel
3) Bőr tulajdonságok panel
4) Élelmiszer érzékenység panel
5) Életmód hajlam panel (15 almodul)
6) Haj tulajdonságok panel
7) Hisztamin intolerancia panel
8) Ízületi hajlam panel
9) Laktóz panel
10) Látható tulajdonságok panel
11) Magasság és elhízás panel
12) Öregedés hajlam panel
13) Sport hajlam panel
14) Szem tulajdonságok panel
15) Y-haplocsoport panel
16) SNP ellenőrző panel 

Mindegyik panel külön futtatható, és külön TXT riportot készít.

Ez a dokumentáció három egymásra épülő szinten magyarázza el, hogyan
működik a program és hogyan értelmezi a MyHeritage RAW DNA fájlokat.

A három szint:

1. **Alapszint** – teljesen laikusoknak  
2. **Ismeretterjesztő szint** – aki mélyebben érteni szeretné  
3. **Tudományos szint** – aki a genetikai alapokat is meg akarja érteni  

Mindhárom szint külön-külön is olvasható, de egymásra épülnek.

---

## 🟦 1) ALAPSZINT – Mit csinál a program?

<details>
<summary><strong>Megnyitás / Bezárás</strong></summary>

A program MyHeritage RAW DNA fájlokból olvas ki genetikai információkat,
és különböző „hajlam panelokon” keresztül megmutatja, hogy a felhasználó
milyen genetikai adottságokkal rendelkezik.

A program NEM diagnosztikai eszköz, csak genetikai hajlamot jelez.

### Mit csinál pontosan?

1. Felismeri a mappában lévő MyHeritage .csv fájlokat.  
2. A felhasználó kiválasztja, melyiket szeretné elemezni.  
3. A panel kiolvassa a fontos genetikai pontokat (SNP-ket).  
4. Súlyozott pontszámot számol.  
5. Kiírja az eredményt a képernyőre.  
6. Létrehoz egy részletes TXT fájlt.  

A rendszer moduláris: minden panel külön futtatható.

</details>

---

## 🟩 2) ISMERETTERJESZTŐ SZINT – Hogyan működik a genetikai elemzés?

<details>
<summary><strong>Megnyitás / Bezárás</strong></summary>

A MyHeritage RAW DNA fájl egy egyszerű táblázat, amelyben minden sor egy
genetikai variánst ír le. Ezeket SNP-nek nevezzük (Single Nucleotide
Polymorphism).

### Egy tipikus sor így néz ki:

```
rs4988235,7,117199646,AG
```

Ez négy dolgot jelent:

#### 1. rsID – a genetikai „címke”
Minden SNP-nek egyedi azonosítója van, pl. **rs4988235**.  
A tudományos kutatások is így hivatkoznak rá.

#### 2. Kromoszóma száma
A variáns a **7. kromoszómán** található.

#### 3. Pozíció
A pontos hely a kromoszómán belül.

#### 4. Genotípus
A felhasználó két allélt örököl: pl. **A** és **G** → **AG**.  
Ezek a betűk a DNS építőkövei: A, C, G, T.

---

### Mit csinál a program ezekkel?

- Megkeresi a fontos SNP-ket.  
- Megnézi, hordozza-e a felhasználó a kockázati allélt.  
- Megszámolja, hány kockázati allélt tartalmaz a genotípus.  
- Súlyozza a hatást (nem minden SNP egyformán fontos).  
- Összpontszámot számol.  
- Kategóriát ad: alacsony / mérsékelt / emelkedett hajlam.  

A program tehát nem diagnosztizál, hanem genetikai valószínűséget mutat.

</details>

---

## 🟥 3) TUDOMÁNYOS SZINT – Mély genetikai magyarázat

<details>
<summary><strong>Megnyitás / Bezárás</strong></summary>

A MyHeritage által biztosított RAW DNA fájl **SNP-alapú genotipizálást**
tartalmaz. Ez azt jelenti, hogy a teljes genom ~0.02%-át vizsgálja,
de olyan pontokon, amelyek tudományosan bizonyítottan relevánsak.

---

### 🔬 Mi az az SNP?

**SNP = Single Nucleotide Polymorphism**  
Egyetlen nukleotid (A, C, G vagy T) eltérése a populációban.

Példa:
- Valakinél: A → G  
- Másnál: A → A  

Ez a különbség befolyásolhat:

- enzimműködést  
- hormontermelést  
- immunválaszt  
- anyagcserét  
- allergiás reakciókat  
- gyógyszerlebontást  

---

### 🔬 Mi az rsID?

Az **rsID** (pl. rs4988235) egy globális, tudományos azonosító.  
Az NCBI dbSNP adatbázis tartja nyilván.

---

### 🔬 Mi az allél?

A DNS két szálból áll, ezért minden SNP-hez két betű tartozik:

- AA  
- AG  
- GG  
- CT  
- TT  

---

### 🔬 Mi a kockázati allél?

A tudományos kutatások megállapítják, hogy egy adott SNP melyik
allélja növeli a kockázatot egy tulajdonságra.

Példák:

- **rs4988235 G** → laktózérzékenység  
- **rs2251746 T** → magasabb IgE szint (allergiahajlam)  
- **rs1815739 T** → lassú izomrost (állóképesség)  

---

### 🔬 Hogyan számol a program?

1. Minden SNP-hez tartozik:
   - kockázati allél  
   - súly (hatás erőssége)  
   - csoport (pl. GLUTÉN, ASZTMA, METABOLIZMUS)  

2. A program megszámolja:
   - 0 kockázati allél → nincs hatás  
   - 1 kockázati allél → heterozigóta hatás  
   - 2 kockázati allél → homozigóta hatás  

3. A hatást súlyozza:
   **súly × kockázati allél száma**

4. A csoportok pontszámait összeadja.

5. A maximális pontszámhoz viszonyítva kategóriát ad.

Ez a módszer megfelel a modern genetikai rizikóbecslés  
(**polygenic risk score**) alapelveinek.

</details>

# 🧬 DNS-elemző rendszer – Bevezetés és alapinformációk

============================================================
 ADATBIZTONSÁG! Ügyelj a személyes adataidra!
============================================================



------------------------------------------------------------
 🔐 GDPR-MEGFELELÉS ÉS ADATVÉDELEM
------------------------------------------------------------

A program maradéktalanul megfelel az Európai Unió általános
adatvédelmi rendeletének (GDPR).

Ez a gyakorlatban azt jelenti, hogy:

- minden feldolgozás teljes mértékben offline történik,
- a program nem csatlakozik az internethez,
- nem küld adatot, nem tölt le semmit,
- a RAW fájl és az eredmények kizárólag a felhasználó gépén maradnak,
- semmilyen adat nem kerül továbbításra harmadik fél felé.

A rendszer nem tárol, nem továbbít és nem oszt meg semmilyen információt.

------------------------------------------------------------
 ⚠️ FONTOS FIGYELMEZTETÉS A RAW DNA FÁJLOKRÓL
------------------------------------------------------------

A MyHeritage RAW DNA fájl rendkívül érzékeny, személyes genetikai
információkat tartalmaz. Ezek az adatok egyedi biológiai azonosítók,
és visszaélés esetén komoly adatvédelmi kockázatot jelenthetnek.

Ezért különösen fontos:

- csak saját RAW fájlt elemezzünk,
- vagy kizárólag akkor, ha valaki kifejezetten engedélyt adott rá,
- az adatokat ne osszuk meg, ne küldjük tovább,
- az eredményfájlokat is biztonságos helyen tároljuk,
- és ügyeljünk arra, hogy a fájl ne kerülhessen illetéktelen személyek kezébe.

A program célja személyes önismeret és ismeretterjesztés.
Nem orvosi diagnózis.
## 🛠 Telepítés

A GenEM telepítése Windows alatt egyszerű és gyors.

### 1. A program letöltése
Töltsd le a GenEM projektet a GitHubról:

1. Nyisd meg a projekt oldalát.
2. Kattints a **Code → Download ZIP** gombra.
3. Csomagold ki a ZIP fájlt.

A kicsomagolt mappát nevezd át **GenEM**-re, majd **helyezd az Asztalra**.  
Ez a legegyszerűbb módja annak, hogy a program mindig könnyen elérhető legyen.

### 2. Python telepítése
A GenEM működéséhez Python 3.10 vagy újabb szükséges.  
Letöltés: https://www.python.org/downloads/

Telepítéskor pip-et is engedélyezd.

### 3. A GenEM indítása Windows alatt

A GenEM kétféleképpen indítható:

#### 1) indit.bat – automatikus parancsikon létrehozással
Az `indit.bat` fájl a következőket végzi:
- elindítja a GenEM programot,
- létrehoz egy parancsikont az Asztalon,
- az Asztalon megjelenő ikonnal később egy kattintással indítható a GenEM.

Használat:
1. Nyisd meg az Asztalon lévő **GenEM** mappát.
2. Kattints duplán az `indit.bat` fájlra.
3. A program elindul.
4. Az Asztalon megjelenik egy új ikon: **GenEM**.
5. Innentől kezdve a GenEM egy kattintással indítható az ikonról.

#### 2) genem.bat – közvetlen indítás a mappából
A GenEM a mappából is indítható a `genem.bat` fájlra kattintva.

Használat:
1. Nyisd meg az Asztalon lévő **GenEM** mappát.
2. Kattints duplán a `genem.bat` fájlra.
3. A program azonnal elindul.

### 4. Személyes DNA fájlok használata
A személyes **_raw_dna_data.csv_** fájlt helyezd a GenEM mappába, mert a program innen olvassa be az elemzéshez szükséges adatokat.  
Az egyes panelek kiértékelésének eredményeit a program automatikusan **.txt formátumban** menti a GenEM mappába.

---

## ⚠️ Adatbiztonsági figyelmeztetés

A GenEM rendkívül érzékeny személyes adatokkal dolgozik, mivel a RAW DNA fájlok genetikai információkat tartalmaznak.  
A program **teljes mértékben offline működik**, nem küld adatot semmilyen szerverre, és nem kapcsolódik az internethez.

Kérjük, különösen figyelj oda arra, hogy:
- a személyes _raw_dna_data.csv_ fájlt csak te kezeld,
- a fájlt biztonságos helyen tartsd,
- ne oszd meg másokkal,
- csak saját gépen futtasd a GenEM-et.

A GenEM által mentett .txt eredmények szintén személyes adatnak minősülnek, ezért kezeld őket körültekintően.

## ❤️ Támogatás / Szponzoráció

Ha hasznosnak találod a GenEM rendszert, és szeretnéd támogatni a fejlesztését, lehetőséged van szponzorrá válni.

A támogatásod segít abban, hogy tovább fejlesszem a programot, új funkciókat adjak hozzá, és folyamatosan naprakészen tartsam a rendszert.

## Support ....  akár egy kávé árával
👉 **Buy Me a Coffee:** https://buymeacoffee.com/orczanaz  
👉 **Revolut:** https://revolut.me/orczanz
Köszönöm, hogy fontolóra veszed a projekt támogatását!

