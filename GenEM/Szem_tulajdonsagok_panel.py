# -*- coding: utf-8 -*-
"""
============================================================
 SZEM TULAJDONSÁGOK – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki a szemszínnel,
 pigmentációval és fényérzékenységgel összefüggő SNP-ket.

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
            rsid = row[0].strip().replace('"', '')
            genotype = row[3].strip().replace('"', '').upper()
            data[rsid] = genotype
    return data


# ============================================================
# SZEM PANEL SNP-K
# (a te eredeti 3 SNP-d + bővített, szakmailag releváns készlet)
# ============================================================

EYE_SNPS = {
    # Eredeti logikádhoz használt SNP-k
    "rs1129038": {"gene": "HERC2", "role": "alapszín", "weight": 3.0},
    "rs916977": {"gene": "HERC2", "role": "moduláló", "weight": 2.0},
    "rs1667394": {"gene": "HERC2", "role": "pigmentáció", "weight": 2.0},

    # Bővített készlet – OCA2 / HERC2 / SLC24A4 / TYR / IRF4
    "rs12913832": {"gene": "HERC2", "role": "fő szemszín SNP", "weight": 4.0},
    "rs1800407": {"gene": "OCA2", "role": "zöld/mogyoró árnyalat", "weight": 2.0},
    "rs7495174": {"gene": "OCA2", "role": "pigmentáció", "weight": 1.5},
    "rs4778138": {"gene": "OCA2", "role": "pigmentáció", "weight": 1.5},
    "rs4778241": {"gene": "OCA2", "role": "pigmentáció", "weight": 1.5},
    "rs12896399": {"gene": "SLC24A4", "role": "világos szem támogatás", "weight": 1.5},
    "rs1393350": {"gene": "TYR", "role": "pigmentáció", "weight": 1.5},
    "rs12203592": {"gene": "IRF4", "role": "világos szem + szeplők", "weight": 1.5},
}


# ============================================================
# SEGÉDFÜGGVÉNYEK – SZEMSZÍN, FÉNYÉRZÉKENYSÉG, PROFIL
# (a te eredeti logikád megőrizve, kiegészítve)
# ============================================================

def estimate_light_sensitivity(label):
    if label == "világos":
        return "Magas fényérzékenység."
    if label == "köztes":
        return "Közepes fényérzékenység."
    if label in ["barna", "sötét"]:
        return "Alacsonyabb fényérzékenység."
    if label in ["zöld/mogyoró", "zöld"]:
        return "Közepes–enyhén emelkedett fényérzékenység."
    return "Nincs adat."


def eye_color_probabilities(label):
    if label == "barna":
        return "Barna ~70%, Zöld ~20%, Kék ~10%"
    if label in ["zöld/mogyoró", "zöld"]:
        return "Zöld/Mogyoró ~60%, Barna ~25%, Kék ~15%"
    if label == "világos":
        return "Kék ~60%, Zöld ~30%, Mogyoró ~10%"
    if label == "köztes":
        return "Zöld ~40%, Mogyoró ~40%, Barna ~20%"
    return "Nem becsülhető."


def eye_type_and_profile(label):
    if label in ["barna", "sötét"]:
        return ("Sötét pigmentáció.", "Több melanin → jobb fényvédelem, alacsonyabb fényérzékenység.")
    if label in ["zöld/mogyoró", "zöld", "köztes"]:
        return ("Köztes pigmentáció.", "Közepes melanin → kiegyensúlyozott, de néha fokozott fényérzékenység.")
    if label == "világos":
        return ("Világos pigmentáció.", "Kevés melanin → fokozott fényérzékenység, erősebb fényvédelem javasolt.")
    return ("Nem meghatározható.", "Nincs elegendő adat a részletes profilhoz.")


# ============================================================
# SZEMSZÍN ÉRTELMEZÉS – A TE EREDETI LOGIKÁDRA ÉPÍTVE
# ============================================================

def interpret_eye_color_core(rs1129, rs9169, rs1667):
    """A te eredeti 3 SNP-s logikád, egységesítve."""
    available = sum(1 for x in [rs1129, rs9169, rs1667] if x != "N/A")

    if available == 0:
        return None, "Nincs elegendő adat a három fő marker alapján."

    # 1 marker esetén
    if available == 1:
        if rs9169 != "N/A":
            if rs9169 == "TT":
                label = "világos"
            elif rs9169 == "TC":
                label = "köztes"
            else:
                label = "barna"
        elif rs1667 != "N/A":
            if rs1667 == "TT":
                label = "világos"
            elif rs1667 == "CT":
                label = "köztes"
            else:
                label = "barna"
        else:
            # csak rs1129038 van
            if rs1129 == "AA":
                label = "világos"
            elif rs1129 == "AG":
                label = "köztes"
            else:
                label = "barna"
        return label, "A becslés egyetlen marker alapján történt, bizonytalanság magasabb."

    # 2 marker esetén
    if available == 2:
        if rs9169 in ["TT", "TC"] and rs1667 in ["TT", "CT"]:
            label = "zöld/mogyoró"
        elif rs9169 == "CC" and rs1667 == "CC":
            label = "barna"
        else:
            label = "köztes"
        return label, "A becslés két marker kombinációja alapján történt."

    # 3 marker esetén – eredeti logikád
    if rs1129 == "AA":
        base_label = "világos"
    elif rs1129 == "AG":
        base_label = "köztes"
    else:
        base_label = "barna"

    if base_label == "világos":
        label = "világos"
    elif base_label == "köztes":
        label = "zöld/mogyoró"
    else:
        label = "barna"

    return label, "A becslés három marker kombinációja alapján történt."


# ============================================================
# BŐVÍTETT SNP-K FIGYELEMBEVÉTELE
# ============================================================

def refine_with_extended_snps(label, raw_data):
    """
    A bővített SNP-k alapján finomítja a szemszín-becslést.
    Nem írja felül teljesen az alap becslést, csak módosíthatja.
    """
    # HERC2 rs12913832 – nagyon erős hatás
    h129 = raw_data.get("rs12913832", None)
    if h129:
        if h129 in ["AA"]:
            # erősen világosító
            if label in ["barna", "köztes"]:
                label = "zöld/mogyoró"
            elif label in ["zöld/mogyoró", "zöld"]:
                label = "világos"
            else:
                label = "világos"
        elif h129 in ["AG"]:
            # enyhe világosítás
            if label == "barna":
                label = "köztes"

    # OCA2 rs1800407 – zöld/mogyoró irány
    o180 = raw_data.get("rs1800407", None)
    if o180 and "T" in o180:
        if label == "barna":
            label = "zöld/mogyoró"
        elif label == "köztes":
            label = "zöld/mogyoró"

    # SLC24A4 rs12896399 – világos szem támogatás
    s128 = raw_data.get("rs12896399", None)
    if s128 and "T" in s128:
        if label in ["köztes", "zöld/mogyoró"]:
            label = "világos"

    return label


# ============================================================
# PANEL KIÉRTÉKELÉSE
# ============================================================

def evaluate_eye_panel(raw_data):
    """
    Visszaadja:
    - összefoglaló szemszín-becslést
    - részletes SNP lista genotípussal
    """
    rs1129 = raw_data.get("rs1129038", "N/A")
    rs9169 = raw_data.get("rs916977", "N/A")
    rs1667 = raw_data.get("rs1667394", "N/A")

    base_label, base_note = interpret_eye_color_core(rs1129, rs9169, rs1667)

    if base_label is None:
        final_label = None
    else:
        final_label = refine_with_extended_snps(base_label, raw_data)

    probs = eye_color_probabilities(final_label) if final_label else "Nem becsülhető."
    sens = estimate_light_sensitivity(final_label) if final_label else "Nincs adat."
    t1, t2 = eye_type_and_profile(final_label) if final_label else ("Nem meghatározható.", "Nincs elegendő adat.")

    # SNP lista
    snp_results = []
    for rsid, meta in EYE_SNPS.items():
        genotype = raw_data.get(rsid, "N/A")
        snp_results.append({
            "rsid": rsid,
            "gene": meta["gene"],
            "role": meta["role"],
            "weight": meta["weight"],
            "genotype": genotype
        })

    summary_text = {
        "base_label": base_label,
        "final_label": final_label,
        "base_note": base_note,
        "probabilities": probs,
        "sensitivity": sens,
        "type_line": t1,
        "profile_line": t2,
        "snp_results": snp_results,
        "rs1129": rs1129,
        "rs9169": rs9169,
        "rs1667": rs1667,
    }

    return summary_text


# ============================================================
# RIPORT + TXT MENTÉS
# ============================================================

def print_and_save_eye_report(summary, filename):
    out_name = f"Szem_tulajdonsagok_panel_eredmeny_{filename}.txt"
    lines = []

    def add(line=""):
        print(line)
        lines.append(line)

    add("==============================================")
    add(" SZEM TULAJDONSÁGOK – GENETIKAI PANEL")
    add("==============================================\n")

    add(f"📄 Elemzett RAW fájl: {filename}\n")

    if summary["final_label"] is None:
        add("A szükséges fő markerek (rs1129038, rs916977, rs1667394) nem állnak rendelkezésre.")
        add("A szemszín genetikai becslése nem végezhető el.\n")
    else:
        add("=== ÖSSZEFOGLALÓ BECSLÉS ===\n")
        add(f"Alap becslés (3 marker alapján): {summary['base_label']}")
        add(f"Megjegyzés: {summary['base_note']}")
        add(f"Finomított becslés (bővített SNP-k figyelembevételével): {summary['final_label']}\n")
        add(f"Valószínűségi eloszlás: {summary['probabilities']}")
        add(f"Fényérzékenység: {summary['sensitivity']}")
        add(f"{summary['type_line']}")
        add(f"{summary['profile_line']}\n")

        add("=== FŐ MARKEREK GENOTÍPUSAI ===")
        add(f"rs1129038 (HERC2): {summary['rs1129']}")
        add(f"rs916977 (HERC2): {summary['rs9169']}")
        add(f"rs1667394 (HERC2): {summary['rs1667']}\n")

    add("=== RÉSZLETES SNP LISTA ===\n")
    for r in summary["snp_results"]:
        add(f"{r['rsid']} ({r['gene']}) – szerep: {r['role']}")
        add(f"   Genotípus: {r['genotype']}, súly: {r['weight']}\n")

    add("==============================================")
    add(" FONTOS MEGJEGYZÉS")
    add("==============================================\n")
    add("- A szemszín és fényérzékenység nem csak genetikától függ.")
    add("- A környezeti tényezők, életkor, hormonális állapot is befolyásolhatják a megjelenést.")
    add("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    with open(out_name, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    add(f"\n💾 Eredmény fájlba mentve: {out_name}")


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("\n=== Szem tulajdonságok genetikai panel ===")

    filename = select_raw_file()
    if filename is None:
        return

    print(f"\n📄 Elemzett RAW fájl: {filename}\n")

    raw_data = read_raw_data(filename)
    if not raw_data:
        print("❌ Nem sikerült beolvasni a RAW fájlt.")
        return

    summary = evaluate_eye_panel(raw_data)
    print_and_save_eye_report(summary, filename)


if __name__ == "__main__":
    run()
