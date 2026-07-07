import csv
import os
import datetime

# ---------------------------------------------------------
# 50 karakter széles progress bar
# ---------------------------------------------------------
def progress_bar(value, max_value, length=50):
    if max_value <= 0:
        return "░" * length
    ratio = max(0.0, min(1.0, value / max_value))
    filled = int(ratio * length)
    empty = length - filled
    return "█" * filled + "░" * empty


# ---------------------------------------------------------
# RAW fájl betöltése – automatikus listázás
# ---------------------------------------------------------
def load_raw_file():
    raw_files = [f for f in os.listdir() if f.lower().endswith(".csv") or f.lower().endswith(".txt")]

    if not raw_files:
        print("Nem találtam RAW fájlt a mappában.")
        return None

    print("\nElérhető RAW fájlok:")
    for i, f in enumerate(raw_files, start=1):
        print(f"{i}) {f}")

    valasztas = input("\nAdd meg a fájl sorszámát: ")

    try:
        index = int(valasztas) - 1
        return raw_files[index]
    except (ValueError, IndexError):
        print("Érvénytelen választás.")
        return None


# ---------------------------------------------------------
# RAW fájl beolvasása – CSV vagy TXT automatikus felismerés
# ---------------------------------------------------------
def read_raw_data(file_path):
    data = {}
    delimiter = "," if file_path.lower().endswith(".csv") else "\t"

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if len(row) >= 4 and not row[0].startswith("#"):
                rsid, chrom, pos, genotype = row
                data[rsid] = genotype

    return data


# ---------------------------------------------------------
# Egyszerű pontszám (0–2) kockázati allél alapján
# ---------------------------------------------------------
def score_from_genotype(genotype, risk_allele):
    if genotype is None:
        return 0
    count = genotype.count(risk_allele)
    if count >= 2:
        return 2
    elif count == 1:
        return 1
    return 0


# ---------------------------------------------------------
# Szöveges kategória pontszám alapján
# ---------------------------------------------------------
def category_from_score(score):
    if score >= 2:
        return "Erős genetikai hatás"
    elif score == 1:
        return "Mérsékelt genetikai hajlam"
    else:
        return "Gyenge genetikai hatás"


