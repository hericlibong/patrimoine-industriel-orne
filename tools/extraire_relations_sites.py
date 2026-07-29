"""Extrait des textes de notices les relations entre sites du corpus.

Trois sorties distinctes, jamais mélangées :

- ``relations_candidates`` : un lien affirmé par une notice entre deux
  installations, avec la phrase qui l'établit ;
- ``mentions_externes`` : un lien affirmé vers un lieu hors corpus, utile au
  récit des réseaux mais sans cible interne ;
- ``liens_exploitants`` : un rapprochement **déduit** de la présence d'un même
  nom d'exploitant dans plusieurs notices. Ce n'est pas une relation affirmée
  par une source et le fichier reste séparé pour cette raison.

Aucune écriture dans le corpus. La sortie est une proposition à relire.
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import duckdb


DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_OUTPUT_DIR = Path("data/interim")

# Types d'installation qui désignent un site industriel dans une mention.
INSTALLATIONS = (
    "haut fourneau",
    "hauts fourneaux",
    "affinerie",
    "affineries",
    "fenderie",
    "fenderies",
    "forge",
    "forges",
    "tréfilerie",
    "tréfileries",
    "laminoir",
    "fonderie",
    "papeterie",
    "filature",
    "filatures",
    "tissage",
    "moulin",
    "usine",
    "usines",
    "laiterie",
    "tannerie",
    "brasserie",
    "minoterie",
    "scierie",
    "mine",
)

# Dépendances qui ne désignent pas un site mais un propriétaire ou une
# institution. Elles sont écartées des relations entre sites.
NON_SITES = (
    "abbaye",
    "château",
    "chateau",
    "comte",
    "comtesse",
    "baron",
    "baronnie",
    "marquis",
    "seigneur",
    "domaine",
    "prieuré",
    "chapitre",
    "évêché",
    "commune",
    "société",
    "compagnie",
    "famille",
)

INSTALL_RE = "|".join(sorted(INSTALLATIONS, key=len, reverse=True))

# Déterminants pouvant précéder le type d'installation dans une mention.
ARTICLE = r"(?:l[ae']\s*|les\s+|le\s+|du\s+|des\s+|au\s+|aux\s+|une?\s+|sa\s+|son\s+)?"

# Motifs de lien. Chaque motif isole le fragment décrivant la cible.
MOTIFS: tuple[tuple[str, str, str], ...] = (
    (
        "approvisionnement",
        "sortant",
        rf"aliment(?:ait|aient|é|ée|és|ées)\s+(?:en\s+(?:\w+\s+){{0,3}})?"
        rf"{ARTICLE}((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
    (
        "approvisionnement",
        "entrant",
        rf"aliment(?:é|ée|és|ées)\s+en\s+(?:\w+\s+){{1,4}}par\s+"
        rf"{ARTICLE}((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
    (
        "fourniture",
        "entrant",
        rf"(?:fourni|fournis|fournie|fournies|produits?|produite?s?|"
        rf"prepar[ée]e?s?|retordage|assembl[ée]e?s?)\s+"
        rf"(?:par|à)\s+{ARTICLE}((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
    (
        "dependance",
        "sortant",
        rf"d[ée]pend(?:ant|ait|aient|ante)\s+(?:de\s+l[ae']?\s*|du\s+|des\s+|d')"
        rf"((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
    (
        "transfert",
        "sortant",
        rf"transf[ée]r[ée]e?s?\s+(?:en\s+\d{{4}}\s+|vers\s+\d{{4}}\s+|"
        rf"fin\s+\w+\s+si[èe]cle\s+)?(?:à|au|vers|dans|sur)\s+"
        rf"{ARTICLE}((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
    (
        "liaison",
        "sortant",
        rf"reli[ée]e?s?\s+(?:en\s+\d{{4}}\s+)?(?:par[^,;.]{{0,40}}\s+)?"
        rf"(?:à|au|aux)\s+{ARTICLE}((?:{INSTALL_RE})\b[^.;]{{0,80}})",
    ),
)

# Flux de matières et de marchés vers l'extérieur du corpus. Ils ne relient pas
# deux sites de l'Orne mais montrent que ces usines travaillaient pour des
# approvisionnements et des marchés lointains.
MOTIFS_FLUX: tuple[tuple[str, str], ...] = (
    ("approvisionnement_externe", r"(?:provenant|en\s+provenance)\s+d[eu']\s*([^.;]{3,70})"),
    ("approvisionnement_externe", r"import[ée]e?s?\s+d[eu']\s*([^.;]{3,70})"),
    ("marche_externe", r"export[ée]e?s?\s+(?:en|à|aux|dans)\s+([^.;]{3,70})"),
    ("marche_externe", r"vendus?e?s?\s+(?:en|à|aux|dans)\s+([^.;]{3,70})"),
    ("marche_externe", r"destin[ée]e?s?\s+à\s+l['ae]?\s*([^.;]{3,70})"),
)

# Exploitants : noms propres qui reviennent d'une notice à l'autre.
MOTIF_EXPLOITANT = re.compile(
    r"(?:acquis|acquise|acquises|acquis|rachet[ée]e?s?|exploit[ée]e?s?)"
    r"(?:\s+en\s+\d{4})?\s+par\s+"
    r"(?:l[ae']\s*|les\s+|le\s+)?([^,;.]{3,80})",
    re.IGNORECASE,
)


def normalise(value: str) -> str:
    """Minuscule sans accent ni ponctuation, pour les comparaisons."""
    decomposed = unicodedata.normalize("NFD", value.lower())
    stripped = "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", stripped).strip()


def split_segments(text: str) -> list[str]:
    """Découpe un historique en segments porteurs d'une seule affirmation."""
    parts = re.split(r"\s*;\s*|(?<=[a-z0-9\)])\.\s+", text)
    return [p.strip() for p in parts if p.strip()]


