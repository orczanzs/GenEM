#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATÓPIÁS DERMATITIS – SÚLYOZOTT GENETIKAI PANEL
GitHub‑kompatibilis, rendezett, átlátható verzió

Használat:
  - Interaktív fájlválasztó: futtasd a scriptet argumentum nélkül.
  - Parancssori fájl megadása: python atopias_dermatitis_panel.py --file MyHeritage_raw_dna.csv
  - Kimeneti mappa megadása: --outdir eredmeny_custom

A kód nem diagnosztikai eszköz. Csak tájékoztató jellegű genetikai hajlam‑értékelés.
"""

from __future__ import annotations
import os
import csv
import datetime
import argparse
import sys
from typing import Dict, List, Optional, Any

__version__ = "1.0.0"

# ============================================================
# VARIÁNS DEFINÍCIÓK – SÚLYOZOTT PANEL
# (Szükség szerint bővíthető, források dokumentálandók a README-ben)
# ============================================================

VARIANTS = [
    {"gene": "FLG", "rsid": "rs61816761", "risk_allele": "A",
     "name": "FLG variáns (bőrgát működés)", "category": "bőrgát", "weight": 2},

    {"gene": "FLG", "rsid": "rs558269137", "risk_allele": "T",
     "name": "FLG loss-of-function", "category": "bőrgát", "weight": 3},

    {"gene": "IL4R", "rsid": "rs1801275", "risk_allele": "G",
     "name": "IL4R variáns (Th2 immunválasz)", "category": "immunválasz", "weight": 1},

    {"gene": "IL13", "rsid": "rs20541", "risk_allele": "A",
     "name": "IL13 variáns (allergiás gyulladás)", "category": "immunválasz", "weight": 1},

    {"gene": "TSLP", "rsid": "rs1837253", "risk_allele": "C",
     "name": "TSLP variáns", "category": "immunválasz", "weight": 1},

    {"gene": "OVOL1", "rsid": "rs6087990", "risk_allele": "G",
     "name": "OVOL1 variáns", "category": "bőrgát", "weight": 1},

    {"gene": "KIF3A", "rsid": "rs12186803", "risk_allele": "A",
     "name": "KIF3A variáns", "category": "bőrgát", "weight": 1},

    {"gene": "CARD11", "rsid": "rs11236797", "risk_allele": "T",
     "name": "CARD11 variáns", "category": "immunválasz", "weight": 1},
]


# ============================================================
# AUTOMATIKUS MYHERITAGE FÁJLVÁLASZTÓ
# ============================================================

def select_raw_file() -> Optional[str]:
    """Kilistázza a mappában található MyHeritage RAW CSV fájlokat és interaktív választást ad."""
    try:
        candidates = [
            f for f in os.listdir(".")
            if f.lower().endswith(".csv") and "myheritage" in f.lower()
        ]
    except FileNotFoundError:
        print("❌ Nem található a munkakönyvtár.")
        return None

    if not candidates:
        print("❌ Nem található MyHeritage RAW DNA fájl a mappában.")
        return None

    print("\n📂 Elérhető MyHeritage RAW fájlok:")
    for i, fname in enumerate(candidates, start=1):
        print(f"  {i}. {fname}")

    while True:
        try:
            choice = input("\nVálassz fájlt (szám) vagy 'q' kilépéshez: ").strip()
            if choice.lower() == "q":
                return None
            idx = int(choice)
            if 1 <= idx <= len(candidates):
                return candidates[idx - 1]
            print("Érvénytelen választás.")
        except ValueError:
            print("Számot adj meg.")


# ============================================================
# RAW BEOLVASÁS
# ============================================================

def load_myheritage_genotypes(filename: str) -> Dict[str, str]:
    """
    Beolvassa a MyHeritage RAW CSV fájlt és visszaadja a genotípusokat rsid -> genotype formában.
    Támogat egyszerű CSV formátumot: rsid, chromosome, position, genotype (vagy hasonló).
    """
    genotypes: Dict[str, str] = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # Próbálunk DictReader-rel rugalmasan dolgozni, de ha nincs fejléc, visszatérünk sima reader-rel
            sample = f.read(2048)
            f.seek(0)
            has_header = "rsid" in sample.lower() or "rs_id" in sample.lower()
            if has_header:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row:
                        continue
                    # többféle lehetséges kulcs kezelése
                    rsid = row.get("rsid") or row.get("rs_id") or row.get("SNP") or row.get("name")
                    genotype = row.get("genotype") or row.get("gen") or row.get("call") or row.get("genotype_call")
                    if rsid and genotype:
                        genotypes[rsid.strip()] = genotype.strip().upper()
            else:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].startswith("#"):
                        continue
                    if len(row) < 4:
                        # ha kevesebb oszlop, próbáljuk a 0 és utolsó oszlopot
                        if len(row) >= 2:
                            rsid = row[0].strip()
                            genotype = row[-1].strip().upper()
                        else:
                            continue
                    else:
                        rsid = row[0].strip()
                        genotype = row[3].strip().upper()
                    if rsid:
                        genotypes[rsid] = genotype
    except FileNotFoundError:
        print(f"❌ A fájl nem található: {filename}")
    except Exception as e:
        print(f"❌ Hiba a fájl beolvasásakor: {e}")
    return genotypes


# ============================================================
# GENOTÍPUS ÉRTELMEZÉS
# ============================================================

def interpret_genotype(genotype: Optional[str], risk_allele: str) -> (Optional[int], str):
    """Értelmezi, hogy a genotípus hány kockázati allélt tartalmaz."""
    if genotype is None or genotype == "":
        return None, "A variáns nem található a RAW fájlban (nincs adat)."

    # Tisztítás: csak betűket tartunk meg (pl. 'AA', 'AG', 'A/G' -> 'AG')
    cleaned = "".join(ch for ch in genotype if ch.isalpha()).upper()
    if not cleaned:
        return None, "Érvénytelen genotípus formátum."

    alleles = list(cleaned)
    risk_count = alleles.count(risk_allele.upper())

    if risk_count == 0:
        text = "Nem hordoz kockázati allélt."
    elif risk_count == 1:
        text = "Heterozigóta hordozó (1 kockázati allél)."
    else:
        text = "Homozigóta hordozó (2 kockázati allél)."

    return risk_count, text


def evaluate_variants(genotypes: Dict[str, str]) -> List[Dict[str, Any]]:
    """Kiértékeli az összes variánst és visszaadja az eredménylistát."""
    results: List[Dict[str, Any]] = []
    for var in VARIANTS:
        rsid = var["rsid"]
        genotype = genotypes.get(rsid)
        risk_count, interp = interpret_genotype(genotype, var["risk_allele"])

        explanation = (
            f"A(z) {var['gene']} gén {rsid} variánsa összefüggésbe hozható az "
            f"atópiás dermatitis bizonyos formáival. A súlyozás szakirodalmi "
            f"hatáserősség alapján történt, de nem diagnosztikai értékű."
        )

        results.append({
            "gene": var["gene"],
            "rsid": rsid,
            "name": var["name"],
            "category": var["category"],
            "risk_allele": var["risk_allele"],
            "genotype": genotype,
            "risk_count": risk_count,
            "weight": var["weight"],
            "interpretation": interp,
            "explanation": explanation,
        })
    return results


# ============================================================
# RIPORT + SÚLYOZOTT ÖSSZEGZÉS + FÁJLBA MENTÉS
# ============================================================

def print_report(results: List[Dict[str, Any]], filename: str, outdir: str = "eredmeny") -> str:
    """Kinyomtatja és fájlba menti a súlyozott eredményeket az outdir mappába. Visszaadja a mentett fájl elérési útját."""
    os.makedirs(outdir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outname = f"atopias_dermatitis_{timestamp}.txt"
    outpath = os.path.join(outdir, outname)
    output_lines: List[str] = []

    def add(line: str = ""):
        print(line)
        output_lines.append(line)

    add("==============================📋")
    add(" SÚLYOZOTT ATÓPIÁS DERMATITIS PANEL 📋")
    add("==============================📋\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    for r in results:
        add(f"🔹 {r['name']} ({r['gene']}, {r['rsid']})")
        add(f"   Kategória: {r['category']}")
        add(f"   Kockázati allél: {r['risk_allele']}")
        add(f"   Genotípus: {r['genotype']}")
        add(f"   Értelmezés: {r['interpretation']}")
        add(f"   Súly: {r['weight']}")
        add(f"   Magyarázat: {r['explanation']}\n")

    available = [r for r in results if r["risk_count"] is not None]

    if not available:
        add("❌ Egyik vizsgált variánsra sincs adat a RAW fájlban.")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        add(f"\n💾 Eredmény fájlba mentve: {outpath}")
        return outpath

    weighted_risk = sum(r["risk_count"] * r["weight"] for r in available)
    max_weighted = sum(2 * r["weight"] for r in available)

    bar_length = 20
    filled = int((weighted_risk / max_weighted) * bar_length) if max_weighted > 0 else 0
    bar = "█" * filled + "░" * (bar_length - filled)

    add("\n==============================📋")
    add(" ÖSSZEGZÉS – Súlyozott genetikai hajlam 📋")
    add("==============================📋\n")

    add("Súlyozott kockázati pontszám:")
    add(f"[{bar}] {weighted_risk} / {max_weighted}\n")

    ratio = (weighted_risk / max_weighted) if max_weighted > 0 else 0

    if ratio <= 0.20:
        category = "ALACSONY"
    elif ratio <= 0.40:
        category = "MÉRSÉKELT"
    elif ratio <= 0.70:
        category = "KÖZEPESEN EMELKEDETT"
    else:
        category = "MAGAS"

    add(f"Genetikai hajlam kategória: {category}\n")

    add("FONTOS: A súlyozás szakirodalmi hatáserősség alapján történt.")
    add("Ez a panel nem diagnózis, csak genetikai hajlamot jelez.")
    add("Atópiás dermatitis akkor is előfordulhat, ha a genetikai kockázat alacsony.\n")

    add(f"📄 Elemzett fájl: {filename}\n")

    add("GENE     RSID          RISK  GENOTÍPUS   KOCKÁZAT   SÚLY   📋")
    add("---------------------------------------------------------------📋")
    for r in results:
        genotype = r['genotype'] if r['genotype'] is not None else "nincs adat"
        rc = r['risk_count'] if r['risk_count'] is not None else "-"
        add(f"{r['gene']:<8} {r['rsid']:<12} {r['risk_allele']:<5} {genotype:<10} {rc:<10} {r['weight']}")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    add(f"\n💾 Eredmény fájlba mentve: {outpath}")
    return outpath


# ============================================================
# FUTTATÁS / CLI
# ============================================================

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Súlyozott atópiás dermatitis genetikai panel - MyHeritage RAW CSV feldolgozó"
    )
    p.add_argument("--file", "-f", help="MyHeritage RAW CSV fájl (ha nincs megadva, interaktív választó indul).")
    p.add_argument("--outdir", "-o", default="eredmeny", help="Kimeneti mappa a .txt fájloknak (alap: eredmeny).")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p.parse_args(argv)


def run(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    if args.file:
        filename = args.file
        if not os.path.isfile(filename):
            print(f"❌ A megadott fájl nem található: {filename}")
            return 2
    else:
        filename = select_raw_file()
        if filename is None:
            print("Kilépés.")
            return 0

    print(f"\n📄 Elemzett RAW fájl: {filename}\n")

    genotypes = load_myheritage_genotypes(filename)
    if not genotypes:
        print("⚠️ Figyelem: nem sikerült genotípus adatokat beolvasni vagy a fájl üres volt.")

    results = evaluate_variants(genotypes)
    try:
        outpath = print_report(results, filename, outdir=args.outdir)
        print(f"\nKész. A jelentés elérhető: {outpath}")
    except Exception as e:
        print(f"❌ Hiba a jelentés mentésekor: {e}")
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(run())
