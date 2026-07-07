# -*- coding: utf-8 -*-
"""
============================================================
 HISZTAMIN ÉRZÉKENYSÉG – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki a hisztamin
 lebontásával, metilációval, gyulladással és bélflórával
 összefüggő SNP-ket.

 A panel NEM diagnózis, csak genetikai hajlamot jelez.
============================================================
"""

import os
import csv

# ============================================================
# AUTOMATIKUS MYHERITAGE RAW FÁJLVÁLASZTÓ
# ============================================================

def select_raw_file():
    """Kilistázza a mappában található MyHeritage RAW CSV fájlokat."""
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
# RAW BEOLVASÁS (CSV)
# ============================================================

def read_raw_data(file_path):
    """Beolvassa a MyHeritage RAW CSV fájlt és visszaadja a genotípusokat."""
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
# HISZTAMIN PANEL SNP-K ÉS SÚLYOK
# ============================================================

VARIANTS = [
    # DAO (AOC1) – hisztamin lebontás (legnagyobb súly)
    {"gene": "AOC1", "rsid": "rs10156191", "risk_allele": "T", "weight": 3.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs1049742", "risk_allele": "T", "weight": 3.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs1049793", "risk_allele": "C", "weight": 3.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs2052129", "risk_allele": "A", "weight": 2.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs2071514", "risk_allele": "T", "weight": 2.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs2070586", "risk_allele": "A", "weight": 2.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},
    {"gene": "AOC1", "rsid": "rs3741775", "risk_allele": "G", "weight": 2.0,
     "group": "DAO", "name": "DAO enzim aktivitás"},

    # HNMT – sejten belüli hisztamin lebontás (közepes súly)
    {"gene": "HNMT", "rsid": "rs11558538", "risk_allele": "T", "weight": 2.0,
     "group": "HNMT", "name": "HNMT enzim aktivitás"},
    {"gene": "HNMT", "rsid": "rs1050891", "risk_allele": "A", "weight": 1.5,
     "group": "HNMT", "name": "HNMT enzim aktivitás"},
    {"gene": "HNMT", "rsid": "rs1801105", "risk_allele": "C", "weight": 1.5,
     "group": "HNMT", "name": "HNMT enzim aktivitás"},

    # MTHFR / MTRR / MTR / CBS – metiláció (kisebb súly)
    {"gene": "MTHFR", "rsid": "rs1801133", "risk_allele": "T", "weight": 1.5,
     "group": "METILÁCIÓ", "name": "MTHFR C677T"},
    {"gene": "MTHFR", "rsid": "rs1801131", "risk_allele": "C", "weight": 1.5,
     "group": "METILÁCIÓ", "name": "MTHFR A1298C"},
    {"gene": "MTRR", "rsid": "rs1801394", "risk_allele": "G", "weight": 1.0,
     "group": "METILÁCIÓ", "name": "MTRR aktivitás"},
    {"gene": "MTR", "rsid": "rs1805087", "risk_allele": "G", "weight": 1.0,
     "group": "METILÁCIÓ", "name": "MTR aktivitás"},
    {"gene": "CBS", "rsid": "rs234706", "risk_allele": "T", "weight": 1.0,
     "group": "METILÁCIÓ", "name": "CBS aktivitás"},
    {"gene": "CBS", "rsid": "rs2298758", "risk_allele": "T", "weight": 1.0,
     "group": "METILÁCIÓ", "name": "CBS aktivitás"},

    # Gyulladásos modulátorok
    {"gene": "IL6", "rsid": "rs1800795", "risk_allele": "C", "weight": 1.5,
     "group": "GYULLADÁS", "name": "IL6 gyulladásos válasz"},
    {"gene": "IL4", "rsid": "rs2243250", "risk_allele": "T", "weight": 1.0,
     "group": "GYULLADÁS", "name": "IL4 gyulladásos válasz"},
    {"gene": "TNF", "rsid": "rs1800629", "risk_allele": "A", "weight": 1.0,
     "group": "GYULLADÁS", "name": "TNF-α gyulladásos válasz"},
    {"gene": "IL10", "rsid": "rs1800896", "risk_allele": "A", "weight": 1.0,
     "group": "GYULLADÁS", "name": "IL10 gyulladásos válasz"},

    # FUT2 – bélflóra → DAO aktivitás
    {"gene": "FUT2", "rsid": "rs601338", "risk_allele": "A", "weight": 1.5,
     "group": "BÉLFLÓRA", "name": "FUT2 szekretor státusz"},
    {"gene": "FUT2", "rsid": "rs602662", "risk_allele": "A", "weight": 1.0,
     "group": "BÉLFLÓRA", "name": "FUT2 variáns"},
    {"gene": "FUT2", "rsid": "rs492602", "risk_allele": "G", "weight": 1.0,
     "group": "BÉLFLÓRA", "name": "FUT2 variáns"},
]


# ============================================================
# GENOTÍPUS ÉRTELMEZÉS EGY SNP-RE
# ============================================================

def interpret_single_variant(genotype, risk_allele):
    if genotype is None:
        return None, 0, "A variáns nem található a RAW fájlban (nincs adat)."

    alleles = list(genotype)
    risk_count = alleles.count(risk_allele)

    if risk_count == 0:
        text = "Nem hordoz kifejezett kockázati allélt ennél a variánsnál."
    elif risk_count == 1:
        text = "Heterozigóta kockázati allél – enyhén emelkedett genetikai hajlam."
    else:
        text = "Homozigóta kockázati allél – emelkedett genetikai hajlam."

    return genotype, risk_count, text


# ============================================================
# PANEL KIÉRTÉKELÉSE
# ============================================================

def evaluate_histamine_panel(raw_data):
    results = []
    total_weighted_risk = 0.0
    max_weighted_risk = 0.0

    group_scores = {}
    group_max = {}

    for var in VARIANTS:
        rsid = var["rsid"]
        gene = var["gene"]
        risk_allele = var["risk_allele"]
        weight = var["weight"]
        group = var["group"]
        name = var["name"]

        genotype = raw_data.get(rsid)
        genotype, risk_count, interp = interpret_single_variant(genotype, risk_allele)

        weighted = risk_count * weight
        total_weighted_risk += weighted
        max_weighted_risk += 2 * weight  # max: 2 kockázati allél

        group_scores[group] = group_scores.get(group, 0.0) + weighted
        group_max[group] = group_max.get(group, 0.0) + 2 * weight

        explanation = (
            f"A(z) {gene} gén {rsid} variánsa a(z) {name} szempontjából releváns. "
            f"A kockázati allél: {risk_allele}. A genetikai eredmény nem diagnózis, "
            f"csak hajlamot jelez."
        )

        results.append({
            "gene": gene,
            "rsid": rsid,
            "name": name,
            "group": group,
            "risk_allele": risk_allele,
            "genotype": genotype,
            "risk_count": risk_count,
            "weighted_risk": weighted,
            "interpretation": interp,
            "explanation": explanation,
        })

    return results, total_weighted_risk, max_weighted_risk, group_scores, group_max


# ============================================================
# KATEGÓRIA MEGHATÁROZÁSA ÖSSZPONTSZÁM ALAPJÁN
# ============================================================

def classify_overall(ratio):
    if ratio <= 0.20:
        return "ALACSONY hisztaminérzékenységi hajlam"
    elif ratio <= 0.40:
        return "MÉRSÉKELT hisztaminérzékenységi hajlam"
    elif ratio <= 0.70:
        return "KÖZEPESEN EMELKEDETT hisztaminérzékenységi hajlam"
    else:
        return "EMELKEDETT hisztaminérzékenységi hajlam"


def classify_group(ratio):
    if ratio <= 0.20:
        return "inkább kedvező genetikai háttér"
    elif ratio <= 0.40:
        return "enyhén emelkedett genetikai hajlam"
    elif ratio <= 0.70:
        return "közepesen emelkedett genetikai hajlam"
    else:
        return "emelkedett genetikai hajlam"


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_and_save_report(results, filename, total_weighted_risk, max_weighted_risk,
                          group_scores, group_max):
    outname = f"Histamin_panel_eredmeny_{filename}.txt"
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" HISZTAMIN ÉRZÉKENYSÉG – GENETIKAI PANEL")
    add("==============================================\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    # Egyedi variánsok
    for r in results:
        add(f"🔹 {r['name']} ({r['gene']}, {r['rsid']}) – csoport: {r['group']}")
        add(f"   Kockázati allél: {r['risk_allele']}")
        add(f"   Genotípus: {r['genotype']}")
        add(f"   Értelmezés: {r['interpretation']}")
        add(f"   Magyarázat: {r['explanation']}\n")

    if max_weighted_risk == 0:
        add("❌ A panel SNP-jei egyike sem található meg a RAW fájlban.")
        with open(outname, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        add(f"\n💾 Eredmény fájlba mentve: {outname}")
        return

    overall_ratio = total_weighted_risk / max_weighted_risk
    overall_category = classify_overall(overall_ratio)

    bar_length = 30
    filled = int(overall_ratio * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    add("\n==============================================")
    add(" ÖSSZEGZÉS – ÖSSZPONTSZÁM")
    add("==============================================\n")

    add("Hisztaminérzékenységi kockázati pontszám (súlyozott):")
    add(f"[{bar}]  {total_weighted_risk:.1f} / {max_weighted_risk:.1f}\n")
    add(f"Genetikai hajlam kategória: {overall_category}\n")

    add("Megjegyzés:")
    add("- A pontszám a hisztamin lebontás, metiláció, gyulladásos válasz és bélflóra")
    add("  genetikai hátterét együtt értékeli.")
    add("- A genetikai eredmény nem diagnózis, csak hajlamot jelez.\n")

    # Csoportos bontás
    add("==============================================")
    add(" RÉSZLETES CSOPORTOSÍTOTT ÉRTÉKELÉS")
    add("==============================================\n")

    for group, score in group_scores.items():
        gmax = group_max[group]
        if gmax == 0:
            continue
        ratio = score / gmax
        cat = classify_group(ratio)

        gbar_filled = int(ratio * bar_length)
        gbar = "█" * gbar_filled + "░" * (bar_length - gbar_filled)

        add(f"🔸 Csoport: {group}")
        add(f"   Pontszám: {score:.1f} / {gmax:.1f}")
        add(f"   [{gbar}]")
        add(f"   Értelmezés: {cat}\n")

    add("==============================================")
    add(" FONTOS MEGJEGYZÉS")
    add("==============================================\n")
    add("- A hisztaminérzékenység tünetei nem csak genetikától függenek.")
    add("- Az étrend, bélflóra, gyógyszerek, stressz és egyéb tényezők is szerepet játszanak.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Hisztamin érzékenység genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    print(f"\n📄 Elemzett RAW fájl: {filename}\n")

    raw_data = read_raw_data(filename)
    if not raw_data:
        print("❌ Nem sikerült beolvasni a RAW fájlt.")
        return

    results, total_weighted_risk, max_weighted_risk, group_scores, group_max = evaluate_histamine_panel(raw_data)
    print_and_save_report(results, filename, total_weighted_risk, max_weighted_risk, group_scores, group_max)


if __name__ == "__main__":
    run()
