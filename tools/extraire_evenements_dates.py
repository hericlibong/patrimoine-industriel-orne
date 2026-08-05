"""Extrait des textes de notices les événements datés de chaque site.

Les textes citent plus de deux mille années qui ne sont structurées nulle part.
Une année seule ne sert à rien : ce qui compte, c'est ce qui s'est passé cette
année-là. Le script extrait donc des **événements datés** — une date, un type
d'événement, la formulation d'origine et la phrase qui l'établit.

Les conventions de datation sont celles de ``config/regles_modele.yml`` et de
``docs/regles_modele.md`` : une date imprécise reste un intervalle, la marge de
« vers une année » est de cinq ans, et une borne ouverte reste nulle. Le milieu
d'un intervalle n'est jamais présenté comme une date réelle.

Aucune écriture dans le corpus. La sortie est une proposition à relire.
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path

import duckdb


DEFAULT_DATABASE = Path("data/processed/patrimoine_orne_corpus_complet_v1.duckdb")
DEFAULT_OUTPUT = Path("data/interim/evenements_dates.csv")

MARGE_VERS_ANNEE = 5

MOIS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9,
    "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}

DERNIER_JOUR = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

# Type d'événement, reconnu par les mots de la phrase. L'ordre compte : le
# premier motif rencontré l'emporte, du plus spécifique au plus général.
TYPES_EVENEMENT: tuple[tuple[str, str], ...] = (
    # « fermeture » et non « fermentation » : le motif exige une fin de mot.
    ("cessation", r"\bcessation|\bcesse\b|arr[êe]t de l|\bferm(?:é|ée|ee|eture)\b|"
                  r"\babandon|\binactif|\binactive|\bd[ée]saffect"),
    ("destruction", r"\bincendi|\bd[ée]trui|\bd[ée]moli|\bruin[ée]|\bsinistre|\bbombard"),
    # Placé avant la création : « reconstruite » contient « construit ».
    ("reconstruction", r"\breconstru|\brestaur|\br[ée]am[ée]nag|\br[ée]nov|\brelev[ée]"),
    # « Usine installée en 1819 » est une création ; « machine installée en
    # 1903 » est un équipement. Le sujet de la phrase fait la différence.
    ("creation", r"\bconstruit|\bconstruction|\bcr[ée]{2}|\b[ée]tabli|\bfond[ée]|"
                 r"^(?:usine|moulin|forge|affinerie|fenderie|tr[ée]filerie|"
                 r"filature|tissage|papeterie|tannerie|fonderie|laminoir|scierie|"
                 r"briqueterie|tuilerie|laiterie|minoterie|mine|carri[èe]re|"
                 r"centrale|atelier|[ée]tablissement|manufacture|haut fourneau)"
                 r"\b[^.;]{0,60}?\binstall"),
    ("attestation", r"\battest|\bmentionn|\bsignal[ée]|\bcit[ée]e? en|figure en"),
    ("agrandissement", r"\bagrandi|augmentation de construction|\bextension|"
                       r"nouveau b[âa]timent|nouveaux ateliers"),
    ("acquisition", r"\bacqui|\brachet|vendue? à|c[ée]d[ée]e? à|propri[ée]t[ée] de"),
    ("conversion", r"\bconverti|\btransform[ée]|affect[ée]e? (?:à|au)|\bremplac[ée]|"
                   r"\br[ée]occup|\br[ée]utilis|\breconvert"),
    ("equipement", r"\binstall|\b[ée]quip[ée]|mise en service|\bturbine|"
                   r"machine à vapeur|roue hydraulique|chaudi[èe]re|\bbobines|"
                   r"\bbroches|\bm[ée]tiers|\bfourneaux|\bpilons|\bmachines"),
    ("reglementation", r"\br[ée]glement|ordonnance royale|arr[êe]t[ée] pr[ée]fectoral|"
                       r"\bd[ée]cret|\bautoris"),
    ("exploitation", r"\bexploit[ée]e?\s+(?:en|à partir|depuis|par)|"
                     r"b[âa]timents? occup[ée]|\bint[ée]gr[ée]e?\s+au|\brepris[e]?\s+par"),
    ("production", r"\bproduis|\bproduction|\bconsommait|\btonnes|\bkg de|\brames|"
                   r"\bpressait|capacit[ée] de production|\bsuperficie|\bsurface"),
    ("emploi", r"\bouvriers|\bouvri[èe]res|\bemploy[ée]s|personnes employ|\bsalari"),
)

# Unités qui suivent un nombre : « 1500 tonnes » n'est pas l'année 1500.
UNITES = (
    r"tonnes?|kg|quintaux|hectolitres?|litres?|m2|m²|francs?|broches?|"
    r"m[ée]tiers?|fuseaux|bobines?|ouvriers?|ouvri[èe]res?|employ[ée]s?|"
    r"camemberts?|rames?|hectares?|HP|CV|ch\b|kw|volts?|pi[èe]ces?|fromages?|"
    r"paires?|douzaines?|st[èe]res?|mm|cm|habitants?|personnes"
)

# Motifs de date, du plus spécifique au plus général.
MOTIFS_DATE: tuple[tuple[str, str], ...] = (
    ("intervalle", r"entre\s+(1[3-9]\d{2})\s+et\s+(1[3-9]\d{2})"),
    ("jour", r"(\d{1,2})\s+(" + "|".join(MOIS) + r")\s+(1[3-9]\d{2})"),
    ("mois", r"\b(" + "|".join(MOIS) + r")\s+(1[3-9]\d{2})"),
    ("vers_annee", r"vers\s+(1[3-9]\d{2})"),
    ("avant", r"avant\s+(1[3-9]\d{2})"),
    ("apres", r"(?:apr[èe]s|depuis)\s+(1[3-9]\d{2})"),
    ("avant_jusque", r"jusqu'en\s+(1[3-9]\d{2})"),
    ("decennie", r"ann[ée]es\s+(1[3-9]\d0)"),
    ("quart_siecle", r"([1-4])(?:er|e|ème)?\s+quart\s+(\d{1,2})e\s+si[èe]cle"),
    ("moitie_siecle", r"([12])(?:re|ère|e|ème)?\s+moiti[ée]\s+(\d{1,2})e\s+si[èe]cle"),
    ("siecle", r"(\d{1,2})e\s+si[èe]cle"),
    ("annee", r"\b(1[3-9]\d{2})\b"),
)


def normalise(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def split_segments(text: str) -> list[str]:
    parts = re.split(r"\s*;\s*|(?<=[a-z0-9\)])\.\s+", text)
    return [p.strip() for p in parts if p.strip()]


def borne_annee(annee: int, debut: bool) -> str:
    return f"{annee}-01-01" if debut else f"{annee}-12-31"


def resoudre_date(code: str, match: re.Match[str]) -> tuple[str, str, str]:
    """Retourne (minimum, maximum, code_precision) selon les règles du projet."""
    if code == "intervalle":
        return borne_annee(int(match.group(1)), True), borne_annee(int(match.group(2)), False), "intervalle"
    if code == "jour":
        jour, mois, annee = int(match.group(1)), MOIS[normalise(match.group(2))], int(match.group(3))
        valeur = f"{annee}-{mois:02d}-{jour:02d}"
        return valeur, valeur, "jour"
    if code == "mois":
        mois, annee = MOIS[normalise(match.group(1))], int(match.group(2))
        return f"{annee}-{mois:02d}-01", f"{annee}-{mois:02d}-{DERNIER_JOUR[mois]:02d}", "mois"
    if code == "vers_annee":
        annee = int(match.group(1))
        return (borne_annee(annee - MARGE_VERS_ANNEE, True),
                borne_annee(annee + MARGE_VERS_ANNEE, False), "vers_annee")
    if code in ("avant", "avant_jusque"):
        return "", borne_annee(int(match.group(1)) - 1, False), "avant"
    if code == "apres":
        return borne_annee(int(match.group(1)) + 1, True), "", "apres"
    if code == "decennie":
        annee = int(match.group(1))
        return borne_annee(annee, True), borne_annee(annee + 9, False), "decennie"
    if code == "quart_siecle":
        quart, siecle = int(match.group(1)), int(match.group(2))
        debut = (siecle - 1) * 100 + 1 + (quart - 1) * 25
        return borne_annee(debut, True), borne_annee(debut + 24, False), "quart_siecle"
    if code == "moitie_siecle":
        moitie, siecle = int(match.group(1)), int(match.group(2))
        debut = (siecle - 1) * 100 + 1 + (moitie - 1) * 50
        return borne_annee(debut, True), borne_annee(debut + 49, False), "moitie_siecle"
    if code == "siecle":
        siecle = int(match.group(1))
        return borne_annee((siecle - 1) * 100 + 1, True), borne_annee(siecle * 100, False), "siecle"
    annee = int(match.group(1))
    return borne_annee(annee, True), borne_annee(annee, False), "annee"


def type_evenement(segment: str) -> str:
    plain = normalise(segment)
    for nom, motif in TYPES_EVENEMENT:
        if re.search(normalise(motif), plain):
            return nom
    return "indetermine"


def charger_communes(connection: duckdb.DuckDBPyConnection) -> tuple[dict[str, str], set[str]]:
    """Commune de chaque site, et ensemble des communes du corpus."""
    par_site: dict[str, str] = {}
    toutes: set[str] = set()
    for reference, communes in connection.execute(
        "select reference_ia, communes_source from sites"
    ).fetchall():
        par_site[reference] = normalise(communes or "")
        for commune in (communes or "").split("|"):
            valeur = normalise(commune.strip())
            if len(valeur) > 5:
                toutes.add(valeur)
    return par_site, toutes


def extraire(database: Path, output: Path) -> dict[str, int]:
    connection = duckdb.connect(str(database), read_only=True)
    communes_par_site, communes_corpus = charger_communes(connection)
    notices = connection.execute(
        """
        select reference_ia, nom_site, historique_source
        from recits_sites
        where historique_source is not null and historique_source <> ''
        """
    ).fetchall()

    lignes: list[dict[str, str]] = []
    for reference, nom, historique in notices:
        for ordre, segment in enumerate(split_segments(historique), 1):
            positions_prises: list[tuple[int, int]] = []
            trouvees: list[tuple[int, int, str, re.Match[str]]] = []
            for code, motif in MOTIFS_DATE:
                for match in re.finditer(motif, segment, re.IGNORECASE):
                    # Une même date ne doit pas être comptée deux fois par un
                    # motif plus général : « vers 1850 » ne redevient pas 1850.
                    if any(d <= match.start() < f for d, f in positions_prises):
                        continue
                    # « 1500 tonnes » est une quantité, pas une année.
                    if re.match(rf"\s*(?:{UNITES})", segment[match.end():], re.IGNORECASE):
                        continue
                    positions_prises.append((match.start(), match.end()))
                    trouvees.append((match.start(), match.end(), code, match))

            trouvees.sort()
            for index, (debut, fin, code, match) in enumerate(trouvees):
                # Le type se lit dans le texte qui précède immédiatement la
                # date, non dans tout le segment : « construction d'une filature
                # en 1903, agrandie en 1907 » contient deux événements
                # différents.
                origine = trouvees[index - 1][1] if index else 0
                contexte = segment[origine:fin]
                type_lu = type_evenement(contexte)
                if type_lu == "indetermine":
                    type_lu = type_evenement(segment)
                minimum, maximum, precision = resoudre_date(code, match)
                # Une phrase qui nomme une autre commune peut dater le site
                # voisin plutôt que celui-ci. Le cas est signalé, jamais tranché
                # automatiquement.
                plain = normalise(segment)
                autres = sorted(
                    commune
                    for commune in communes_corpus
                    if commune in plain and commune not in communes_par_site.get(reference, "")
                )
                lignes.append(
                    {
                        "reference_ia": reference,
                        "nom_site": nom,
                        "ordre_segment": str(ordre),
                        "type_evenement": type_lu,
                        "date_min": minimum,
                        "date_max": maximum,
                        "precision_code": precision,
                        "texte_source": match.group(0),
                        "autre_lieu_cite": autres[0] if autres else "",
                        "phrase_source": segment,
                    }
                )

    output.parent.mkdir(parents=True, exist_ok=True)
    lignes.sort(key=lambda r: (r["reference_ia"], int(r["ordre_segment"]), r["date_min"]))
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(lignes[0]))
        writer.writeheader()
        writer.writerows(lignes)

    return {
        "notices_lues": len(notices),
        "evenements_dates": len(lignes),
        "sites_concernes": len({ligne["reference_ia"] for ligne in lignes}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    for key, value in extraire(args.database, args.output).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
