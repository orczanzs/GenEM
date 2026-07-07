# -*- coding: utf-8 -*-
"""
============================================================
 SPORT HAJLAM – GENETIKAI PANEL
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki azokat a
 genetikai variánsokat, amelyek a sportteljesítménnyel,
 izomrost-típussal, állóképességgel, regenerációval és
 energiafelhasználással kapcsolatosak.

 A panel NEM diagnózis, csak genetikai hajlamot jelez.
============================================================
"""

import os
import csv

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
# SNP LISTA – SPORT HAJLAM
# ============================================================

VARIANTS = [
    # IZOMROST-TÍPUS (sprinter vs állóképesség)
    {"gene": "ACTN3", "rsid": "rs1815739", "risk_allele": "T", "weight": 3.0, "group": "IZOMROST"},
    {"gene": "ACE", "rsid": "rs4343", "risk_allele": "A", "weight": 2.0, "group": "IZOMROST"},

    # ÁLLÓKÉPESSÉG / VO2max
    {"gene": "PPARGC1A", "rsid": "rs8192678", "risk_allele": "A", "weight": 2.5, "group": "ÁLLÓKÉPESSÉG"},
    {"gene": "NOS3", "rsid": "rs1799983", "risk_allele": "T", "weight": 2.0, "group": "ÁLLÓKÉPESSÉG"},
    {"gene": "VEGFA", "rsid": "rs2010963", "risk_allele": "C", "weight": 1.5, "group": "ÁLLÓKÉPESSÉG"},

    # REGENERÁCIÓ / GYULLADÁS / SÉRÜLÉKENYSÉG
    {"gene": "IL6", "rsid": "rs1800795", "risk_allele": "C", "weight": 2.0, "group": "REGENERÁCIÓ"},
    {"gene": "TNF", "rsid": "rs1800629", "risk_allele": "A", "weight": 1.5, "group": "REGENERÁCIÓ"},
    {"gene": "COL5A1", "rsid": "rs12722", "risk_allele": "T", "weight": 1.5, "group": "REGENERÁCIÓ"},
    {"gene": "MSTN", "rsid": "rs1805086", "risk_allele": "A", "weight": 1.5, "group": "REGENERÁCIÓ"},

    # ZSÍRÉGETÉS / ENERGIAFELHASZNÁLÁS
    {"gene": "ADRB2", "rsid": "rs1042713", "risk_allele": "A", "weight": 2.0, "group": "METABOLIZMUS"},
    {"gene": "ADRB3", "rsid": "rs4994", "risk_allele": "C", "weight": 2.0, "group": "METABOLIZMUS"},
    {"gene": "PPARA", "rsid": "rs4253778", "risk_allele": "G", "weight": 1.5, "group": "METABOLIZMUS"},
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
# KATEGÓRIA
# ============================================================

def classify_ratio(r):
    if r <= 0.20:
        return "ALACSONY sporthajlam"
    if r <= 0.40:
        return "MÉRSÉKELT sporthajlam"
    if r <= 0.70:
        return "KÖZEPESEN EMELKEDETT sporthajlam"
    return "EMELKEDETT sporthajlam"


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max):
    outname = f"Sport_hajlam_panel_eredmeny_{filename}.txt"
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" SPORT HAJLAM – GENETIKAI PANEL")
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
    add("- A sportteljesítmény genetikai és környezeti tényezők kombinációja.")
    add("- Az edzés, étrend, pihenés és életmód nagy szerepet játszik.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Sport hajlam genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    raw_data = read_raw_data(filename)
    results, total_weighted, max_weighted, group_scores, group_max = evaluate_panel(raw_data)
    print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max)


if __name__ == "__main__":
    run()
