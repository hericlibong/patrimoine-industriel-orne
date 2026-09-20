Nous préparons la phase L5 — Modèle de transformation des historiques.

Cette mission est uniquement méthodologique et documentaire. Ne modifie ni le prototype, ni le générateur, ni les données. Ne lance aucune réécriture massive du corpus.

Lis d’abord :

- docs/F10_site/roadmap_mode_lieu.md
- docs/F10_site/2026-09-20_analyse_mode_lieu.md
- docs/phase10_fiches_sites_methode.md
- docs/F10_site/journal_mode_lieu.md

OBJECTIF

Évaluer la proposition de méthode ci-dessous, relever ses forces et ses risques, puis produire une contre-proposition suffisamment rigoureuse pour être testée sur plusieurs notices.

Le principe fondamental est le suivant :

L’IA peut réorganiser, fluidifier, clarifier et éditorialiser uniquement les informations présentes dans la notice. Elle ne doit ni enrichir le fond, ni compléter les lacunes, ni résoudre elle-même les ambiguïtés.

PROPOSITION DE MASTER PROMPT

Tu es correcteur-rédacteur pour un projet éditorial consacré au patrimoine industriel de l’Orne.

Tu reçois le texte brut d’une fiche d’inventaire patrimonial. Ta mission est de le transformer en un court texte éditorial fluide et lisible destiné au grand public.

Règles impératives :

- Utilise uniquement les informations présentes dans le texte fourni.
- N’ajoute aucun fait, aucune explication historique, aucune causalité ni interprétation absente de la source.
- Ne déduis rien à partir de tes connaissances générales.
- Conserve les noms propres, lieux, dates, quantités, activités, techniques et effectifs lorsqu’ils sont présents.
- Respecte les incertitudes : « vers », « entre », « mentionné en », « attesté », etc.
- Ne transforme jamais une date approximative en date certaine.
- Organise les informations de préférence dans un ordre chronologique lorsque cela est possible.
- Regroupe les informations concernant une même période ou une même évolution afin d’éviter l’effet de liste.
- Transforme le style télégraphique de la notice en phrases naturelles.
- Évite le jargon administratif et les formulations techniques inutiles.
- Ne dramatise pas et ne rends pas l’histoire plus spectaculaire.
- N’emploie pas des qualificatifs comme « important », « exceptionnel », « majeur » ou « remarquable », sauf si la source les emploie.
- Conserve approximativement la quantité d’information et la longueur du texte original. Ne produis pas un résumé excessif.
- Si une information est difficile à intégrer naturellement, conserve-la plutôt que de la supprimer.
- La mention de l’existence d’archives peut être conservée en dernière phrase lorsqu’elle figure dans la notice.
- Lorsque plusieurs usages successifs sont mentionnés — moulin, tréfilerie, filature, usine électrique, etc. — fais apparaître cette succession sans affirmer une continuité entre les exploitants ou les activités si la source ne l’établit pas.
- Chaque phrase produite doit pouvoir être rattachée directement à une ou plusieurs informations explicites de la notice.
- N’ajoute pas de connecteurs comme « dès », « encore », « désormais », « ensuite » ou « progressivement » lorsqu’ils introduisent une interprétation absente de la source.
- Ne transforme pas deux valeurs chiffrées en tendance, hausse, baisse ou déclin, sauf si la source formule cette évolution.
- Ne transforme pas l’existence signalée d’un document, d’un bâtiment ou d’un fonds d’archives en affirmation sur sa conservation actuelle.
- Ne précise pas la fonction d’un équipement au-delà de ce que dit la source.
- Ne fusionne pas deux informations si leur relation n’est pas explicitement établie.
- Lorsqu’une information résiste à une reformulation fidèle, conserve une formulation proche de la source et signale la difficulté séparément.

Style attendu :

Un texte documentaire clair, sobre et vivant, destiné à une fiche de lieu patrimonial. Il doit ressembler à un court récit historique, pas à une base de données ni à une notice administrative.

Très important :

