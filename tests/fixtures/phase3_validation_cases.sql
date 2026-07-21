-- Cas synthetiques de validation finale de la phase 3.
-- Ils ne decrivent aucun lieu reel de l'Orne.

INSERT INTO sources (
    source_id, titre, producteur, role_code, methode_acces_code,
    statut_audit_code, date_dernier_audit, notes, cree_par
) VALUES (
    'test_casias', 'Source CASIAS fictive', 'Projet - test',
    'elargissement', 'fichier_test', 'test', DATE '2026-07-20',
    'Donnees synthetiques reservees aux tests.', 'fixture'
);

INSERT INTO sites (
    site_id, nom_principal, niveau_structurel_code,
    commune_actuelle_code_insee, commune_actuelle_nom, lieu_dit_principal,
    statut_corpus_code, decision_inclusion_code, motif_decision,
    fiabilite_code, notes_internes, cree_par
) VALUES
    (
        '10000000-0000-4000-8000-000000000004', 'Scierie Simple du Test',
        'site_principal', '61004', 'Commune Test D', 'Le Bois',
        'cartographiable', 'inclus',
        'Un site, une activite, une source et une geometrie.',
        'forte', 'Cas simple fictif.', 'fixture'
    ),
    (
        '10000000-0000-4000-8000-000000000005', 'Filature Reconvertie du Test',
        'site_principal', '61005', 'Commune Test E', 'Le Bourg',
        'cartographiable', 'inclus',
        'Activite textile ancienne et usage culturel contemporain distinct.',
        'forte', 'Cas reconverti fictif.', 'fixture'
    ),
    (
        '10000000-0000-4000-8000-000000000006', 'Moulin des Pres',
        'site_principal', '61006', 'Commune Test F', 'Les Pres',
        'candidat', 'a_verifier',
        'Notice patrimoniale a rapprocher eventuellement d une fiche CASIAS.',
        'faible', 'Premiere branche du rapprochement fictif.', 'fixture'
    ),
    (
        '10000000-0000-4000-8000-000000000007', 'Ancien moulin des Pres',
        'site_principal', '61006', 'Commune Test F', 'Les Pres',
        'candidat', 'a_verifier',
        'Ressemblance insuffisante pour fusionner automatiquement les notices.',
        'faible', 'Seconde branche du rapprochement fictif.', 'fixture'
    );

INSERT INTO activites (
    activite_id, site_id, secteur_code, activite_code,
    activite_libelle_source, type_installation_code,
    debut_min, debut_max, debut_precision_code, debut_texte_source,
    fin_min, fin_max, fin_precision_code, fin_texte_source,
    principale, fiabilite_code, cree_par
) VALUES
    (
        '20000000-0000-4000-8000-000000000005',
        '10000000-0000-4000-8000-000000000004',
        'bois', 'scierie', 'Scierie mecanique', 'usine',
        DATE '1910-01-01', DATE '1910-12-31', 'annee', '1910',
        DATE '1980-01-01', DATE '1980-12-31', 'annee', '1980',
        true, 'forte', 'fixture'
    ),
    (
        '20000000-0000-4000-8000-000000000006',
        '10000000-0000-4000-8000-000000000005',
        'textile', 'filature', 'Filature de laine', 'usine',
        DATE '1850-01-01', DATE '1850-12-31', 'annee', '1850',
        DATE '1960-01-01', DATE '1960-12-31', 'annee', '1960',
        true, 'forte', 'fixture'
    );

INSERT INTO etats_actuels (
    etat_actuel_id, site_id, conservation_code,
    accessibilite_code, date_verification, methode_verification_code,
    fiabilite_code, version_numero, motif_version_code, notes, cree_par
) VALUES
    (
        '30000000-0000-4000-8000-000000000005',
        '10000000-0000-4000-8000-000000000004',
        'partiellement_conserve', 'visible_espace_public', DATE '2026-07-20',
        'terrain_test', 'forte', 1, 'nouvelle_observation',
        'Etat actuel fictif du cas simple.', 'fixture'
    ),
    (
        '30000000-0000-4000-8000-000000000006',
        '10000000-0000-4000-8000-000000000005',
        'conserve', 'visitable', DATE '2026-07-20',
        'terrain_test', 'forte', 1, 'nouvelle_observation',
        'Usage culturel fictif, distinct de l activite historique.', 'fixture'
    );

INSERT INTO usages_actuels (
    usage_actuel_id, etat_actuel_id, usage_code, principal, cree_par
) VALUES
    (
        '31000000-0000-4000-8000-000000000005',
        '30000000-0000-4000-8000-000000000005', 'sans_usage', true, 'fixture'
    ),
    (
        '31000000-0000-4000-8000-000000000006',
        '30000000-0000-4000-8000-000000000006', 'culture_musee', true, 'fixture'
    ),
    (
        '31000000-0000-4000-8000-000000000007',
        '30000000-0000-4000-8000-000000000006', 'tourisme_visite', false, 'fixture'
    );

