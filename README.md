# GenEM
Genetic analysis toolkit – first working version
# 📘 Genetic Predisposition Analysis Panel System – Three‑Level Knowledge Framework
## 🇭🇺 genetikai Elemző Müszerfal aza GenEM
## 🇭🇺 Magyar leírás

👉 [Kattints ide a magyar verzióhoz](GenEM/read/OlvassEl.md)


This program is a fully offline genetic analysis system designed to interpret various predispositions and traits from MyHeritage RAW DNA files.

Its goal is to present genetic patterns in a clear, understandable way, showing how they may influence:

- metabolism
- physical characteristics
- lifestyle tendencies
- overall biological functioning

During development, the project focused on:

- security
- transparency
- GDPR compliance
- ensuring that user data never leaves the local machine

The program fully complies with the European Union’s General Data Protection Regulation (GDPR).

---

## 🧩 Panels Included

1. Allergy predisposition panel
2. Atopic dermatitis panel
3. Skin traits panel
4. Food sensitivity panel
5. Lifestyle predisposition panel (15 submodules)
6. Hair traits panel
7. Histamine intolerance panel
8. Joint predisposition panel
9. Lactose panel
10. Visible traits panel
11. Height & obesity panel
12. Aging predisposition panel
13. Sport predisposition panel
14. Eye traits panel
15. Y‑haplogroup panel
16. SNP verification panel

Each panel runs independently and generates its own TXT report.

---

## 🟦 1) BASIC LEVEL – What does the program do?

The program reads genetic information from MyHeritage RAW DNA files and, through various “predisposition panels,” shows what genetic tendencies the user may have.

It is not a diagnostic tool — it only indicates genetic predisposition.

Steps:
1. Detects MyHeritage .csv files
2. User selects which file to analyze
3. Panel reads key SNPs
4. Calculates weighted scores
5. Displays results
6. Generates a detailed TXT report

---

## 🟩 2) EDUCATIONAL LEVEL – How does the analysis work?

A MyHeritage RAW DNA file is a simple table where each row describes a genetic variant called an SNP (Single Nucleotide Polymorphism).

Example row:

rs4988235,7,117199646,AG

This represents:
- rsID (unique identifier)
- Chromosome number
- Position
- Genotype (two alleles, e.g., AG)

The program:
- Finds relevant SNPs
- Checks for risk alleles
- Counts them
- Applies weights
- Calculates a total score
- Assigns a category (low / moderate / elevated predisposition)

---

## 🟥 3) SCIENTIFIC LEVEL – Deep genetic explanation

The MyHeritage RAW DNA file contains SNP‑based genotyping, covering ~0.02% of the genome at scientifically validated locations.

### SNPs
Single nucleotide differences that may affect:
- enzyme function
- hormone production
- immune response
- metabolism
- allergic reactions
- drug metabolism

### Risk alleles
Examples:
- rs4988235 G → lactose intolerance
- rs2251746 T → higher IgE levels
- rs1815739 T → slow‑twitch muscle fibers

### Scoring
- 0 risk alleles → no effect
- 1 → heterozygous effect
- 2 → homozygous effect
- Weighted scoring applied
- Categories summed and normalized

This follows the principles of polygenic risk scoring.

---

# 🧬 Data Security & GDPR Compliance

- All processing is offline
- No internet connection
- No data transmission
- RAW files and results remain on the user’s machine
- No third‑party sharing

⚠️ RAW DNA files contain highly sensitive personal genetic information. Handle them securely and never share without explicit permission.

The program is intended for personal insight and education. It is not a medical diagnostic tool.
👉 [Kattints ide a magyar verzióhoz](GenEM/read/OlvassEl.md)
---

## ❤️ Support / Sponsorship

If you find GenEM useful and would like to support its development, you can become a sponsor.

Your support helps me continue improving the project, adding new features, and keeping everything up to date.

## Support my work

If you like what I'm building and want to support me, you can do it here:

👉 **Buy Me a Coffee:** https://buymeacoffee.com/orczanz  
👉 **Revolut:** https://revolut.me/orczanz

Thank you for considering supporting the project!
