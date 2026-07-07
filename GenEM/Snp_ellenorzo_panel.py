#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-blokkos SNP ellenőrző panel – 1 sor előtte, 1 sor utána
UTF-8 helyes vágólap + TXT az Eredmenyek mappába
A TXT teljes tartalma megjelenik a terminálon
A vágólapra CSAK a talált rs sor + AI-kérés kerül
"""

import csv
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def detect_delimiter(sample_text: str) -> str:
    if sample_text.count(";") > sample_text.count(","):
        return ";"
    if "\t" in sample_text and sample_text.count("\t") > sample_text.count(","):
        return "\t"
    return ","

def clean_value(v):
    if v is None:
        return ""
    v = v.replace("\ufeff", "").replace("\ufffe", "")
    v = re.sub(r"[^\x09\x20-\x7E\u00A0-\uFFFF]", "", v)
    return v.strip()

def read_csv_rows(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return []
    sample = text[:8192]
    delimiter = detect_delimiter(sample)
    lines = text.splitlines()
    reader = csv.reader(lines, delimiter=delimiter)
    try:
        header = next(reader)
    except StopIteration:
        return []
    normalized_headers = [clean_value(h).upper() for h in header]
    rows = []
    for parts in reader:
        parts = [clean_value(p) for p in parts]
        row = {}
        for i, h in enumerate(normalized_headers):
            val = parts[i] if i < len(parts) else ""
            row[h] = val
        if "RSID" not in row and len(parts) >= 1:
            row["RSID"] = clean_value(parts[0])
        rows.append(row)
    return rows

def find_first_rsid_index(rows, rsid):
    target = rsid.strip().upper()
    for i, row in enumerate(rows):
        val = row.get("RSID", "").strip().upper()
        if val == target:
            return i
    return None

def format_row_short(row, marker="  "):
    rsid = clean_value(row.get("RSID", ""))
    chrom = clean_value(row.get("CHROMOSOME", row.get("CHROM", "")))
    pos = clean_value(row.get("POSITION", row.get("POS", "")))
    genotype = clean_value(row.get("RESULT", row.get("GENOTYPE", "")))
    return f"{marker} {rsid}  chr{chrom}:{pos}  {genotype}"

def copy_to_clipboard(text: str) -> bool:
    """UTF‑8 biztos vágólap (tkinter elsődleges)"""
    try:
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return True
    except Exception:
        return False

def write_output_file(base_path: Path, raw_path: Path, rsid: str, output_lines, ai_block):
    """TXT az Eredmenyek mappába kerül"""
    eredm_dir = base_path / "Eredmenyek"
    eredm_dir.mkdir(exist_ok=True)

    datum = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_rsid = rsid.replace("/", "_").replace("\\", "_")
    out_name = f"SNP_kornyezet_{raw_path.stem}_{datum}_{safe_rsid}.txt"
    out_path = eredm_dir / out_name

    with out_path.open("w", encoding="utf-8") as f:
        f.write("SNP környezet (AI-ellenőrzéshez)\n")
        f.write(f"RAW fájl: {raw_path.name}\n")
        f.write(f"Dátum: {datum}\n")
        f.write(f"rsID: {rsid}\n\n")
        for line in output_lines:
            f.write(line + "\n")
        f.write("\n")
        f.write(ai_block)

    return out_path

def run_panel():
    script_path = Path(__file__).resolve()
    base_path = script_path.parent

    csv_files = sorted(base_path.glob("*.csv"))
    if not csv_files:
        print("Nincs .csv fájl a program mappájában!")
        return

    print("Elérhető RAW CSV fájlok:")
    for i, f in enumerate(csv_files, 1):
        print(f"{i}) {f.name}")

    choice = input(f"Válassz fájlt (1-{len(csv_files)}): ").strip()
    try:
        raw_path = csv_files[int(choice) - 1]
    except:
        print("Érvénytelen választás.")
        return

    print("Fájl beolvasása...")
    rows = read_csv_rows(raw_path)
    if not rows:
        print("A fájl üres vagy hibás.")
        return

    rsid = input("Add meg a keresett rs sort, például: rs3131972, rsID-t:  ").strip()
    index = find_first_rsid_index(rows, rsid)
    if index is None:
        print(f"Nem található: {rsid}")
        return

    start = max(0, index - 1)
    end = min(len(rows), index + 2)

    output_lines = ["=== SNP környezet (ellenőrzéshez) ===", ""]
    for i in range(start, end):
        marker = ">>" if i == index else "  "
        line = format_row_short(rows[i], marker)
        print(line)
        output_lines.append(line)

    ai_block = (
        "\n--- Hogyan ellenőrizd bármely AI-val ---\n"
        "1) Nyisd meg a kedvenc AI chat alkalmazásodat (pl. Copilot, ChatGPT, Claude).\n"
        "2) Illeszd be a vágólap tartalmát (Ctrl+V / Cmd+V).\n"
        '3) Írd ezt: "Kérlek adj rövid, stabil, tudományos magyarázatot minden rs sorhoz. '
        'Ha egy SNP nem ismert, írd azt: Általános genomikus marker vagy: Ritka variáns, nincs ismert funkció."\n'
    )

    print(ai_block)

    # A teljes TXT tartalom
    full_txt = "\n".join(output_lines) + ai_block

    print("\n--- A TXT fájl teljes tartalma ---\n")
    print(full_txt)

    # Megkeressük a >> jellel kezdődő sort
    found_line = next(line for line in output_lines if line.startswith(">>"))

    # A vágólapra CSAK a talált rs sor + AI-kérés kerül
    clipboard_text = (
        f"{found_line}\n\n"
        "Kérlek adj rövid, stabil, tudományos magyarázatot erre az rs sorra.\n"
        "Ha egy SNP nem ismert, írd azt: Általános genomikus marker vagy: Ritka variáns, nincs ismert funkció.\n"
    )

    copied = copy_to_clipboard(clipboard_text)

    out_path = write_output_file(base_path, raw_path, rsid, output_lines, ai_block)

    print("\n--- A vágólapra került tartalom ---\n")
    print(clipboard_text)

    if copied:
        print("\nA vágólapra másolás sikeres (UTF‑8).")
    else:
        print("\nNem sikerült a vágólapra másolni.")

    print("Mentve:", out_path)

if __name__ == "__main__":
    run_panel()
