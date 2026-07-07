# -*- coding: utf-8 -*-
"""
============================================================
 ÉLETMÓD – GENETIKAI HAJLAM PANEL (15 ALMODUL)
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki azokat a
 genetikai variánsokat, amelyek az alábbi életmóddal
 összefüggő hajlamokkal hozhatók kapcsolatba:

 1) Alvás – cirkadián ritmus
 2) Alvásminőség
 3) Stresszreakció – kortizol
 4) Szorongásra való hajlam
 5) Koffein metabolizmus
 6) Alkohol lebontás
 7) Étvágy és jóllakottság
 8) Anyagcsere sebesség
 9) Szénhidrát-érzékenység
10) Zsírok metabolizmusa
11) Vitaminok (D, B12, folát)
12) Magnézium és elektrolitok
13) Természetes aktivitási szint
14) Regenerációs sebesség
15) Fáradékonyság genetikai mintázat

 A panel NEM diagnózis, csak genetikai hajlamot jelez.
============================================================
"""

import os
import csv
from datetime import datetime

# ============================================================
# AUTOMATIKUS RAW FÁJLVÁLASZTÓ
# ============================================================

def select_raw_file():
    candidates = [
        f for f in os.listdir(".")
        if f.lower().endswith(".csv") and "myheritage" in f.lower()
    ]

    if not candidates:
        print("❌ Nem található MyHeritage RAW DNA fájl.")
        return None

    print("\n📂 Elérhető RAW fájlok:")
    for i, f in enumerate(candidates, 1):
        print(f"  {i}. {f}")

    while True:
        try:
            c = int(input("\nVálassz fájlt (szám): "))
            if 1 <= c <= len(candidates):
                return candidates[c - 1]
            print("Érvénytelen választás.")
        except ValueError:
            print("Számot adj meg.")


# ============================================================
# RAW BEOLVASÁS
# ============================================================

def read_raw_data(file_path):
    data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            if len(row) < 4:
                continue
            rsid = row[0].strip()
            genotype = row[3].strip().upper()
            data[rsid] = genotype
    return data


# ============================================================
# SNP LISTA – 15 ÉLETMÓD ALMODUL
# ============================================================

VARIANTS = [

    # 1) Alvás – cirkadián ritmus
    {"group": "ALVÁS – CIRKADIÁN", "gene": "CLOCK", "rsid": "rs1801260", "risk_allele": "C", "weight": 2.0},
    {"group": "ALVÁS – CIRKADIÁN", "gene": "PER3",  "rsid": "rs228697",  "risk_allele": "G", "weight": 2.0},

    # 2) Alvásminőség
    {"group": "ALVÁSMINŐSÉG", "gene": "BDNF", "rsid": "rs6265", "risk_allele": "A", "weight": 2.0},
    {"group": "ALVÁSMINŐSÉG", "gene": "CACNA1C", "rsid": "rs1006737", "risk_allele": "A", "weight": 1.5},

    # 3) Stresszreakció – kortizol
    {"group": "STRESSZ", "gene": "COMT", "rsid": "rs4680", "risk_allele": "A", "weight": 3.0},

    # 4) Szorongás
    {"group": "SZORONGÁS", "gene": "SLC6A4", "rsid": "rs25531", "risk_allele": "T", "weight": 2.0},

    # 5) Koffein metabolizmus
    {"group": "KOFFEIN", "gene": "CYP1A2", "rsid": "rs762551", "risk_allele": "A", "weight": 3.0},

    # 6) Alkohol lebontás
    {"group": "ALKOHOL", "gene": "ALDH2", "rsid": "rs671", "risk_allele": "A", "weight": 3.0},

    # 7) Étvágy és jóllakottság
    {"group": "ÉTVÁGY", "gene": "FTO", "rsid": "rs9939609", "risk_allele": "A", "weight": 2.0},

    # 8) Anyagcsere sebesség
    {"group": "ANYAGCSERE", "gene": "FADS1", "rsid": "rs174537", "risk_allele": "T", "weight": 2.0},

    # 9) Szénhidrát-érzékenység
    {"group": "SZÉNHIDRÁT", "gene": "TCF7L2", "rsid": "rs7903146", "risk_allele": "T", "weight": 3.0},

    # 10) Zsírok metabolizmusa
    {"group": "ZSÍRANYAGCSERE", "gene": "APOA2", "rsid": "rs5082", "risk_allele": "C", "weight": 2.0},

    # 11) Vitaminok
    {"group": "VITAMIN", "gene": "GC", "rsid": "rs2282679", "risk_allele": "A", "weight": 2.0},

    # 12) Magnézium
    {"group": "MAGNÉZIUM", "gene": "CNNM2", "rsid": "rs11191548", "risk_allele": "C", "weight": 2.0},

    # 13) Természetes aktivitás
    {"group": "AKTIVITÁS", "gene": "MAOA", "rsid": "rs6323", "risk_allele": "T", "weight": 1.5},

    # 14) Regeneráció
    {"group": "REGENERÁCIÓ", "gene": "ACTN3", "rsid": "rs1815739", "risk_allele": "T", "weight": 2.0},

    # 15) Fáradékonyság
    {"group": "FÁRADÉKONYSÁG", "gene": "SOD2", "rsid": "rs4880", "risk_allele": "C", "weight": 2.0},
]