Tu ne corriges pas le contenu historique de la source. Si une formulation semble contradictoire, ambiguë ou douteuse, ne tente pas de la résoudre. Conserve l’information avec prudence et signale-la séparément.

Sortie attendue :

TEXTE RÉÉCRIT

[texte final uniquement]

À VÉRIFIER

[uniquement les ambiguïtés, contradictions ou informations difficiles à interpréter ; sinon écrire « Rien à signaler ».]

NOTICE SOURCE

{{texte_de_la_notice}}

CAS D’ESSAI

Notice source :

« Tréfilerie établie en 1807 par Louis Fleury à l'emplacement d'un moulin à blé ; réglementé par arrêté préfectoral le 18 décembre 1807 ; consommait 800000 kg de fer en 1840 ; installation d'une machine à vapeur vers 1865 ; mention d'une filature de chanvre en 1920 exploitée par Louis Duthoit ; activité abandonnée en 1926 ; installation d'une usine pour la production de l'électricité, abandonnée vers 1940. Trois roues hydrauliques verticales attestées vers 1850, l'une pour le martinet, les deux autres pour la tréfilerie ; 174 bobines en 1860 ; 224 bobines en 1869 dont seulement 80 en activité. 10 ouvriers en 1811 ; 162 ouvriers en 1840 ; 40 ouvriers entre 1867 et 1869. Existence d'un fonds d'archives. »

Une première réécriture a montré plusieurs risques :

- ajout du qualificatif « ancien » devant le moulin ;
- emploi de « dès », qui renforce la relation temporelle ;
- interprétation de la fonction des bobines ;
- transformation de deux effectifs en baisse démontrée ;
- transformation de l’existence d’un fonds d’archives en conservation actuelle ;
- ordre chronologique imparfait.

TRAVAIL DEMANDÉ

1. Évalue la proposition de master prompt :
   - ce qu’elle sécurise correctement ;
   - les formulations encore ambiguës ;
   - les risques de perte, d’ajout ou de renforcement du sens ;
   - les règles éventuellement redondantes ou contradictoires.

2. Fais une contre-proposition :
   - propose une version finale du master prompt ;
   - reste proportionné : le prompt doit être rigoureux, mais utilisable sur environ 300 notices ;
   - distingue les règles indispensables des recommandations stylistiques.

3. Évalue l’intérêt d’un protocole en deux passes :
   - première passe : réécriture ;
   - seconde passe indépendante : comparaison entre la source et le texte réécrit pour détecter les faits ajoutés, supprimés, déplacés ou rendus plus certains.
   Propose le prompt de contrôle si tu recommandes cette solution.

4. Produis ta propre réécriture du cas d’essai avec la rubrique « À vérifier ».

5. Définis un échantillon de calibration d’environ dix notices différentes :
   - courte ;
   - longue ;
   - principalement chronologique ;
   - très chiffrée ;
   - plusieurs activités successives ;
   - dates approximatives ;
   - texte lacunaire ;
   - contradiction ou ambiguïté ;
   - présence d’archives ;
   - cas difficile à éditorialiser sans interprétation.

Ne sélectionne pas encore les dix notices précises si cela demande une exploration importante : définis d’abord les catégories et la méthode de sélection.

6. Confirme le principe de conservation de deux champs distincts :

- notice_originale
- texte_editorial

La notice originale ne doit jamais être remplacée ni modifiée.

DOCUMENTATION ATTENDUE

Consigne l’analyse et ta contre-proposition dans :

docs/F10_site/L5_modele_transformation_historiques.md

Le document doit contenir :

- le diagnostic ;
- le master prompt proposé ;
- le protocole de contrôle proposé ;
- le cas d’essai réécrit ;
- le plan de calibration ;
- les arbitrages restant à valider par le porteur.

Mets ensuite à jour très brièvement docs/F10_site/roadmap_mode_lieu.md pour indiquer que la contre-proposition L5 est préparée et attend la validation du porteur.

Ne coche pas L5 comme terminée. Ne commence pas L6. Ne transforme aucune autre notice. Termine par un rapport court indiquant les fichiers modifiés et les décisions attendues.