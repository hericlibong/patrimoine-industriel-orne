"""Rassemble la matière d'un système industriel pour le lire.

Le découpage des systèmes est calculé — il regroupe les sites distants de moins
de trois kilomètres de proche en proche. Ce que le système raconte, en revanche,
ne se calcule pas : il faut lire les notices. Cet outil prépare cette lecture.

    python tools/lire_systeme.py --rang 2

Le rang 1 est le plus gros ensemble, la vallée de la Risle, déjà lue.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path

import duckdb


RACINE = Path(__file__).resolve().parents[1]
BASE = RACINE / "data" / "processed" / "patrimoine_orne_corpus_complet_v1.duckdb"
LIEN_A_3_KM = 3000


def ensembles(connection: duckdb.DuckDBPyConnection) -> list[list[str]]:
    """Les sites regroupés par proximité, du plus grand ensemble au plus petit."""
    lignes = connection.execute(
        "select reference_ia, x_lambert93, y_lambert93 from sites"
        " where x_lambert93 is not null"
    ).fetchall()
    parent = list(range(len(lignes)))

    def racine(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for i in range(len(lignes)):
        for j in range(i + 1, len(lignes)):
            if math.hypot(lignes[i][1] - lignes[j][1], lignes[i][2] - lignes[j][2]) < LIEN_A_3_KM:
                a, b = racine(i), racine(j)
                if a != b:
                    parent[b] = a

    groupes: dict[int, list[str]] = defaultdict(list)
    for index, ligne in enumerate(lignes):
        groupes[racine(index)].append(ligne[0])
    return sorted(groupes.values(), key=len, reverse=True)


def lire(rang: int) -> str:
    connection = duckdb.connect(str(BASE), read_only=True)
    references = ensembles(connection)[rang - 1]
    marques = ",".join(f"'{reference}'" for reference in references)

    sites = connection.execute(
        f"""
        select s.reference_ia, s.nom_principal, s.communes_source,
               s.lieux_dits_source, s.secteurs_codes, s.nombre_activites,
               s.distance_cours_eau_m, s.distance_ressource_minerale_m,
               s.nombre_protections_mh, s.nombre_objets_palissy,
               s.conservation_code, s.accessibilite_code, r.historique_source
        from sites s
        left join recits_sites r on r.site_id = s.site_id
        where s.reference_ia in ({marques})
        order by s.communes_source, s.reference_ia
        """
    ).fetchall()

    liens = connection.execute(
        f"""
        select source_reference, target_reference, type_relation_code, justification
        from relations_sites
        where source_reference in ({marques}) and target_reference in ({marques})
        """
    ).fetchall()

    evenements = connection.execute(
        f"""
        select reference_ia, count(*), min(date_min), max(date_max)
        from chronologie_sites where reference_ia in ({marques})
        group by 1
        """
    ).fetchall()
    par_site = {ligne[0]: ligne for ligne in evenements}
    connection.close()

    communes = Counter(site[2] for site in sites)
    secteurs: Counter[str] = Counter()
    for site in sites:
        for code in (site[4] or "").split("|"):
            if code.strip():
                secteurs[code.strip()] += 1

    lignes = [
        f"SYSTÈME N° {rang} — {len(sites)} sites",
        f"communes : {', '.join(f'{c} ({n})' for c, n in communes.most_common())}",
        f"secteurs : {', '.join(f'{c} {n}' for c, n in secteurs.most_common())}",
        f"liens documentés entre ces sites : {len(liens)}",
        "",
    ]
    for lien in liens:
        lignes.append(f"  LIEN {lien[0]} --{lien[2]}--> {lien[1]}")
        lignes.append(f"       « {lien[3]} »")
    lignes.append("")

    for index, site in enumerate(sites, 1):
        chrono = par_site.get(site[0])
        bornes = f"{chrono[2]} à {chrono[3]}" if chrono and chrono[2] else "—"
        lignes.append(f"--- [{index}/{len(sites)}] {site[0]} | {site[1]}")
        lignes.append(f"    {site[2]} | lieu-dit : {site[3] or '—'}")
        lignes.append(
            f"    {site[4]} | {site[5]} activité(s) | eau {site[6]} m"
            f" | minerai {site[7]} m | MH {site[8]} | Palissy {site[9]}"
        )
        lignes.append(
            f"    conservation : {site[10]} | accès : {site[11]}"
            f" | {chrono[1] if chrono else 0} événements datés, {bornes}"
        )
        lignes.append(f"    HIST : {site[12] or '(absent)'}")
        lignes.append("")
    return "\n".join(lignes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rang", type=int, required=True)
    parser.add_argument("--sortie", type=Path)
    args = parser.parse_args()
    texte = lire(args.rang)
    if args.sortie:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(texte, encoding="utf-8")
        print(f"écrit : {args.sortie} ({len(texte)} caractères)")
    else:
        print(texte)


if __name__ == "__main__":
    main()