# ---------------------------------------------------------
# A panel futtatása
# ---------------------------------------------------------
def run():
    print("\n==============================================")
    print(" LÁTHATÓ TULAJDONSÁGOK PANEL")
    print("==============================================\n")

    raw_path = load_raw_file()
    if not raw_path:
        return

    raw = read_raw_data(raw_path)
    datum = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append("==============================================")
    lines.append(" LÁTHATÓ TULAJDONSÁGOK PANEL")
    lines.append("==============================================\n")

    lines.append(f"📄 Elemzett RAW fájl: {os.path.basename(raw_path)}")
    lines.append(f"Dátum: {datum}\n")

    lines.append("Figyelem: Az alábbi genetikai információk érzékeny személyes adatok.")
    lines.append("A tartalom tájékoztató jellegű, nem minősül orvosi diagnózisnak.\n")

    # ---------------------------------------------------------
    # SZEM
    # ---------------------------------------------------------
    lines.append("=== SZEM ===\n")

    # Szemszín – HERC2 rs12913832
    g = raw.get("rs12913832")
    if g == "AA":
        txt = "Világos (kék/zöld)"
        score = 2
    elif g in ("AG", "GA"):
        txt = "Közepes / kevert"
        score = 1
    elif g == "GG":
        txt = "Barna"
        score = 0
    else:
        txt = "Nincs adat"
        score = 0

    lines.append(f"🔸 Szemszín: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Rövidlátás – GJD2 rs524952 (T kockázati allél)
    g = raw.get("rs524952")
    score = score_from_genotype(g, "T")
    txt = "Emelkedett rövidlátás hajlam" if score > 0 else "Alacsony rövidlátás hajlam"
    lines.append(f"🔸 Rövidlátás: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Kancsalság – WRB rs1881492 (A kockázati allél)
    g = raw.get("rs1881492")
    score = score_from_genotype(g, "A")
    txt = "Emelkedett kancsalság hajlam" if score > 0 else "Alacsony kancsalság hajlam"
    lines.append(f"🔸 Kancsalság: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Szemforma – EDAR rs3827760
    g = raw.get("rs3827760")
    if g == "TT":
        txt = "Ázsiai jellegű szemforma"
        score = 2
    elif g in ("CT", "TC"):
        txt = "Kevert jellegű szemforma"
        score = 1
    elif g == "CC":
        txt = "Európai jellegű szemforma"
        score = 0
    else:
        txt = "Nincs adat"
        score = 0

    lines.append(f"🔸 Szemforma: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # ---------------------------------------------------------
    # BŐR
    # ---------------------------------------------------------
    lines.append("=== BŐR ===\n")

    # Bőrszín – SLC24A5 rs1426654
    g = raw.get("rs1426654")
    if g == "AA":
        txt = "Világos pigmentáció"
        score = 2
    elif g in ("AG", "GA"):
        txt = "Közepes pigmentáció"
        score = 1
    elif g == "GG":
        txt = "Sötétebb pigmentáció"
        score = 0
    else:
        txt = "Nincs adat"
        score = 0

    lines.append(f"🔸 Bőrszín: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # UV-érzékenység – IRF4 rs12203592 (T kockázati allél)
    g = raw.get("rs12203592")
    score = score_from_genotype(g, "T")
    txt = "Emelkedett UV-érzékenység" if score > 0 else "Alacsony UV-érzékenység"
    lines.append(f"🔸 UV-érzékenység: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Szeplősödés – MC1R rs1805007 (T kockázati allél)
    g = raw.get("rs1805007")
    score = score_from_genotype(g, "T")
    txt = "Emelkedett szeplősödés hajlam" if score > 0 else "Alacsony szeplősödés hajlam"
    lines.append(f"🔸 Szeplősödés: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # ---------------------------------------------------------
    # HAJ
    # ---------------------------------------------------------
    lines.append("=== HAJ ===\n")

    # Hajszín – MC1R rs1805008 (T kockázati allél – vöröses beütés)
    g = raw.get("rs1805008")
    score = score_from_genotype(g, "T")
    txt = "Vöröses hajbeütésre hajlamos" if score > 0 else "Nincs vörös hajra utaló variáns"
    lines.append(f"🔸 Hajszín: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Hajvastagság – EDAR rs3827760 (ugyanaz az SNP, más szempont)
    g = raw.get("rs3827760")
    if g == "TT":
        txt = "Vastagabb hajszál"
        score = 2
    elif g in ("CT", "TC"):
        txt = "Közepes vastagság"
        score = 1
    elif g == "CC":
        txt = "Átlagos vastagság"
        score = 0
    else:
        txt = "Nincs adat"
        score = 0

    lines.append(f"🔸 Hajvastagság: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Kopaszodás – AR rs1160312 (A kockázati allél)
    g = raw.get("rs1160312")
    score = score_from_genotype(g, "A")
    txt = "Emelkedett kopaszodási hajlam" if score > 0 else "Alacsony kopaszodási hajlam"
    lines.append(f"🔸 Kopaszodás: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # Őszülés – IRF4 rs12203592 (T kockázati allél – ugyanaz az SNP, más szempont)
    g = raw.get("rs12203592")
    score = score_from_genotype(g, "T")
    txt = "Emelkedett őszülési hajlam" if score > 0 else "Alacsony őszülési hajlam"
    lines.append(f"🔸 Őszülés: {txt}")
    lines.append(f"   Genotípus: {g}")
    lines.append(f"   [{progress_bar(score, 2)}]")
    lines.append(f"   Értelmezés: {category_from_score(score)}\n")

    # ---------------------------------------------------------
    # RÉSZLETES SNP LISTA
    # ---------------------------------------------------------
    lines.append("=== RÉSZLETES SNP LISTA ===\n")

    snp_list = [
        ("rs12913832", "Szemszín – HERC2"),
        ("rs524952", "Rövidlátás – GJD2"),
        ("rs1881492", "Kancsalság – WRB"),
        ("rs3827760", "Szemforma / hajvastagság – EDAR"),
        ("rs1426654", "Bőrszín – SLC24A5"),
        ("rs12203592", "UV-érzékenység / őszülés – IRF4"),
        ("rs1805007", "Szeplősödés – MC1R"),
        ("rs1805008", "Hajszín – MC1R"),
        ("rs1160312", "Kopaszodás – AR"),
    ]

    for rsid, desc in snp_list:
        genotype = raw.get(rsid)
        if genotype is None:
            interp = "A variáns nem található."
        else:
            interp = "Genotípus jelen van, értelmezés a fenti szakaszokban."
        lines.append(f"{rsid} ({desc})")
        lines.append(f"   Genotípus: {genotype}")
        lines.append(f"   Értelmezés: {interp}\n")

    # ---------------------------------------------------------
    # FONTOS MEGJEGYZÉS
    # ---------------------------------------------------------
    lines.append("==============================================")
    lines.append(" FONTOS MEGJEGYZÉS")
    lines.append("==============================================\n")

    lines.append("- A látható tulajdonságok genetikai hajlamai csak részben határozzák meg a külső jegyeket.")
    lines.append("- A környezet, életkor, hormonális és életmódbeli tényezők legalább ilyen fontosak.")
    lines.append("- A panel tájékoztató jellegű, orvosi diagnózist nem helyettesít.\n")

    # ---------------------------------------------------------
    # Mentés + terminál kiírás
    # ---------------------------------------------------------
    os.makedirs("Eredmenyek", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(raw_path))[0]
    output_path = os.path.join("Eredmenyek", f"{base_name}_lathato_tulajdonsagok.txt")

    content = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(content)
    print("\nEredmény elmentve ide:", output_path)


# ---------------------------------------------------------
# Automatikus indítás
# ---------------------------------------------------------
if __name__ == "__main__":
    run()
