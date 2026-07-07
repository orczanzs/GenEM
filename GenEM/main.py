# -*- coding: utf-8 -*-
"""
============================================================
 FŐMENÜ – GENETIKAI PANEL PROJEKT
------------------------------------------------------------
 Ez a program egységes belépési pontként szolgál minden panelhez.
 A paneleket külön .py fájlok tartalmazzák, mindegyik saját
 run() függvénnyel.

 Új panel hozzáadása:
 1) Hozz létre egy új .py fájlt (pl. Magassag_panel.py)
 2) A fájlban legyen egy run() függvény
 3) Itt a main.py-ben add hozzá a PANELS listához:

    ("Magasság panel", "Magassag_panel")

 Ennyi. A rendszer automatikusan működni fog.
============================================================
"""

import importlib

# ============================================================
# PANEL LISTA – IDE KELL HOZZÁADNI AZ ÚJ PANELEKET
# ==========================================================
PANELS = [
    ("Laktóz intolerancia panel", "Lactose_panel"),
    ("Hisztamin érzékenység panel", "Histamin_panel"),
    ("Atópiás dermatitis panel", "Atopias_dermatitis_panel"),
    ("Bőr tulajdonságok panel", "Bor_tulajdonsagok_panel"),
    ("Haj tulajdonságok panel", "Haj_tulajdonsagok_panel"),
    ("Szem tulajdonságok panel", "Szem_tulajdonsagok_panel"),
    # ÚJ PANELT IDE ÍRSZ BE:
    # ("Panel neve", "Fajl_neve_kiterjesztes_nelkul")
    ("Magasság Elhizás BMI ", "Magassag_Elhizas_panel"),
    ("Öregedési Hajlam" , "Oregedesi_hajlam_panel"),
    ("Sportolási Hajlam" , "Sport_hajlam_panel"),
    ("Izület Hajlam", "Izuleti_hajlam_panel"),
]

# ============================================================
# FŐMENÜ
# ============================================================

def main():
    print("\n==============================================")
    print(" GENETIKAI PANEL PROJEKT – FŐMENÜ")
    print("==============================================\n")

    print("A projekt jelenleg az alábbi paneleket tudja futtatni:\n")

    for i, (name, module) in enumerate(PANELS, start=1):
        print(f"  {i}. {name}")

    print("\n  0. Kilépés\n")

    while True:
        try:
            choice = int(input("Válassz egy panelt (szám): "))
            if choice == 0:
                print("\nKilépés...\n")
                return
            if 1 <= choice <= len(PANELS):
                panel_name, module_name = PANELS[choice - 1]
                print(f"\n📌 {panel_name} betöltése...\n")

                module = importlib.import_module(module_name)
                module.run()
                return
            else:
                print("Érvénytelen választás.")
        except ValueError:
            print("Számot adj meg.")

# ============================================================
# FUTTATÁS
# ============================================================

if __name__ == "__main__":
    main()
