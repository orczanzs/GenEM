# -*- coding: utf-8 -*-
"""
============================================================
 HAJ TULAJDONSÁGOK – GENETIKAI PANEL
 GitHub‑kompatibilis, rendezett, egységes verzió
------------------------------------------------------------
 Ez a panel MyHeritage RAW DNA fájlokból olvassa ki a hajszín,
 kopaszodási hajlam, őszülési hajlam és hajvastagság genetikai
 markereit.

 A panel NEM diagnosztikai eszköz. A genetikai értékek
 tájékoztató jellegűek.
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
# RAW BEOLVASÁS (CSV, egységesen)
# ============================================================

def read_raw_data(file_path):
    """Beolvassa a MyHeritage RAW CSV fájlt."""
    data = {}
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if len(row) >= 4 and not row[0].startswith("#"):
                rsid = row[0].replace('"', '').strip()
                genotype = row[3].replace('"', '').strip()
                data[rsid] = genotype
    return data


# ============================================================
# SEGÉDFÜGGVÉNY – MELANIN PROFIL
# ============================================================

def melanin_profile(eumelanin_level, pheomelanin_level):
    return (
        f"Eumelanin (sötét pigment) szint: {eumelanin_level}.\n"
        f"Pheomelanin (vörös pigment) szint: {pheomelanin_level}.\n"
    )


# ============================================================
# HAJSZÍN BECSLÉSE
# ============================================================

def estimate_hair_color(raw_data):
    rs129 = raw_data.get("rs12913832", "N/A")   # HERC2
    rs168 = raw_data.get("rs16891982", "N/A")   # SLC45A2
    rs142 = raw_data.get("rs1426654", "N/A")    # SLC24A5
    rs128 = raw_data.get("rs12821256", "N/A")   # KITLG
    rs5007 = raw_data.get("rs1805007", "N/A")   # MC1R
    rs5008 = raw_data.get("rs1805008", "N/A")   # MC1R

    explanation = []
    red_score = 0
    light_score = 0
    dark_score = 0

    # MC1R – vörös haj
    if rs5007 != "N/A" and "T" in rs5007:
        red_score += 1
        explanation.append("Az MC1R rs1805007 variáns vörös hajra hajlamosító hatású.")
    if rs5008 != "N/A" and "T" in rs5008:
        red_score += 1
        explanation.append("Az MC1R rs1805008 variáns vörös hajra hajlamosító hatású.")

    # HERC2 – világos vs sötét
    if rs129 != "N/A":
        if rs129 == "AA":
            light_score += 2
            explanation.append("A HERC2 rs12913832 AA genotípus világosabb hajszín irányába hat.")
        elif rs129 in ["AG", "GA"]:
            light_score += 1
            dark_score += 1
            explanation.append("A HERC2 rs12913832 heterozigóta állapota köztes hajszínt támogat.")
        else:
            dark_score += 2
            explanation.append("A HERC2 rs12913832 sötétebb variánsa sötétebb hajszín irányába hat.")

    # SLC45A2 – sötét pigment
    if rs168 != "N/A" and rs168 in ["GG", "GC", "CG"]:
        dark_score += 1
        explanation.append("Az SLC45A2 rs16891982 variáns fokozza a sötét pigment mennyiségét.")

    # SLC24A5 – világos pigment
    if rs142 != "N/A":
        if rs142 == "AA":
            light_score += 2
            explanation.append("Az SLC24A5 rs1426654 AA genotípus világosabb pigmentációval társul.")
        elif rs142 in ["AG", "GA"]:
            light_score += 1
            explanation.append("Az SLC24A5 rs1426654 heterozigóta állapota enyhén világosító hatású.")

    # KITLG – szőke haj
    if rs128 != "N/A" and "C" in rs128:
        light_score += 2
        explanation.append("A KITLG rs12821256 variáns a szőke haj irányába hat.")

    # Hajszín meghatározása
    color_label = "ismeretlen"
    shade_text = "A hajszín nem becsülhető megbízhatóan."
    eumelanin_level = "közepes"
    pheomelanin_level = "közepes"

    if red_score >= 2:
        color_label = "vörös"
        shade_text = "Erős vörös hajlam."
        eumelanin_level = "alacsony-közepes"
        pheomelanin_level = "magas"
    elif red_score == 1:
        if dark_score > light_score:
            color_label = "barna vöröses árnyalattal"
            shade_text = "Barna haj vöröses árnyalattal."
            eumelanin_level = "közepes-magas"
            pheomelanin_level = "közepes"
        else:
            color_label = "világosbarna / sötétszőke vöröses árnyalattal"
            shade_text = "Világosabb haj vöröses árnyalattal."
            eumelanin_level = "közepes"
            pheomelanin_level = "közepes-magas"
    else:
        if dark_score - light_score >= 2:
            color_label = "sötétbarna / fekete"
            shade_text = "Magas eumelanin szint."
            eumelanin_level = "magas"
            pheomelanin_level = "alacsony"
        elif dark_score > light_score:
            color_label = "középbarna / sötétbarna"
            shade_text = "Közepes-magas eumelanin."
            eumelanin_level = "közepes-magas"
            pheomelanin_level = "alacsony-közepes"
        elif light_score - dark_score >= 2:
            color_label = "szőke"
            shade_text = "Világosszőke vagy aranyszőke."
            eumelanin_level = "alacsony"
            pheomelanin_level = "közepes"
        else:
            color_label = "világosbarna / sötétszőke"
            shade_text = "Köztes pigmentáció."

    melanin_text = melanin_profile(eumelanin_level, pheomelanin_level)

    return {
        "color_label": color_label,
        "shade_text": shade_text,
        "melanin_text": melanin_text,
        "explanation": explanation,
        "rs_values": {
            "rs12913832": rs129,
            "rs16891982": rs168,
            "rs1426654": rs142,
            "rs12821256": rs128,
            "rs1805007": rs5007,
            "rs1805008": rs5008,
        },
    }


# ============================================================
# KOPASZODÁSI HAJLAM
# ============================================================

def evaluate_balding(raw_data):
    markers = {
        "rs1160312": raw_data.get("rs1160312", "N/A"),
        "rs5919393": raw_data.get("rs5919393", "N/A"),
        "rs7349332": raw_data.get("rs7349332", "N/A"),
        "rs12565727": raw_data.get("rs12565727", "N/A"),
        "rs2153960": raw_data.get("rs2153960", "N/A"),
        "rs9982601": raw_data.get("rs9982601", "N/A"),
    }

    risk_score = 0.0
    protective_score = 0.0
    explanation = []
    missing = []

    # rs1160312
    g = markers["rs1160312"]
    if g == "N/A":
        missing.append("rs1160312")
    else:
        if g == "GG":
            risk_score += 2
            explanation.append("Az rs1160312 GG genotípus emelkedett hajlamot jelez a férfias típusú hajhullásra.")
        elif g in ["AG", "GA"]:
            risk_score += 1
            explanation.append("Az rs1160312 heterozigóta állapota enyhén emelkedett hajlamot jelez.")
        elif g == "AA":
            protective_score += 1
            explanation.append("Az rs1160312 AA genotípus inkább alacsonyabb hajlammal társul.")

    # rs5919393
    g = markers["rs5919393"]
    if g == "N/A":
        missing.append("rs5919393")
    else:
        if g == "TT":
            risk_score += 2
            explanation.append("Az rs5919393 TT genotípus emelkedett hajlamot jelez.")
        elif g in ["CT", "TC"]:
            risk_score += 1
            explanation.append("Az rs5919393 heterozigóta állapota enyhén emelkedett hajlamot jelez.")
        elif g == "CC":
            protective_score += 1
            explanation.append("Az rs5919393 CC genotípus inkább alacsonyabb hajlammal társul.")

    # rs7349332
    g = markers["rs7349332"]
    if g == "N/A":
        missing.append("rs7349332")
    else:
        if g == "TT":
            risk_score += 2
            explanation.append("Az rs7349332 TT genotípus fokozott hajlamot jelez a hajritkulásra.")
        elif g in ["CT", "TC"]:
            risk_score += 1
            explanation.append("Az rs7349332 heterozigóta állapota enyhén emelkedett hajlamot jelez.")
        elif g == "CC":
            protective_score += 1
            explanation.append("Az rs7349332 CC genotípus inkább védő hatású.")

    # rs12565727
    g = markers["rs12565727"]
    if g == "N/A":
        missing.append("rs12565727")
    else:
        if g == "GG":
            risk_score += 2
            explanation.append("Az rs12565727 GG genotípus emelkedett kopaszodási hajlammal társulhat.")
        elif g in ["AG", "GA"]:
            risk_score += 1
            explanation.append("Az rs12565727 heterozigóta állapota enyhén emelkedett hajlamot jelez.")
        elif g == "AA":
            protective_score += 1
            explanation.append("Az rs12565727 AA genotípus inkább alacsonyabb hajlammal társul.")

    # rs9982601
    g = markers["rs9982601"]
    if g == "N/A":
        missing.append("rs9982601")
    else:
        if g == "TT":
            risk_score += 1
            explanation.append("Az rs9982601 TT genotípus enyhén emelkedett hajlamot jelez.")
        elif g in ["CT", "TC"]:
            risk_score += 0.5
            explanation.append("Az rs9982601 heterozigóta állapota kismértékben emelheti a hajlamot.")
        elif g == "CC":
            protective_score += 0.5
            explanation.append("Az rs9982601 CC genotípus inkább semleges vagy enyhén védő hatású.")

    # rs2153960 – csak megjelenítjük
    if markers["rs2153960"] == "N/A":
        missing.append("rs2153960")
    else:
        explanation.append("Az rs2153960 marker jelen van a RAW fájlban; a panel jelen verziója ezt csak megjeleníti, nem pontozza.")

    if all(v == "N/A" for v in markers.values()):
        category = "nem értékelhető"
        summary = "A kopaszodási hajlam genetikai értékelése nem lehetséges, mert a szükséges markerek nem találhatók a RAW fájlban."
    else:
        if risk_score == 0 and protective_score > 0:
            category = "alacsony genetikai hajlam"
            summary = "A vizsgált markerek alapján inkább alacsony genetikai hajlam valószínű a férfias típusú hajhullásra."
        elif risk_score <= 2:
            category = "enyhén emelkedett genetikai hajlam"
            summary = "A vizsgált markerek alapján enyhén emelkedett genetikai hajlam valószínű."
        elif risk_score <= 4:
            category = "közepesen emelkedett genetikai hajlam"
            summary = "A vizsgált markerek alapján közepesen emelkedett genetikai hajlam valószínű."
        else:
            category = "fokozott genetikai hajlam"
            summary = "A vizsgált markerek alapján fokozott genetikai hajlam valószínű."

    return {
        "category": category,
        "summary": summary,
        "explanation": explanation,
        "markers": markers,
        "missing": missing,
    }


# ============================================================
# ŐSZÜLÉSI HAJLAM
# ============================================================

def evaluate_greying(raw_data):
    markers = {
        "rs12203592": raw_data.get("rs12203592", "N/A"),  # IRF4
        "rs1393350": raw_data.get("rs1393350", "N/A"),    # TYR
        "rs12821256": raw_data.get("rs12821256", "N/A"),  # KITLG
        "rs683": raw_data.get("rs683", "N/A"),            # TYRP1
    }

    risk_score = 0.0
    protective_score = 0.0
    explanation = []
    missing = []

    # rs12203592 – fő őszülési marker
    g = markers["rs12203592"]
    if g == "N/A":
        missing.append("rs12203592")
    else:
        if g == "TT":
            risk_score += 2
            explanation.append("Az rs12203592 TT genotípus korai őszülésre emelkedett genetikai hajlammal társul.")
        elif g in ["CT", "TC"]:
            risk_score += 1
            explanation.append("Az rs12203592 heterozigóta állapota enyhén emelkedett őszülési hajlamot jelezhet.")
        elif g == "CC":
            protective_score += 1
            explanation.append("Az rs12203592 CC genotípus inkább alacsonyabb korai őszülési hajlammal társul.")

    # rs1393350 – pigmentációs marker
    g = markers["rs1393350"]
    if g == "N/A":
        missing.append("rs1393350")
    else:
        if g == "AA":
            risk_score += 1
            explanation.append("Az rs1393350 AA genotípus világosabb pigmentációval és enyhén emelkedett őszülési hajlammal társulhat.")
        elif g in ["AG", "GA"]:
            risk_score += 0.5
            explanation.append("Az rs1393350 heterozigóta állapota enyhe pigmentációs hatással bír.")
        elif g == "GG":
            explanation.append("Az rs1393350 GG genotípus inkább semleges a korai őszülés szempontjából.")

    # rs683 – TYRP1
    g = markers["rs683"]
    if g == "N/A":
        missing.append("rs683")
    else:
        if g == "AA":
            risk_score += 0.5
            explanation.append("Az rs683 AA genotípus enyhén befolyásolhatja a pigmentációt és az őszülés időzítését.")
        elif g in ["CA", "AC"]:
            risk_score += 0.25
            explanation.append("Az rs683 heterozigóta állapota kismértékű pigmentációs hatással bír.")
        elif g == "CC":
            explanation.append("Az rs683 CC genotípus inkább semleges a korai őszülés szempontjából.")

    # rs12821256 – pigment, nem kifejezetten őszülés
    g = markers["rs12821256"]
    if g == "N/A":
        missing.append("rs12821256")
    else:
        if "C" in g:
            explanation.append("Az rs12821256 C allél világosabb (szőkésebb) hajszínnel társulhat, ami az őszülés láthatóságát befolyásolhatja.")
        else:
            explanation.append("Az rs12821256 genotípus nem hordoz világosító (C) allélt, pigmentációs hatása semlegesebb.")

    if all(v == "N/A" for v in markers.values()):
        category = "nem értékelhető"
        summary = "Az őszülési hajlam genetikai értékelése nem lehetséges, mert a szükséges markerek nem találhatók a RAW fájlban."
    else:
        if risk_score == 0 and protective_score > 0:
            category = "alacsony genetikai őszülési hajlam"
            summary = "A vizsgált markerek alapján inkább alacsony genetikai hajlam valószínű a korai őszülésre."
        elif risk_score <= 1:
            category = "átlagos genetikai őszülési hajlam"
            summary = "A vizsgált markerek alapján átlagos genetikai hajlam valószínű a korai őszülésre."
        elif risk_score <= 2.5:
            category = "enyhén emelkedett genetikai őszülési hajlam"
            summary = "A vizsgált markerek alapján enyhén emelkedett genetikai hajlam valószínű a korai őszülésre."
        else:
            category = "emelkedett genetikai őszülési hajlam"
            summary = "A vizsgált markerek alapján emelkedett genetikai hajlam valószínű a korai őszülésre."

    return {
        "category": category,
        "summary": summary,
        "explanation": explanation,
        "markers": markers,
        "missing": missing,
    }


# ============================================================
# HAJVASTAGSÁG
# ============================================================

def evaluate_thickness(raw_data):
    markers = {
        "rs11803731": raw_data.get("rs11803731", "N/A"),  # TCHH
        "rs7349332": raw_data.get("rs7349332", "N/A"),    # WNT10A
        "rs3827760": raw_data.get("rs3827760", "N/A"),    # EDAR
    }

    thin_score = 0.0
    thick_score = 0.0
    explanation = []
    missing = []

    # rs11803731 – TCHH
    g = markers["rs11803731"]
    if g == "N/A":
        missing.append("rs11803731")
    else:
        if g == "TT":
            thick_score += 2
            explanation.append("Az rs11803731 TT genotípus vastagabb hajszálakkal társulhat.")
        elif g in ["CT", "TC"]:
            thick_score += 1
            explanation.append("Az rs11803731 heterozigóta állapota közepes hajvastagságot jelezhet.")
        elif g == "CC":
            thin_score += 1
            explanation.append("Az rs11803731 CC genotípus inkább vékonyabb hajszálakkal társulhat.")

    # rs7349332 – WNT10A
    g = markers["rs7349332"]
    if g == "N/A":
        missing.append("rs7349332")
    else:
        if g == "TT":
            thin_score += 2
            explanation.append("Az rs7349332 TT genotípus vékonyabb, ritkább hajszálakkal társulhat.")
        elif g in ["CT", "TC"]:
            thin_score += 1
            explanation.append("Az rs7349332 heterozigóta állapota enyhén vékonyabb hajszálakat jelezhet.")
        elif g == "CC":
            thick_score += 1
            explanation.append("Az rs7349332 CC genotípus inkább vastagabb hajszálakkal társulhat.")

    # rs3827760 – EDAR
    g = markers["rs3827760"]
    if g == "N/A":
        missing.append("rs3827760")
    else:
        if g == "GG":
            thick_score += 2
            explanation.append("Az rs3827760 GG genotípus nagyon vastag hajszálakkal társulhat (gyakori kelet-ázsiai populációkban).")
        elif g in ["AG", "GA"]:
            thick_score += 1
            explanation.append("Az rs3827760 heterozigóta állapota enyhén vastagabb hajszálakat jelezhet.")
        elif g == "AA":
            explanation.append("Az rs3827760 AA genotípus európai típusú, közepes hajvastagsággal társuló variáns.")

    if all(v == "N/A" for v in markers.values()):
        category = "nem értékelhető"
        summary = "A hajvastagság genetikai értékelése nem lehetséges, mert a szükséges markerek nem találhatók a RAW fájlban."
    else:
        if thin_score == 0 and thick_score > 0:
            category = "inkább vastag hajszálak"
            summary = "A vizsgált markerek alapján inkább vastagabb hajszálak genetikai hajlama valószínű."
        elif thick_score == 0 and thin_score > 0:
            category = "inkább vékony hajszálak"
            summary = "A vizsgált markerek alapján inkább vékonyabb hajszálak genetikai hajlama valószínű."
        else:
            category = "közepes hajvastagság"
            summary = "A vizsgált markerek alapján közepes, átlagos hajvastagság genetikai hajlama valószínű."

    return {
        "category": category,
        "summary": summary,
        "explanation": explanation,
        "markers": markers,
        "missing": missing,
    }


# ============================================================
# ÉLETKORI MEGJEGYZÉS
# ============================================================

def life_stage_comment():
    return (
        "Életkori és állapotbeli megjegyzés:\n"
        "- A genetikai hajszín az alapszínt jelenti, amelyre a szervezet „programozva” van.\n"
        "- Gyermekkorban a haj gyakran világosabb, majd pubertáskor sötétedhet.\n"
        "- Őszülés vagy hajritkulás esetén is ez a genetikai alapszín marad a háttérben, még ha a jelenlegi megjelenés eltér is tőle.\n"
    )


# ============================================================
# FŐ ÉRTELMEZŐ FÜGGVÉNY – HAJPANEL ÖSSZEFOGLALÓ
# ============================================================

def interpret_hair_panel(raw_data):
    hair = estimate_hair_color(raw_data)
    bald = evaluate_balding(raw_data)
    grey = evaluate_greying(raw_data)
    thick = evaluate_thickness(raw_data)
    life_text = life_stage_comment()

    rs_vals = hair["rs_values"]

    summary = (
        "=== HAJ TULAJDONSÁG PANEL ===\n\n"
        "Genetikai hajszín becslés:\n"
        f"- Becsült genetikai hajszín: {hair['color_label']}\n"
        f"- Árnyalat: {hair['shade_text']}\n\n"
        "Felhasznált főbb genetikai markerek (genotípusok) – hajszín:\n"
        f"- HERC2 (rs12913832): {rs_vals['rs12913832']}\n"
        f"- SLC45A2 (rs16891982): {rs_vals['rs16891982']}\n"
        f"- SLC24A5 (rs1426654): {rs_vals['rs1426654']}\n"
        f"- KITLG (rs12821256): {rs_vals['rs12821256']}\n"
        f"- MC1R (rs1805007): {rs_vals['rs1805007']}\n"
        f"- MC1R (rs1805008): {rs_vals['rs1805008']}\n\n"
        "Melanin profil:\n"
        f"{hair['melanin_text']}\n"
        "Tudományos magyarázat a hajszín hátteréről:\n"
        + "\n".join(hair["explanation"]) +
        "\n\n"
        + life_text +
        "\n"
    )

    # Kopaszodási hajlam blokk
    summary += "Kopaszodási hajlam (androgenetikus alopecia):\n"
    summary += f"- Összefoglaló: {bald['category']}\n"
    summary += f"- Részletes értelmezés: {bald['summary']}\n\n"
    summary += "Felhasznált kopaszodási markerek (genotípusok):\n"
    for rsid, g in bald["markers"].items():
        if g == "N/A":
            summary += f"- {rsid}: A RAW fájl nem tartalmazza az ehhez szükséges genetikai markert.\n"
        else:
            summary += f"- {rsid}: {g}\n"
    if bald["explanation"]:
        summary += "\nTudományos magyarázat a kopaszodási hajlam hátteréről:\n"
        summary += "\n".join(bald["explanation"]) + "\n\n"

    # Őszülési hajlam blokk
    summary += "Őszülési hajlam:\n"
    summary += f"- Összefoglaló: {grey['category']}\n"
    summary += f"- Részletes értelmezés: {grey['summary']}\n\n"
    summary += "Felhasznált őszülési markerek (genotípusok):\n"
    for rsid, g in grey["markers"].items():
        if g == "N/A":
            summary += f"- {rsid}: A RAW fájl nem tartalmazza az ehhez szükséges genetikai markert.\n"
        else:
            summary += f"- {rsid}: {g}\n"
    if grey["explanation"]:
        summary += "\nTudományos magyarázat az őszülés genetikai hátteréről:\n"
        summary += "\n".join(grey["explanation"]) + "\n\n"

    # Hajvastagság blokk
    thick_data = thick
    summary += "Hajvastagság genetikai becslése:\n"
    summary += f"- Összefoglaló: {thick_data['category']}\n"
    summary += f"- Részletes értelmezés: {thick_data['summary']}\n\n"
    summary += "Felhasznált hajvastagság markerek (genotípusok):\n"
    for rsid, g in thick_data["markers"].items():
        if g == "N/A":
            summary += f"- {rsid}: A RAW fájl nem tartalmazza az ehhez szükséges genetikai markert.\n"
        else:
            summary += f"- {rsid}: {g}\n"
    if thick_data["explanation"]:
        summary += "\nTudományos magyarázat a hajvastagság genetikai hátteréről:\n"
        summary += "\n".join(thick_data["explanation"]) + "\n\n"

    summary += "===========================\n"
    return summary


# ============================================================
# FŐ FUTTATÓ FÜGGVÉNY – EREDMÉNY FÁJLBA ÍRÁSSAL
# ============================================================

def run_hair_panel(file_path):
    raw_data = read_raw_data(file_path)
    summary = interpret_hair_panel(raw_data)
    out_name = f"Haj_panel_eredmeny_{os.path.basename(file_path)}.txt"
    with open(out_name, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"\nEredmény elmentve ide: {out_name}\n")
    print(summary)


# ============================================================
# FUTTATÁS
# ============================================================

def run():
    print("=== HAJ TULAJDONSÁG PANEL ===")
    fajl = select_raw_file()
    if fajl is None:
        return
    print(f"\nKiválasztott RAW fájl: {fajl}\n")
    run_hair_panel(fajl)


if __name__ == "__main__":
    run()