def load_sites(connection: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        select reference_ia, nom_principal, communes_source, lieux_dits_source
        from sites
        """
    ).fetchall()
    sites = []
    for reference, nom, communes, lieux_dits in rows:
        sites.append(
            {
                "reference": reference,
                "nom": nom or "",
                "communes": [c.strip() for c in (communes or "").split("|") if c.strip()],
                "lieux_dits": [l.strip() for l in (lieux_dits or "").split("|") if l.strip()],
            }
        )
    return sites


# Mots trop courants pour identifier un lieu à eux seuls.
MOTS_NON_DISTINCTIFS = {
    "usine", "moulin", "forge", "ferme", "grand", "grande", "petit", "petite",
    "saint", "sainte", "notre", "dame", "haut", "basse", "haute", "vieux",
    "vieille", "neuf", "neuve", "bois", "pont", "eglise", "chateau", "ville",
    "sur", "sous", "les", "des", "lieu", "dit", "dite", "puits", "fosse",
    "cite", "ouvriere", "papier", "fer", "tan", "chaise", "launay",
}

# Un type d'installation n'est pas un nom de lieu : « affinerie de Varenne »
# doit être résolu par « Varenne », jamais par « affinerie ».
MOTS_NON_DISTINCTIFS |= {
    "affinerie", "affineries", "fenderie", "fenderies", "trefilerie",
    "trefileries", "laminoir", "laminoirs", "fonderie", "fonderies",
    "papeterie", "papeteries", "filature", "filatures", "tissage", "tissages",
    "laiterie", "laiteries", "tannerie", "tanneries", "brasserie", "minoterie",
    "scierie", "scieries", "fourneau", "fourneaux", "quincaillerie",
    "fromagerie", "beurrerie", "briqueterie", "tuilerie", "clouterie",
    "distillerie", "cidrerie", "verrerie", "abattoir", "carriere",
    "extraction", "industrie", "industriel", "industrielle", "fabrication",
    "construction", "materiel", "produits", "alimentaires", "metaux",
    "mecanique", "electrique", "centrale", "atelier", "ateliers",
    "batiment", "magasin", "logement", "logements", "passementerie",
    "chaussures", "habillement", "blanchiment", "ebenisterie",
}


def tokens_distinctifs(value: str) -> set[str]:
    """Mots suffisamment distinctifs pour identifier un lieu."""
    return {
        token
        for token in normalise(value).split()
        if len(token) >= 5 and token not in MOTS_NON_DISTINCTIFS
    }


def build_gazetteer(sites: Iterable[dict[str, Any]]) -> dict[str, set[str]]:
    """Associe un mot de lieu distinctif aux références de sites concernées."""
    gazetteer: dict[str, set[str]] = defaultdict(set)
    for site in sites:
        sources = list(site["communes"]) + list(site["lieux_dits"]) + [site["nom"]]
        for value in sources:
            for token in tokens_distinctifs(value):
                gazetteer[token].add(site["reference"])
    return gazetteer


def installations_mentionnees(mention: str) -> set[str]:
    """Types d'installation cités dans une mention."""
    normalised = normalise(mention)
    return {
        installation
        for installation in INSTALLATIONS
        if re.search(rf"\b{re.escape(normalise(installation))}", normalised)
    }


def resolve(
    mention: str,
    gazetteer: dict[str, set[str]],
    source: str,
    profils: dict[str, str],
) -> tuple[str, str]:
    """Cherche la ou les références correspondant à une mention.

    La résolution croise deux signaux : le nom de lieu et le type
    d'installation. Une mention comme « la forge d'Aube » ne doit pas retenir
    tous les sites de la commune d'Aube, mais seulement ceux dont la notice
    décrit une forge ou une affinerie.
    """
    normalised = normalise(mention)
    scores: dict[str, int] = defaultdict(int)
    for token, references in gazetteer.items():
        if re.search(rf"\b{re.escape(token)}\b", normalised):
            for reference in references:
                scores[reference] += 1
    scores.pop(source, None)
    if not scores:
        return "", "non_resolu"

    # Un site qui concorde sur deux repères de lieu — commune et lieu-dit par
    # exemple — prime sur celui qui n'en partage qu'un.
    meilleur = max(scores.values())
    hits = {reference for reference, score in scores.items() if score == meilleur}

    types = installations_mentionnees(mention)
    if types and len(hits) > 1:
        affines = {
            reference
            for reference in hits
            if any(normalise(t) in profils.get(reference, "") for t in types)
        }
        if affines:
            hits = affines

    if len(hits) == 1:
        return next(iter(hits)), "resolu"
    return "|".join(sorted(hits)), "ambigu"


def mentions_a_ecarter(mention: str) -> bool:
    """Vrai lorsque la mention désigne une institution ou un propriétaire."""
    normalised = normalise(mention)
    return any(normalise(word) in normalised for word in NON_SITES)


def extract(database: Path, output_dir: Path) -> dict[str, int]:
    connection = duckdb.connect(str(database), read_only=True)
    sites = load_sites(connection)
    gazetteer = build_gazetteer(sites)
    # Profil textuel d'un site : son nom et ses libellés d'activité, servant à
    # vérifier qu'une mention de type « forge » désigne bien ce site.
    profils = {
        reference: normalise(f"{nom} {libelles or ''}")
        for reference, nom, libelles in connection.execute(
            """
            select s.reference_ia, s.nom_principal,
                   string_agg(a.libelle_source, ' ')
            from sites s left join activites a on a.site_id = s.site_id
            group by 1, 2
            """
        ).fetchall()
    }
    notices = connection.execute(
        """
        select reference_ia, nom_site, historique_source
        from recits_sites
        where historique_source is not null and historique_source <> ''
        """
    ).fetchall()

    relations: list[dict[str, str]] = []
    externes: list[dict[str, str]] = []
    exploitants: list[dict[str, str]] = []

    for reference, nom, historique in notices:
        for segment in split_segments(historique):
            for type_lien, direction, motif in MOTIFS:
                for match in re.finditer(motif, segment, re.IGNORECASE):
                    mention = match.group(1).strip(" ,")
                    if mentions_a_ecarter(mention):
                        continue
                    cible, statut = resolve(mention, gazetteer, reference, profils)
                    ligne = {
                        "reference_source": reference,
                        "nom_source": nom,
                        "type_lien": type_lien,
                        "direction": direction,
                        "mention": mention,
                        "reference_cible": cible,
                        "statut_resolution": statut,
                        "phrase_source": segment,
                    }
                    if statut == "non_resolu":
                        externes.append(ligne)
                    else:
                        relations.append(ligne)
            for type_flux, motif in MOTIFS_FLUX:
                for match in re.finditer(motif, segment, re.IGNORECASE):
                    externes.append(
                        {
                            "reference_source": reference,
                            "nom_source": nom,
                            "type_lien": type_flux,
                            "direction": "sortant"
                            if type_flux == "marche_externe"
                            else "entrant",
                            "mention": match.group(1).strip(" ,"),
                            "reference_cible": "",
                            "statut_resolution": "hors_corpus",
                            "phrase_source": segment,
                        }
                    )
            for match in MOTIF_EXPLOITANT.finditer(segment):
                exploitants.append(
                    {
                        "reference_source": reference,
                        "nom_source": nom,
                        "exploitant": match.group(1).strip(" ,"),
                        "phrase_source": segment,
                    }
                )

    relations = _dedupe(relations, ("reference_source", "reference_cible", "type_lien"))
    externes = _dedupe(externes, ("reference_source", "mention"))

    output_dir.mkdir(parents=True, exist_ok=True)
    _write(output_dir / "relations_candidates.csv", relations)
    _write(output_dir / "mentions_externes.csv", externes)
    _write(output_dir / "liens_exploitants.csv", exploitants)

    return {
        "relations_candidates": len(relations),
        "mentions_externes": len(externes),
        "mentions_exploitants": len(exploitants),
        "notices_lues": len(notices),
    }


def _dedupe(rows: list[dict[str, str]], cles: tuple[str, ...]) -> list[dict[str, str]]:
    """Retire les doublons produits par plusieurs motifs sur une même phrase."""
    vus: set[tuple[str, ...]] = set()
    uniques = []
    for row in rows:
        signature = tuple(row[cle] for cle in cles)
        if signature in vus:
            continue
        vus.add(signature)
        uniques.append(row)
    return uniques


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    counts = extract(args.database, args.output_dir)
    for key, value in counts.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
