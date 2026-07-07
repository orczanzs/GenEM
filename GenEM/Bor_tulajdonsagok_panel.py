# -*- coding: utf-8 -*-
"""
============================================================
 BŐR TULAJDONSÁGOK – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból keresi ki azokat a
 variánsokat, amelyek szakirodalmi adatok alapján összefüggésbe
 hozhatók a bőrtónus genetikai meghatározóival.

 A pontszám NEM diagnosztikai értékű, csak genetikai irányultságot
 jelez (világosabb ↔ sötétebb tónus).
============================================================
"""

import os
import csv

# ============================================================
# AUTOMATIKUS MYHERITAGE FÁJLVÁLASZTÓ
# ============================================================

def select_raw_file():
    """Automatikusan kilistázza a mappában található MyHeritage RAW CSV fájlokat."""
    candidates = [
        f for f in os.listdir(".")
        if f.lower().endswith(".csv") and "myheritage" in f.lower()
    ]

    if not candidates:
        print("❌ Nem található MyHeritage RAW DNA fájl a mappában.")
        return None

    print("\n📂 Elérhető MyHeritage RAW fájlok:")
    for i, fname in enumerate(candidates, start=1):
        print(f"  {i}. {fname}")

    while True:
        try:
            choice = int(input("\nVálassz fájlt (szám): "))
            if 1 <= choice <= len(candidates):
                return candidates[choice - 1]
            print("Érvénytelen választás.")
        except ValueError:
            print("Számot adj meg.")


# ============================================================
# SNP LISTA – BŐR PANEL
# ============================================================

BOR_PANEL_SNPK = [
    "rs1426654", "rs16891982", "rs12913832", "rs1042602", "rs1800414",
    "rs1805007", "rs1805008", "rs885479", "rs2153271", "rs6058017",
    "rs12203592", "rs1393350"
]


# ============================================================
# SNP ÉRTÉKELÉS – PONTSZÁM + MAGYARÁZAT
# ============================================================

def bor_panel_ertekeles(megtalalt_snpk):
    """A megtalált SNP-k alapján pontszámot és kategóriát számol."""
    pont = 0.0
    magyarazat = []

    # SLC24A5 – rs1426654
    if "rs1426654" in megtalalt_snpk:
        gt = megtalalt_snpk["rs1426654"]
        if gt == "AA":
            pont += 3
            magyarazat.append("rs1426654 (SLC24A5): AA → erősen világos irány.")
        elif gt in ["AG", "GA"]:
            pont += 1
            magyarazat.append("rs1426654 (SLC24A5): AG → világos irány.")
        else:
            magyarazat.append("rs1426654 (SLC24A5): GG → sötétebb irány.")

    # SLC45A2 – rs16891982
    if "rs16891982" in megtalalt_snpk:
        gt = megtalalt_snpk["rs16891982"]
        if gt == "CC":
            pont += 3
            magyarazat.append("rs16891982 (SLC45A2): CC → nagyon világos irány.")
        elif gt in ["CG", "GC"]:
            pont += 1
            magyarazat.append("rs16891982 (SLC45A2): CG → világos irány.")
        else:
            magyarazat.append("rs16891982 (SLC45A2): GG → sötétebb irány.")

    # HERC2 – rs12913832
    if "rs12913832" in megtalalt_snpk:
        gt = megtalalt_snpk["rs12913832"]
        if gt == "AA":
            pont += 1
            magyarazat.append("rs12913832 (HERC2): AA → világosabb tónus.")
        elif gt in ["AG", "GA"]:
            pont += 0.5
            magyarazat.append("rs12913832 (HERC2): AG → enyhe világosító hatás.")
        else:
            magyarazat.append("rs12913832 (HERC2): GG → semleges vagy sötétebb.")

    # TYR – rs1042602
    if "rs1042602" in megtalalt_snpk:
        gt = megtalalt_snpk["rs1042602"]
        if gt == "AA":
            pont += 1
            magyarazat.append("rs1042602 (TYR): AA → világosabb tónus.")
        elif gt in ["AC", "CA"]:
            pont += 0.5
            magyarazat.append("rs1042602 (TYR): AC → enyhe világosító hatás.")

    # OCA2 – rs1800414
    if "rs1800414" in megtalalt_snpk:
        gt = megtalalt_snpk["rs1800414"]
        if gt == "AA":
            pont += 1
            magyarazat.append("rs1800414 (OCA2): AA → világosabb tónus.")
        elif gt in ["AG", "GA"]:
            pont += 0.5
            magyarazat.append("rs1800414 (OCA2): AG → enyhe világosító hatás.")

    # MC1R – rs1805007, rs1805008, rs885479
    for snp in ["rs1805007", "rs1805008", "rs885479"]:
        if snp in megtalalt_snpk:
            gt = megtalalt_snpk[snp]
            if any(a in gt for a in ["A", "T"]):
                pont += 1
                magyarazat.append(f"{snp} (MC1R): világosító irány.")

    # IRF4 – rs12203592
    if "rs12203592" in megtalalt_snpk:
        gt = megtalalt_snpk["rs12203592"]
        if gt == "TT":
            pont += 1
            magyarazat.append("rs12203592 (IRF4): TT → világosabb bőr, szeplőhajlam.")
        elif gt in ["CT", "TC"]:
            pont += 0.5
            magyarazat.append("rs12203592 (IRF4): CT → enyhe világosító hatás.")

    # ASIP – rs6058017
    if "rs6058017" in megtalalt_snpk:
        if megtalalt_snpk["rs6058017"] == "AA":
            pont += 1
            magyarazat.append("rs6058017 (ASIP): AA → világosabb tónus.")

    # TYR – rs1393350
    if "rs1393350" in megtalalt_snpk:
        if megtalalt_snpk["rs1393350"] == "AA":
            pont += 1
            magyarazat.append("rs1393350 (TYR): AA → világosító irány.")

    # Kategória meghatározása
    if pont >= 8:
        kategoria = "nagyon világos"
    elif pont >= 6:
        kategoria = "világos"
    elif pont >= 4:
        kategoria = "világos-közepes"
    elif pont >= 2:
        kategoria = "közepes"
    elif pont >= 1:
        kategoria = "közepes-sötét"
    else:
        kategoria = "sötét vagy nagyon sötét"

    return kategoria, pont, magyarazat