INSERT INTO geometries (
    geometrie_id, site_id, geom, type_geometrie_code,
    precision_geographique_code, methode_localisation_code,
    crs_source, geometrie_reference, usage_code, date_verification,
    fiabilite_code, notes, cree_par
) VALUES
    (
        '60000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000004', ST_Point(470000, 6870000),
        'point_site', 'batiment_verifie', 'coordonnees_source', 'EPSG:2154', true,
        'affichage', DATE '2026-07-20', 'forte', 'Coordonnees fictives.', 'fixture'
    ),
    (
        '60000000-0000-4000-8000-000000000004',
        '10000000-0000-4000-8000-000000000005', ST_Point(480000, 6880000),
        'point_site', 'batiment_verifie', 'coordonnees_source', 'EPSG:2154', true,
        'affichage', DATE '2026-07-20', 'forte', 'Coordonnees fictives.', 'fixture'
    );

INSERT INTO mentions_sources (
    mention_id, source_id, reference_source, date_consultation,
    entite_type_code, entite_id, champ_cible, valeur_originale,
    valeur_normalisee, statut_valeur_code, nature_information_code,
    fiabilite_code, extracteur, version_extracteur, cree_par
) VALUES
    (
        '80000000-0000-4000-8000-000000000005', 'test_inventaire', 'IATEST0004',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000004', 'nom_principal',
        json_object('texte', 'Scierie Simple du Test'),
        json_object('texte', 'Scierie Simple du Test'),
        'renseignee', 'sourcee', 'forte', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000006', 'test_inventaire', 'IATEST0005',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000005', 'nom_principal',
        json_object('texte', 'Filature Reconvertie du Test'),
        json_object('texte', 'Filature Reconvertie du Test'),
        'renseignee', 'sourcee', 'forte', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000007', 'test_inventaire', 'IATEST0006',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000006', 'nom_principal',
        json_object('texte', 'Moulin des Pres'),
        json_object('texte', 'Moulin des Pres'),
        'renseignee', 'sourcee', 'moyenne', 'fixture_sql', '1.0', 'fixture'
    ),
    (
        '80000000-0000-4000-8000-000000000008', 'test_casias', 'BNOTEST0007',
        TIMESTAMPTZ '2026-07-20 12:00:00+02', 'sites',
        '10000000-0000-4000-8000-000000000007', 'nom_principal',
        json_object('texte', 'Ancien moulin des Pres'),
        json_object('texte', 'Ancien moulin des Pres'),
        'renseignee', 'sourcee', 'faible', 'fixture_sql', '1.0', 'fixture'
    );

INSERT INTO identifiants_externes (
    identifiant_externe_id, source_id, type_identifiant_code, valeur,
    entite_type_code, entite_id, principal_pour_source,
    date_verification, fiabilite_code, cree_par
) VALUES
    (
        '90000000-0000-4000-8000-000000000004', 'test_inventaire', 'IA',
        'IATEST0004', 'sites', '10000000-0000-4000-8000-000000000004',
        true, DATE '2026-07-20', 'forte', 'fixture'
    ),
    (
        '90000000-0000-4000-8000-000000000005', 'test_inventaire', 'IA',
        'IATEST0005', 'sites', '10000000-0000-4000-8000-000000000005',
        true, DATE '2026-07-20', 'forte', 'fixture'
    ),
    (
        '90000000-0000-4000-8000-000000000006', 'test_inventaire', 'IA',
        'IATEST0006', 'sites', '10000000-0000-4000-8000-000000000006',
        true, DATE '2026-07-20', 'moyenne', 'fixture'
    ),
    (
        '90000000-0000-4000-8000-000000000007', 'test_casias', 'BNO',
        'BNOTEST0007', 'sites', '10000000-0000-4000-8000-000000000007',
        true, DATE '2026-07-20', 'faible', 'fixture'
    );

INSERT INTO propositions_rapprochement (
    proposition_rapprochement_id, site_a_id, site_b_id, methode_code,
    score_similarite, criteres, statut_decision_code, fiabilite_code,
    notes, cree_par
) VALUES (
    'a0000000-0000-4000-8000-000000000001',
    '10000000-0000-4000-8000-000000000006',
    '10000000-0000-4000-8000-000000000007',
    'nom_commune_lieu_dit', 0.8200,
    json_object(
        'nom_proche', true,
        'meme_commune', true,
        'meme_lieu_dit', true,
        'identifiant_exact', false
    ),
    'a_verifier', 'faible',
    'La similarite cree une proposition, jamais une fusion automatique.',
    'fixture'
);
