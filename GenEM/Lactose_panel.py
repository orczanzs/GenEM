# -*- coding: utf-8 -*-
"""
============================================================
 LAKTÓZ INTOLERANCIA – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki az rs4988235
 variánst (LCT gén), amely a laktáz enzim aktivitásával és a
 laktóztoleranciával áll összefüggésben.

 A panel NEM diagnózis, csak genetikai hajlamot jelez.
============================================================
"""

import os
import csv

# ============================================================
# AUTOMATIKUS MYHERITAGE FÁJLVÁLASZTÓ
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

def load_myheritage_genotypes(filename):
    """Beolvassa a MyHeritage RAW CSV fájlt és visszaadja a genotípusokat."""
    genotypes = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if not row or row[0].startswith("#"):
                    continue
                if len(row) < 4:
                    continue
                rsid = row[0].strip()
                genotype = row[3].strip().upper()
                genotypes[rsid] = genotype
    except FileNotFoundError:
        print(f"❌ A fájl nem található: {filename}")
    return genotypes


# ============================================================
# LAKTÓZ PANEL VARIÁNSOK
# ============================================================

VARIANTS = [
    {"gene": "LCT", "rsid": "rs4988235", "risk_allele": "C",
     "name": "Laktáz enzim aktivitás (LCT gén)", "category": "emésztés"},
]


# ============================================================
# GENOTÍPUS ÉRTELMEZÉS
# ============================================================

def interpret_genotype(genotype, risk_allele):
    """Értelmezi a laktózérzékenységhez kapcsolódó genotípust."""
    if genotype is None:
        return None, "A variáns nem található a RAW fájlban (nincs adat)."

    alleles = list(genotype)
    risk_count = alleles.count(risk_allele)

    if risk_count == 0:
        text = "Genetikailag valószínűleg laktóztoleráns (T/T)."
    elif risk_count == 1:
        text = "Részleges tolerancia (C/T heterozigóta)."
    else:
        text = "Genetikailag hajlamos laktózérzékenységre (C/C)."

    return risk_count, text


def evaluate_variants(genotypes):
    """Kiértékeli a panel variánsait."""
    results = []
    for var in VARIANTS:
        rsid = var["rsid"]
        genotype = genotypes.get(rsid)
        risk_count, interp = interpret_genotype(genotype, var["risk_allele"])

        explanation = (
            f"A(z) {var['gene']} gén {rsid} variánsa befolyásolja a laktáz enzim "
            f"termelését. A genetikai eredmény nem diagnózis, csak hajlamot jelez."
        )

        results.append({
            "gene": var["gene"],
            "rsid": rsid,
            "name": var["name"],
            "category": var["category"],
            "risk_allele": var["risk_allele"],
            "genotype": genotype,
            "risk_count": risk_count,
            "interpretation": interp,
            "explanation": explanation,
        })
    return results


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_report(results, filename):
    """Kinyomtatja és fájlba menti a laktóz panel eredményeit."""
    outname = f"Lactose_panel_eredmeny_{filename}.txt"
    output = []

    def add(line=""):
        print(line)
        output.append(line)

    add("==============================📋")
    add(" LAKTÓZ INTOLERANCIA PANEL 📋")
    add("==============================📋\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    for r in results:
        add(f"🔹 {r['name']} ({r['gene']}, {r['rsid']})")
        add(f"   Kategória: {r['category']}")
        add(f"   Kockázati allél: {r['risk_allele']}")
        add(f"   Genotípus: {r['genotype']}")
        add(f"   Értelmezés: {r['interpretation']}")
        add(f"   Magyarázat: {r['explanation']}\n")

    available = [r for r in results if r["risk_count"] is not None]

    if not available:
        add("❌ Egyik vizsgált variánsra sincs adat a RAW fájlban.")
        return

    total_risk = sum(r["risk_count"] for r in available)
    max_risk = len(available) * 2

    bar_length = 20
    filled = int((total_risk / max_risk) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    add("\n==============================📋")
    add(" ÖSSZEGZÉS – Genetikai hajlam 📋")
    add("==============================📋\n")

    add("Kockázati allélok összesítése:")
    add(f"[{bar}] {total_risk} / {max_risk}\n")

    ratio = total_risk / max_risk

    if ratio <= 0.20:
        category = "ALACSONY"
    elif ratio <= 0.40:
        category = "MÉRSÉKELT"
    elif ratio <= 0.70:
        category = "KÖZEPESEN EMELKEDETT"
    else:
        category = "MAGAS"

    add(f"Genetikai hajlam kategória: {category}\n")
    add("Ez az értékelés csak a laktáz enzim aktivitásra vonatkozik.")
    add("A genetikai eredmény nem diagnózis.\n")

    add(f"📄 Elemzett fájl: {filename}\n")

    add("GENE     RSID          RISK  GENOTÍPUS   KOCKÁZAT 📋")
    add("---------------------------------------------------📋")
    for r in results:
        genotype = r['genotype'] if r['genotype'] is not None else "nincs adat"
        rc = r['risk_count'] if r['risk_count'] is not None else "-"
        add(f"{r['gene']:<8} {r['rsid']:<12} {r['risk_allele']:<5} {genotype:<10} {rc}")

    with open(outname, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    add(f"\n💾 Eredmény fájlba mentve: {outname}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Laktóz intolerancia panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    print(f"\n📄 Elemzett RAW fájl: {filename}\n")

    genotypes = load_myheritage_genotypes(filename)
    if not genotypes:
        print("❌ Nem sikerült beolvasni a fájlt.")
        return

    results = evaluate_variants(genotypes)
    print_report(results, filename)


if __name__ == "__main__":
    run()
