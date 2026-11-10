"""Indexe tous les dossiers du texte extrait de la série S des Archives de l'Orne.

L'unité produite est un dossier d'archives. Les rapprochements proposés servent
à retrouver les sources d'un lieu et demandent une lecture avant intégration.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parents[1]
SOURCE = RACINE / "data/raw/archives_orne/2026-11-10/serie_s_moulins_usines.txt"
SORTIE = RACINE / "docs/archives_orne_serie_s.csv"


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte.casefold())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in texte if not unicodedata.combining(c))).strip()


def indexer() -> list[dict]:
    lignes = SOURCE.read_text(encoding="utf-8").splitlines()
    dossiers = []
    courant = None
    cote, commune, page = "", "", 0
    supplement = False
    for index, ligne in enumerate(lignes):
        ligne = ligne.strip()
        if ligne.startswith("Dossiers de moulins recensés"):
            supplement = True
        marque_page = re.fullmatch(r"--- PAGE (\d+) ---", ligne)
        if marque_page:
            page = int(marque_page[1])
            continue
        if not ligne or ligne.isdigit() or ligne.startswith("Archives départementales"):
            continue
        marque_cote = re.match(r"^(S\d{3,4})\s+(.+)", ligne)
        suivante = next((s.strip() for s in lignes[index + 1:] if s.strip()), "")
        marque_commune = (
            re.fullmatch(r"[A-ZÀ-Ý][A-Za-zÀ-ÿ '’().-]{2,65}\.", ligne)
            and re.match(r"Dossiers?\s+\d+", suivante)
            and not re.match(
                r"(?:Plan|Projet|Copie|Extrait|Dessin|Procès|Règlement|Croquis|Arrêté|"
                r"Pétition|Demande|Délibération|Autorisation|Réclamation|Correspondance|Voir)\b",
                ligne,
            )
        )
        marque_dossier = re.match(r"^Dossiers?\s+(\d+)\s*:\s*(.*)", ligne)
        if marque_cote or marque_commune or marque_dossier:
            if courant:
                dossiers.append(courant)
                courant = None
        if marque_cote:
            cote = marque_cote[1]
            commune = re.sub(r"\s+\d{4}.*$", "", marque_cote[2]).rstrip(". ")
            if supplement:
                courant = {"cote": cote, "dossier": "", "commune": "Plusieurs communes",
                           "page": page, "intitule": commune, "description": ""}
        elif marque_commune:
            commune = ligne.rstrip(". ")
        elif marque_dossier:
            courant = {"cote": cote, "dossier": marque_dossier[1], "commune": commune,
                       "page": page, "intitule": marque_dossier[2], "description": ""}
        elif courant:
            courant["description"] += " " + ligne
    if courant:
        dossiers.append(courant)
    return dossiers


def main() -> None:
    with (RACINE / "data/exports/sites_corpus_complet_v1.csv").open(encoding="utf-8") as fichier:
        sites = list(csv.DictReader(fichier))
    complements = yaml.safe_load((RACINE / "data/manual/lieux_complementaires.yml").read_text(encoding="utf-8"))["lieux"]
    for site in complements:
        sites.append({"reference_ia": site["ref"], "communes_source": site["commune"],
                      "nom_principal": site["nom"], "lieux_dits_source": site["lieuDit"]})
    dossiers = indexer()
    for dossier in dossiers:
        commune = normaliser(dossier["commune"])
        locaux = [s for s in sites if normaliser(s["communes_source"]) == commune]
        corps = normaliser(dossier["intitule"] + " " + dossier["description"])
        proposes = []
        for site in locaux:
            lieu = normaliser(site["lieux_dits_source"])
            if len(lieu) >= 5 and lieu in corps:
                proposes.append(site["reference_ia"])
        dossier["references_commune"] = " | ".join(s["reference_ia"] for s in locaux)
        dossier["rapprochements_lieu_dit"] = " | ".join(proposes)
        dossier["instruction"] = "lecture_du_dossier"
        dossier["source"] = "https://archives.orne.fr/sites/default/files/2020-09/FRAD061_INV_S_S_MOULINS_USINES.pdf"
        dossier["description"] = dossier["description"].strip()
    with SORTIE.open("w", encoding="utf-8-sig", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(dossiers[0]))
        writer.writeheader()
        writer.writerows(dossiers)
    total = len(re.findall(r"(?m)^Dossiers?\s+\d+\s*:", SOURCE.read_text(encoding="utf-8")))
    numerotes = sum(bool(d["dossier"]) for d in dossiers)
    if numerotes != total:
        raise ValueError(f"{len(dossiers)} dossiers indexés pour {total} en-têtes")
    print(f"{numerotes} dossiers et {len(dossiers) - numerotes} rubriques de supplément indexés sur 135 pages.")


if __name__ == "__main__":
    main()