# ============================================================
# SNP ÉRTELMEZÉS
# ============================================================

def interpret_single_variant(genotype, risk_allele):
    if genotype is None:
        return None, 0, "A variáns nem található."

    alleles = list(genotype)
    risk_count = alleles.count(risk_allele)

    if risk_count == 0:
        text = "Nem hordoz kockázati allélt."
    elif risk_count == 1:
        text = "Heterozigóta kockázati allél."
    else:
        text = "Homozigóta kockázati allél."

    return genotype, risk_count, text


# ============================================================
# PANEL KIÉRTÉKELÉSE
# ============================================================

def evaluate_panel(raw_data):
    results = []
    total_weighted = 0.0
    max_weighted = 0.0

    group_scores = {}
    group_max = {}

    for var in VARIANTS:
        rsid = var["rsid"]
        gene = var["gene"]
        group = var["group"]
        risk_allele = var["risk_allele"]
        weight = var["weight"]

        genotype = raw_data.get(rsid)
        genotype, risk_count, interp = interpret_single_variant(genotype, risk_allele)

        weighted = risk_count * weight
        total_weighted += weighted
        max_weighted += 2 * weight

        group_scores[group] = group_scores.get(group, 0.0) + weighted
        group_max[group] = group_max.get(group, 0.0) + 2 * weight

        results.append({
            "gene": gene,
            "rsid": rsid,
            "group": group,
            "risk_allele": risk_allele,
            "genotype": genotype,
            "risk_count": risk_count,
            "weighted": weighted,
            "interpretation": interp,
        })

    return results, total_weighted, max_weighted, group_scores, group_max


# ============================================================
# KATEGÓRIA
# ============================================================

def classify_ratio(r):
    if r <= 0.20:
        return "ALACSONY életmód-genetikai érzékenység"
    if r <= 0.40:
        return "MÉRSÉKELT életmód-genetikai érzékenység"
    if r <= 0.70:
        return "KÖZEPESEN EMELKEDETT életmód-genetikai érzékenység"
    return "EMELKEDETT életmód-genetikai érzékenység"


# ============================================================
# RIPORT + TXT MENTÉS (Eredmenyek mappába)
# ============================================================

def print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not os.path.exists("Eredmenyek"):
        os.makedirs("Eredmenyek")

    outname = os.path.join("Eredmenyek", f"Eletmod_panel_eredmeny_{timestamp}.txt")
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" ÉLETMÓD – GENETIKAI HAJLAM PANEL")
    add("==============================================\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    ratio = total_weighted / max_weighted
    category = classify_ratio(ratio)

    bar_len = 30
    filled = int(ratio * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    add("=== ÖSSZPONTSZÁM ===\n")
    add(f"[{bar}]  {total_weighted:.1f} / {max_weighted:.1f}")
    add(f"Genetikai kategória: {category}\n")

    add("=== CSOPORTOSÍTOTT EREDMÉNYEK ===\n")
    for group, score in group_scores.items():
        gmax = group_max[group]
        r = score / gmax
        cat = classify_ratio(r)

        gfilled = int(r * bar_len)
        gbar = "█" * gfilled + "░" * (bar_len - gfilled)

        add(f"🔸 {group}")
        add(f"   Pontszám: {score:.1f} / {gmax:.1f}")
        add(f"   [{gbar}]")
        add(f"   Értelmezés: {cat}\n")

    add("=== RÉSZLETES SNP LISTA ===\n")
    for r in results:
        add(f"{r['rsid']} ({r['gene']}) – csoport: {r['group']}")
        add(f"   Genotípus: {r['genotype']}, kockázat: {r['risk_count']}, súly: {r['weighted']:.1f}")
        add(f"   Értelmezés: {r['interpretation']}\n")

    add("==============================================")
    add(" FONTOS MEGJEGYZÉS")
    add("==============================================\n")
    add("- Az életmóddal kapcsolatos genetikai hajlamok csak részben határozzák meg a mindennapi működést.")
    add("- A környezet, alvás, étrend, stressz és életvitel legalább ilyen fontos.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Életmód genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    raw_data = read_raw_data(filename)
    results, total_weighted, max_weighted, group_scores, group_max = evaluate_panel(raw_data)
    print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max)


if __name__ == "__main__":
    run()
