# -*- coding: utf-8 -*-
"""
============================================================
 ALLERGIA HAJLAM – GENETIKAI PANEL
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki azokat a
 genetikai variánsokat, amelyek az alábbi allergiás
 hajlamokkal hozhatók összefüggésbe:

 - Általános allergiás hajlam (IgE szint)
 - Pollen allergia hajlam
 - Poratka allergia hajlam
 - Ételallergia hajlam (mogyoró, tojás, tejfehérje)
 - Asztma genetikai hajlam
 - Bőrallergia / ekcéma hajlam

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
# SNP LISTA – ALLERGIA HAJLAM
# ============================================================

VARIANTS = [

    # --------------------------------------------------------
    # ÁLTALÁNOS ALLERGIÁS HAJLAM (IgE SZINT)
    # --------------------------------------------------------
    {"group": "IGE SZINT", "gene": "FCER1A", "rsid": "rs2251746", "risk_allele": "T", "weight": 3.0},
    {"group": "IGE SZINT", "gene": "IL13",   "rsid": "rs20541",   "risk_allele": "A", "weight": 2.0},

    # --------------------------------------------------------
    # POLLEN ALLERGIA
    # --------------------------------------------------------
    {"group": "POLLEN", "gene": "HLA-DQ", "rsid": "rs9273349", "risk_allele": "A", "weight": 2.5},
    {"group": "POLLEN", "gene": "IL4",    "rsid": "rs2243250", "risk_allele": "T", "weight": 2.0},

    # --------------------------------------------------------
    # PORATKA ALLERGIA
    # --------------------------------------------------------
    {"group": "PORATKA", "gene": "TLR4", "rsid": "rs4986790", "risk_allele": "A", "weight": 2.0},
    {"group": "PORATKA", "gene": "HLA-DQ", "rsid": "rs9271366", "risk_allele": "C", "weight": 1.5},

    # --------------------------------------------------------
    # ÉTELALLERGIA (mogyoró, tojás, tejfehérje)
    # --------------------------------------------------------
    {"group": "ÉTEL", "gene": "IL10",  "rsid": "rs1800896", "risk_allele": "A", "weight": 2.0},
    {"group": "ÉTEL", "gene": "STAT6", "rsid": "rs324011",  "risk_allele": "T", "weight": 2.0},
    {"group": "ÉTEL", "gene": "HLA",   "rsid": "rs9275596", "risk_allele": "A", "weight": 1.5},

    # --------------------------------------------------------
    # ASZTMA HAJLAM
    # --------------------------------------------------------
    {"group": "ASZTMA", "gene": "ORMDL3", "rsid": "rs7216389", "risk_allele": "T", "weight": 3.0},
    {"group": "ASZTMA", "gene": "IL33",    "rsid": "rs928413",  "risk_allele": "A", "weight": 2.0},

    # --------------------------------------------------------
    # BŐRALLERGIA / EKCÉMA
    # --------------------------------------------------------
    {"group": "EKCÉMA", "gene": "FLG",  "rsid": "rs61816761", "risk_allele": "A", "weight": 3.0},
    {"group": "EKCÉMA", "gene": "TSLP", "rsid": "rs3806933",  "risk_allele": "T", "weight": 2.0},
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
        return "ALACSONY allergiahajlam"
    if r <= 0.40:
        return "MÉRSÉKELT allergiahajlam"
    if r <= 0.70:
        return "KÖZEPESEN EMELKEDETT allergiahajlam"
    return "EMELKEDETT allergiahajlam"


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max):
    outname = f"Allergia_hajlam_panel_eredmeny_{filename}.txt"
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" ALLERGIA HAJLAM – GENETIKAI PANEL")
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
    add("- Az allergiás hajlam genetikai és környezeti tényezők kombinációja.")
    add("- A környezet, étrend, immunrendszer állapota nagy szerepet játszik.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Allergia hajlam genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    raw_data = read_raw_data(filename)
    results, total_weighted, max_weighted, group_scores, group_max = evaluate_panel(raw_data)
    print_and_save_report(results, filename, total_weighted, max_weighted, group_scores, group_max)


if __name__ == "__main__":
    run()