# ============================================================
# SNP KERESÉS + RIPORT
# ============================================================

def snp_kereses_es_ertekeles(fajlnev):
    """Megkeresi a panel SNP-jeit és kiértékeli őket."""
    megtalalt = {}
    hianyzik = []

    print(f"\n📄 Elemzett RAW fájl: {fajlnev}\n")

    with open(fajlnev, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        sorok = list(reader)

    for snp in BOR_PANEL_SNPK:
        talalat = False
        for sor in sorok:
            if not sor or sor[0].startswith("#"):
                continue
            if len(sor) >= 4 and sor[0] == snp:
                megtalalt[snp] = sor[3].strip()
                print(f"{snp} → megtalálva ({sor[3].strip()})")
                talalat = True
                break
        if not talalat:
            hianyzik.append(snp)
            print(f"{snp} → NINCS a RAW fájlban")

    # Összegzés
    osszes = len(BOR_PANEL_SNPK)
    talalt_db = len(megtalalt)
    hiany_db = len(hianyzik)

    kategoria, pont, magyarazat = bor_panel_ertekeles(megtalalt)

    osszegzes = []
    osszegzes.append("--- BŐR-PANEL ÖSSZEGZÉS ---")
    osszegzes.append(f"Elemzett fájl: {fajlnev}")
    osszegzes.append(f"Összes SNP: {osszes}")
    osszegzes.append(f"Megtalált SNP: {talalt_db}")
    osszegzes.append(f"Hiányzó SNP: {hiany_db}")
    osszegzes.append("")

    if talalt_db == 0:
        osszegzes.append("A panel SNP-jei egyike sem található meg a RAW fájlban.")
        osszegzes.append("Ez gyakori MyHeritage esetén, mert a chip nem tartalmaz bőrszín markereket.")
    else:
        osszegzes.append(f"Bőrtónus kategória: {kategoria}")
        osszegzes.append(f"Összpontszám: {pont}")
        osszegzes.append("")
        osszegzes.append("Részletes magyarázat:")
        for m in magyarazat:
            osszegzes.append(f"- {m}")

    szoveg = "\n".join(osszegzes)

    print("\n" + szoveg)

    with open("bor_panel_osszefoglalo.txt", "w", encoding="utf-8") as f:
        f.write(szoveg)

    print("\n💾 Az összegzés elmentve: bor_panel_osszefoglalo.txt")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Bőr tulajdonságok panel ===")
    fajlnev = select_raw_file()
    if fajlnev is None:
        return
    snp_kereses_es_ertekeles(fajlnev)


if __name__ == "__main__":
    run()
