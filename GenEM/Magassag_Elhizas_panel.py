# -*- coding: utf-8 -*-
"""
============================================================
 MAGASSÁG + ELHÍZÁSI HAJLAM – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki a magasság
 és az elhízási hajlam (BMI) genetikai markereit.

 A panel NEM diagnózis, csak genetikai hajlamot jelez.
============================================================
"""

import os
import csv

# ============================================================
# AUTOMATIKUS MYHERITAGE RAW FÁJLVÁLASZTÓ
# ============================================================

def select_raw_file():
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
# SNP LISTA – MAGASSÁG + ELHÍZÁS
# ============================================================

VARIANTS = [
    # MAGASSÁG
    {"gene": "HMGA2", "rsid": "rs1042725", "risk_allele": "C", "weight": 2.5, "group": "MAGASSÁG"},
    {"gene": "EFEMP1", "rsid": "rs3791679", "risk_allele": "A", "weight": 1.5, "group": "MAGASSÁG"},
    {"gene": "GDF5", "rsid": "rs143383", "risk_allele": "T", "weight": 1.5, "group": "MAGASSÁG"},
    {"gene": "SOCS2", "rsid": "rs10889677", "risk_allele": "A", "weight": 1.0, "group": "MAGASSÁG"},
    {"gene": "ZBTB38", "rsid": "rs6440003", "risk_allele": "A", "weight": 1.0, "group": "MAGASSÁG"},

    # ELHÍZÁSI HAJLAM (BMI)
    {"gene": "FTO", "rsid": "rs9939609", "risk_allele": "A", "weight": 3.0, "group": "ELHÍZÁS"},
    {"gene": "MC4R", "rsid": "rs17782313", "risk_allele": "C", "weight": 2.5, "group": "ELHÍZÁS"},
    {"gene": "TMEM18", "rsid": "rs6548238", "risk_allele": "C", "weight": 2.0, "group": "ELHÍZÁS"},
    {"gene": "SH2B1", "rsid": "rs7498665", "risk_allele": "G", "weight": 1.5, "group": "ELHÍZÁS"},
    {"gene": "NEGR1", "rsid": "rs2815752", "risk_allele": "A", "weight": 1.5, "group": "ELHÍZÁS"},
    {"gene": "BDNF", "rsid": "rs6265", "risk_allele": "A", "weight": 1.0, "group": "ELHÍZÁS"},
    {"gene": "GNPDA2", "rsid": "rs10938397", "risk_allele": "G", "weight": 1.0, "group": "ELHÍZÁS"},
]


# ============================================================
# SNP ÉRTELMEZÉS
# ============================================================

def interpret_single_variant(genotype, risk_allele):
    if genotype is None:
        return None, 0, "A variáns nem található a RAW fájlban."

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
        risk_allele = var["risk_allele"]
        weight = var["weight"]
        group = var["group"]

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
# KATEGÓRIA MEGHATÁROZÁS
# ============================================================

def classify_ratio(r):
    if r <= 0.20:
        return "ALACSONY genetikai hajlam"
    if r <= 0.40:
        return "MÉRSÉKELT genetikai hajlam"
    if r <= 0.70:
        return "KÖZEPESEN EMELKEDETT genetikai hajlam"
    return "EMELKEDETT genetikai hajlam"


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max):
    outname = f"Magassag_Elhizas_panel_eredmeny_{filename}.txt"
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" MAGASSÁG + ELHÍZÁSI HAJLAM – GENETIKAI PANEL")
    add("==============================================\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    # Összpontszám
    ratio = total_weighted / max_weighted
    category = classify_ratio(ratio)

    bar_len = 30
    filled = int(ratio * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    add("=== ÖSSZPONTSZÁM ===\n")
    add(f"[{bar}]  {total_weighted:.1f} / {max_weighted:.1f}")
    add(f"Genetikai hajlam kategória: {category}\n")

    # Csoportok
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

    # Részletes SNP lista
    add("=== RÉSZLETES SNP LISTA ===\n")
    for r in results:
        add(f"{r['rsid']} ({r['gene']}) – csoport: {r['group']}")
        add(f"   Genotípus: {r['genotype']}, kockázat: {r['risk_count']}, súly: {r['weighted']:.1f}")
        add(f"   Értelmezés: {r['interpretation']}\n")

    add("==============================================")
    add(" FONTOS MEGJEGYZÉS")
    add("==============================================\n")
    add("- A magasság és elhízási hajlam erősen poligénes tulajdonságok.")
    add("- A környezet, étrend, életmód és hormonális tényezők is jelentősen befolyásolják.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Magasság + Elhízási hajlam genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    raw_data = read_raw_data(filename)
    results, total_weighted, max_weighted, group_scores, group_max = evaluate_panel(raw_data)
    print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max)


if __name__ == "__main__":
    run()
