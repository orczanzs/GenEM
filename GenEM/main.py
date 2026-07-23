# -*- coding: utf-8 -*-
"""
============================================================
 FŐMENÜ – GENETIKAI PANEL PROJEKT
------------------------------------------------------------
 Wrapper megoldással: minden panel futása után az újonnan
 létrehozott fájlok automatikusan az 'eredmeny' mappába kerülnek.
============================================================
"""

import importlib
import os
import shutil

# ============================================================
# PANEL LISTA – IDE KELL HOZZÁADNI AZ ÚJ PANELEKET
# ============================================================
PANELS = [
    ("Laktóz intolerancia panel", "Lactose_panel"),
    ("Hisztamin érzékenység panel", "Histamin_panel"),
    ("Atópiás dermatitis panel", "Atopias_dermatitis_panel"),
    ("Bőr tulajdonságok panel", "Bor_tulajdonsagok_panel"),
    ("Haj tulajdonságok panel", "Haj_tulajdonsagok_panel"),
    ("Szem tulajdonságok panel", "Szem_tulajdonsagok_panel"),
    ("Magasság Elhizás BMI", "Magassag_Elhizas_panel"),
    ("Öregedési Hajlam", "Oregedesi_hajlam_panel"),
    ("Sportolási Hajlam", "Sport_hajlam_panel"),
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

                # ============================================================
                # WRAPPER – ÚJ FÁJLOK AUTOMATIKUS ÁTHELYEZÉSE
                # ============================================================

                OUTPUT_DIR = "eredmeny"
                os.makedirs(OUTPUT_DIR, exist_ok=True)

                # Fájlok listája a panel futása előtt
                before_files = set(os.listdir("."))

                # Panel futtatása
                module.run()

                # Fájlok listája a panel futása után
                after_files = set(os.listdir("."))

                # Új fájlok meghatározása
                new_files = after_files - before_files

                # Áthelyezés az eredmeny mappába
                for f in new_files:
                    src = os.path.join(".", f)
                    dst = os.path.join(OUTPUT_DIR, f)
                    if os.path.isfile(src):
                        shutil.move(src, dst)
                        print(f"📁 Áthelyezve: {f} → {OUTPUT_DIR}/")

                print("\n✔️ Minden új fájl átmozgatva az 'eredmeny' mappába.\n")
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
