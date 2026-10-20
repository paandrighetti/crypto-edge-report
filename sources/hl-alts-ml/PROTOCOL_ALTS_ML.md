# PROTOCOLE PRÉ-ENREGISTRÉ : alts en long/short, méta-labeling du manchon de tendance Hyperliquid, méta-labeling de A4_BE_V50_L1

Version 1.0, figée le 24/09/2026 avant tout calcul de rendement de stratégie sur données réelles pour ces trois arcs. Seul un contrôle de qualité des données a précédé la rédaction (couverture, volumes nuls, format et fréquence du funding, ordres de grandeur) ; ses constats sont consignés en section 1. Toute modification ultérieure est ajoutée en bas du fichier, datée et justifiée ; les tests déjà exécutés restent comptés.

## 0. Demande et lecture retenue

Message de l'utilisateur (24/09/2026, 20 h 16) : « Go pour ça : Alts en long/short, filtrage du signal par apprentissage (meta-labeling) et pour le beta classique identifié comme le meilleur par l'analyse dans ce cas ».

Lecture retenue, en trois arcs indépendants :

- **Arc A.** Exécuter tel quel le test pré-enregistré `xs_ls` (long/short cross-sectionnel dollar-neutre sur les perpétuels Hyperliquid, 17/09/2026), jamais lancé sur le cache complet.
- **Arc B.** Méta-labeling du manchon de tendance canonique sur l'univers point-in-time des perpétuels Hyperliquid. C'est l'arc « meta_label » décrit le 17/09/2026, dont le package n'existe plus sur le disque de l'utilisateur ; il est reconstruit ici avec un protocole nouveau.
- **Arc C.** Méta-labeling de la stratégie retenue par l'étude d'allocation, A4_BE_V50_L1 (tendance BTC + ETH au comptant, cible de volatilité 50 %, exposition ≤ 100 %).

Ce qu'une conclusion positive déclenche :

- arcs A et B : passage en G1 (portefeuille fictif suivi en temps réel), sans capital, conformément à la discipline G0 → G1 → G2 du programme ;
- arc C : une re-simulation dans le cadre de l'étude d'allocation (C.8, critère C5). L'allocation retenue ne change que si C5 est passé.

## 1. Données

### 1.1 Hyperliquid

- **Source.** Cache local de l'utilisateur `hl_cache` (récupéré le 16/09/2026) :
  - 234 perpétuels, dont 56 délistés ;
  - 232 ont au moins 30 clôtures ;
  - bougies journalières depuis le 01/01/2023 ;
  - funding depuis le 12/05/2023.
- **Panneau compact.** `data/raw/hyperliquid_panel/hl_daily.parquet`, construit par `scripts/build_hl_panel.py`, avec l'empreinte sha256 de chaque fichier source dans `hl_cache_manifest.json`. La bougie du jour de collecte, incomplète, est retirée ; le panneau s'arrête au 15/09/2026.
- **Identité avec le chargeur enregistré.** `build_hl_panel.py --check` vérifie que les panneaux close, volume en dollars et funding sont identiques, à l'élément près, à ceux de `xs_ls.data.load_hl_cache` sur le cache brut.

### 1.2 Défaut constaté : bougies sans transaction avant l'ouverture du marché

Hyperliquid renvoie des bougies avec volume nul et zéro transaction avant la première transaction d'un marché :

- 124 coins sur 234 sont concernés, pour 22 800 jours-coin au total ;
- jusqu'à 999 jours par coin, pour AXS, DASH, ICP, XMR et ZEC (premières transactions entre octobre 2025 et janvier 2026) ;
- les prix de ces bougies bougent (variation absolue moyenne de 2 à 4 % par jour), mais rien n'y est négociable sur la plateforme.

Effet sur la règle d'univers enregistrée de `xs_ls` (top N par médiane du volume en dollars, 90 jours d'historique) : des coins sans aucun volume entrent dans l'univers dès que moins de N coins se négocient. Cela représente 1 784, 5 366 et 9 978 jours-coin d'univers sans volume pour N = 30, 50 et 80. L'historique sans transaction compte aussi dans les 90 jours requis.

**Correction « négociable ».** Clôture, extrêmes, volume et funding sont mis à manquant avant le premier jour de volume positif de chaque coin. Après correction, l'univers top 50 est complet à partir du 01/01/2024 (au lieu du 01/04/2023) et ne contient plus aucun jour-coin sans volume.

### 1.3 Vérification des trois hypothèses du README de `xs_ls`

1. **Horodatage.** Les bougies sont indexées par l'heure d'ouverture (00 h 00 UTC) : l'ouverture du jour d égale la clôture du jour d − 1 (BTC : 16 610,3 puis 16 610,4). Vérifiée.
2. **Unité du volume.** Le volume est en unités de base : BTC 72 423 BTC le 15/09/2026, soit environ 5,5 milliards de dollars. Vérifiée.
3. **Funding.** Taux par intervalle, sous forme de fraction. Le cache stocke une colonne unique nommée d'après le coin, pas `fundingRate`, et le chargeur enregistré échoue sur ce format. L'intervalle est de 8 h jusqu'au 07/06/2023, horaire ensuite. La somme journalière donne, pour BTC, un funding annualisé de 13,5 % en 2023, 24,1 % en 2024, 10,6 % en 2025 et 4,8 % en 2026. Ordre de grandeur vérifié.
4. **Continuité.** Aucune date manquante à l'intérieur de la vie d'un coin.

### 1.4 BTC et ETH en euros (arc C)

- **Source.** Panneau de l'étude d'allocation (`alloc.data.load_panel`) : Coin Metrics, taux de change et de trésorerie de la Banque centrale européenne.
- **Période de décision.** Exploration 01/01/2016 → 31/12/2024.
- **Période descriptive.** La période 01/01/2025 → 23/09/2026 a déjà été ouverte une fois pour la décision d'allocation : elle est contaminée. Elle est publiée à titre descriptif et ne sert à aucune décision.

## Partie A : `xs_ls`, long/short cross-sectionnel dollar-neutre

### A.1 Ce qui est enregistré et inchangé

Le README et la configuration de `xs_ls` (17/09/2026) sont recopiés à l'identique dans `vendor/xs_ls/`, avec leurs sha256 dans `vendor/README.md`. Sont conservés tels quels :

- la grille de 54 cellules : 9 signaux, top 30/50/80, pondération par quintiles ou par rangs ;
- les coûts de 6, 15 et 25 points de base, avec 15 en référence ;
- les niveaux de levier brut 1 et 2,5 ;
- le Sharpe déflaté avec 54 essais ;
- le benchmark de 200 signaux aléatoires persistants (processus autorégressif d'ordre 1, φ = 0,9) ;
- le diagnostic sur la fenêtre du tweet (08/07/2026 → 10/09/2026) ;
- la règle de décision : Sharpe net ≥ 1,0 à 15 points de base, Sharpe déflaté P(SR > 0) ≥ 0,95, au moins 3 années positives sur 4, |bêta BTC| < 0,2.

### A.2 Écarts déclarés avant le run

1. **Adaptateur de lecture du funding.** Le chargeur accepte une colonne unique dont le nom est celui du coin. Il n'y a aucune autre modification du code. Le panneau compact est lu par `metalabel.hl.xs_panels`, identique au chargeur enregistré (1.1).
2. **Deux versions des données.**
   - Version « enregistrée » : toutes les bougies du cache.
   - Version « négociable » : correction 1.2. C'est la version principale, car elle correspond à l'intention du README (univers point-in-time négociable).
   - Le verdict CONSERVER exige que les deux versions concluent CONSERVER. Sinon, REJET.
3. **Lancement.** `scripts/run_xs_ls.py` appelle `xs_ls.run.run_grid` puis `xs_ls.run.report` avec `Config()` inchangée, sur le même principe que `python -m xs_ls.run`.

### A.3 Robustesse prévue par le README (non décisionnelle)

Rebalancement tous les 3 jours sur la version négociable, avec la commande du README.

### A.4 Conséquence

- CONSERVER : passage en G1, sans capital.
- REJET : l'arc est clos. Les 54 cellules sont comptées comme essais (section D).

## Partie B : méta-labeling du manchon de tendance Hyperliquid

### B.1 Signal primaire et stratégie de référence

**Signal primaire.** `trend_backtest.signal_z` avec les paramètres de `trend_backtest.Config` : horizons 30 et 90 jours, volatilité 30 jours, borne 3. Le côté est le signe de z.

**Manchon brut R0.** C'est `trend_backtest.run_pipeline` avec `Config()` et `CostModel()` inchangés :

- univers éligible par liquidité en dollars, avec hystérésis (entrée au 70e centile, sortie au 50e), 120 jours d'historique, révision tous les 30 jours ;
- 12 noms retenus par |conviction / volatilité|, conviction tanh(z), plafond de 15 % par nom ;
- cible de volatilité de 25 % × demi-Kelly, levier brut plafonné à 1, bande de non-transaction de 5 % ;
- coûts de 5,5 points de base par unité de rotation, funding payé ou reçu.

**Données.** Version négociable, du 01/01/2023 au 10/09/2026.

### B.2 Échantillon

Jours-coin du masque d'éligibilité du manchon, avec z défini et non nul.

### B.3 Étiquette

- **Horizons.** h ∈ {1, 3, 7} jours, h = 7 en principal.
- **Convention temporelle.** Celle du manchon : poids fixé à la clôture d, rendement des jours d + 1 à d + h.
- **Étiquette nette.** y = 1 si côté × (Π(1 + r) − 1 − ΣF) > 0, où F est le funding journalier (positif : les longs paient).
- **Étiquette prix seul (ablation).** y = 1 si côté × Σ log(1 + r) > 0.
- **Coins délistés.** Les rendements postérieurs à la dernière clôture d'un coin délisté valent zéro (position close au dernier prix), comme dans le manchon. Aucun jour-coin n'est retiré pour cause de délistage.

### B.4 Variables

15 variables par coin, toutes calculées avec des données datées au plus tard de d. Les 4 variables de marché du premier jet (z de BTC, largeur, dispersion, volatilité de marché) ont été retirées après la calibration synthétique (B.11).

| Variable | Définition |
|---|---|
| \|z\| | valeur absolue du signal primaire |
| côté | signe de z |
| côté × rendement logarithmique | sur 1, 7 et 30 jours |
| log de la volatilité 30 jours | |
| log du rapport de volatilité | 7 jours / 30 jours |
| amplitude moyenne sur 7 jours | log(haut / bas), divisée par la volatilité 30 jours |
| log du volume médian en dollars | sur 30 jours |
| log de l'accélération du volume | moyenne 7 jours / médiane 30 jours |
| côté × funding moyen 7 jours | coût du côté |
| côté × (funding 7 jours − funding 30 jours) | |
| log de l'âge | jours depuis la première transaction |
| bêta glissant 90 jours contre BTC | |
| distance à l'extrême 60 jours | dans le sens du côté (≤ 0) |

### B.5 Modèles

Hyperparamètres fixés sur données synthétiques seulement (B.11), sans aucun réglage sur données réelles.

- **Base.** Régression logistique (C = 1) sur (|z|, côté, |z| × côté) : ce que z seul dit de la probabilité de succès.
- **Méta principal.** Arbres de gradient `HistGradientBoostingClassifier` (scikit-learn) sur les 15 variables :
  - profondeur maximale 3, taux d'apprentissage 0,02, 150 itérations ;
  - au moins 1 000 observations par feuille, pénalité L2 = 1,0 ;
  - sans arrêt anticipé, graine 0.
- **Méta secondaire.** Régression logistique pénalisée (L2, C = 0,01) sur les 15 variables :
  - variables standardisées avec la moyenne et l'écart-type de l'échantillon d'entraînement, puis bornées à ±5 ;
  - valeurs manquantes remplacées par la médiane d'entraînement.

### B.6 Validation hors échantillon

- **Découpage.** Walk-forward mensuel, fenêtre d'entraînement croissante.
- **Purge.** Pour un bloc commençant au jour s, l'entraînement n'utilise que les observations dont l'étiquette est entièrement connue la veille : d + h ≤ s − 1 (López de Prado 2018, chapitre 7).
- **Bornes.** Premier bloc testé : 01/10/2024, avec environ 10 mois d'entraînement depuis la constitution de l'univers négociable fin novembre 2023. Le dernier bloc s'arrête à la dernière décision dont l'étiquette est complète au 10/09/2026.

### B.7 Dimensionnement méta

- **Taille de pari.** m(p) = max(0 ; 2 Φ((p − 0,5) / √(p (1 − p))) − 1), où p est la probabilité hors échantillon (López de Prado 2018, section 10.3).
- **Manchon méta M1.** Même pipeline que R0, avec la conviction tanh(z) × m(p). On a m = 1 avant la première prédiction, donc R0 et M1 sont identiques avant le 01/10/2024.

### B.8 Statistiques

**Perte logarithmique (log-loss).**

- Le jour d, on calcule ΔLL_d, la moyenne sur les coins de la perte du modèle de base moins celle du méta. Une valeur positive signifie que le méta est meilleur.
- Test : bootstrap stationnaire sur les jours (Politis et Romano 1994), bloc moyen de 30 jours, 2 000 tirages, graine 20260924.
- p unilatéral = (1 + #{moyenne* − moyenne ≥ moyenne}) / 2 001. Le t de Newey-West est publié.

**AUC.** Aire sous la courbe ROC du méta, avec intervalle à 95 % par bootstrap de blocs de jours (1 000 tirages).

**Écart de Sharpe.**

- ΔSR = Sharpe net annualisé (base 365) de M1 moins celui de R0, sur les jours hors échantillon.
- Test : bootstrap stationnaire apparié (bloc 30, 2 000 tirages), p unilatéral centré. C'est le principe de Ledoit et Wolf (2008), en version non studentisée.

**Sharpe probabiliste.** PSR de M1 hors échantillon, P(SR > 0) (Bailey et López de Prado 2012).

### B.9 Règle de décision

Configuration principale : arbres de gradient, h = 7, étiquette nette. CONSERVER (passage en G1) si et seulement si les cinq conditions sont réunies :

| Code | Condition |
|---|---|
| B1 | ΔLL moyen > 0 avec p < 0,05 |
| B2 | borne basse de l'intervalle à 95 % de l'AUC du méta > 0,50 |
| B3 | ΔSR > 0 avec p < 0,05 |
| B4 | ΔLL moyen > 0 dans au moins 2 des 3 tiers chronologiques de la période hors échantillon |
| B5 | PSR(M1) ≥ 0,95 |

Sinon, REJET.

Les 11 autres configurations (2 modèles × 3 horizons × 2 étiquettes, moins la principale) sont publiées. Elles ne sont pas décisionnelles et sont comptées comme essais.

### B.10 Contrôles synthétiques, exécutés avant le run réel

Générateur de `metalabel/synthetic.py` : 170 coins, dont BTC, soit environ 50 coins éligibles par jour comme sur les données réelles, sur le même calendrier. Chocs de Student à 5 degrés, facteur de marché, dérive nulle, funding indépendant des rendements, listages et délistages échelonnés.

- **Contrôle négatif.** Aucune prévisibilité (κ = 0). 20 graines ; B1 doit échouer dans au moins 17.
- **Contrôle positif.** Effet planté : la tendance 30 jours se prolonge de κ σ par jour quand la volatilité 7 jours est sous la volatilité 30 jours, et s'inverse de κ σ sinon. Avec κ = 0,20, l'écart de taux de réussite entre les deux états vaut 11 à 14 points. 10 graines ; B1 doit passer dans au moins 8.
- **Puissance à κ = 0,10** (écart de 5 à 9 points) : publiée, sans critère.

Si un contrôle échoue, le run réel n'est pas interprété. Le code est corrigé et une modification datée est ajoutée ici avant tout nouveau run.

### B.11 Calibration synthétique préalable et effet minimal détectable

Le premier jet de ce protocole n'a jamais été exécuté sur données réelles. Il prévoyait des arbres plus agressifs (taux 0,05, 300 itérations, feuilles ≥ 500), 19 variables dont 4 de marché, et un contrôle positif à κ = 0,05. Sur données synthétiques, ce jet :

- dégradait la perte logarithmique hors échantillon, même avec un effet planté fort (κ = 0,20 : ΔLL de −0,018 à +0,000, p ≥ 0,47) ;
- ne détectait pas κ = 0,05, qui correspond à un écart de 2 à 6 points seulement.

Cause identifiée : les étiquettes sont dominées par le facteur de marché, commun à tous les coins d'un même jour. Les variables de marché apprennent alors quelques épisodes de marché et sur-ajustent.

Calibration menée (scripts et journaux dans `scripts/calibration/`) :

- 3 graines par niveau d'effet (κ = 0 ; 0,05 ; 0,10 ; 0,20) ;
- 4 à 5 variantes de modèles ;
- univers synthétique de la taille de l'univers réel au second tour.

Choix retenu :

- variables par coin seules ;
- arbres régularisés : taux 0,02, 150 itérations, feuilles ≥ 1 000 ;
- logistique secondaire à C = 0,01.

Sous l'hypothèse nulle, aucune variante ne produit de faux positif (p ≥ 0,16). À κ = 0,20, les arbres retenus détectent l'effet dans 3 graines sur 3 (p = 0,002). À κ = 0,10, ils le détectent dans 0 graine sur 3 à 5 %.

**Effet minimal détectable annoncé avant le run.** Avec 23 mois hors échantillon, seul un effet conditionnel de l'ordre de 10 points ou plus de taux de réussite est détectable. Un REJET sur données réelles exclut un tel effet, pas un effet de quelques points.

## Partie C : méta-labeling de A4_BE_V50_L1

### C.1 Stratégie primaire

Poids de A4_BE_V50_L1 calculés par `alloc.strategies._a4_weights`, avec le moteur `alloc.engine.simulate` et les coûts de l'étude :

- décision à la clôture t, exécution à t + 1 ;
- bande de 5 % ;
- frais au comptant, trésorerie au fonds monétaire.

### C.2 Échantillon

Couples (actif, jour) avec un poids A4 strictement positif, du 01/05/2016 au 31/12/2024.

### C.3 Étiquette

- **Horizons.** h = 7 en principal, h = 14 en secondaire.
- **Définition.** y = 1 si Σ log(1 + r) − Σ trésorerie > 0 sur les jours d + 2 à d + h + 1, fenêtre qui suit l'exécution décalée.

### C.4 Variables

9 variables :

- cadran de l'actif ;
- tanh(z 15 jours) − tanh(z 60 jours) ;
- log(volatilité 20 jours / volatilité 60 jours) ;
- rendements logarithmiques sur 1 et 7 jours ;
- distance au plus haut 60 jours ;
- funding BTC moyen sur 7 jours ;
- cadran de l'autre actif ;
- indicatrice ETH.

### C.5 Modèles

Hyperparamètres fixés sur données synthétiques seulement (C.11).

- **Base.** Logistique (C = 1) sur (cadran, indicatrice ETH).
- **Principal.** Logistique L2, C = 0,01, avec la même standardisation que B.5.
- **Secondaire.** Arbres de gradient : profondeur 2, au moins 200 observations par feuille, 100 itérations, taux 0,02, graine 0.

### C.6 Validation

Walk-forward annuel à fenêtre croissante, avec la purge de B.6. Années testées : 2018 à 2024, soit 7 années hors échantillon.

### C.7 Règle d'application

- **Principale.** Filtre : poids A4 × 1{p ≥ 0,5}, sans remise à l'échelle.
- **Secondaire.** Poids A4 × m(p).
- **Avant 2018.** Aucune prédiction, donc la stratégie méta égale A4.

### C.8 Règle de décision

Configuration principale : logistique, h = 7, filtre. Les écarts portent sur la période 01/01/2018 → 31/12/2024.

| Code | Condition |
|---|---|
| C1 | ΔLL moyen > 0 avec p < 0,05 (test de B.8) |
| C2 | Δg > 0 avec un t de Newey-West ≥ 2,0, où Δg est l'écart annualisé de rendement logarithmique quotidien moyen, méta moins A4, net de tous les coûts |
| C3 | Δg > 0 dans au moins 5 des 7 années |
| C4 | le drawdown maximal du méta n'est pas plus mauvais que celui de A4 de plus de 5 points |
| C5 | seulement si C1 à C4 passent : modèle figé sur 2016-2024, re-simulation en régime SD2, horizon 4 ans, 10 000 trajectoires et mêmes graines que l'étude ; la médiane de W_T doit augmenter et P(W_T < 0,4 W0) rester ≤ 5 % |

- Seul C5 passé modifie l'allocation.
- Sinon, l'allocation retenue est inchangée.
- Les 4 autres configurations sont publiées, non décisionnelles et comptées comme essais :
  - logistique h = 14 ;
  - arbres h = 7 ;
  - arbres h = 14 ;
  - logistique h = 7 avec m(p).

### C.9 Période contaminée

Le modèle entraîné sur 2016-2024 est appliqué à la période 01/01/2025 → 23/09/2026. Ce résultat est publié à titre descriptif seulement.

### C.10 Contrôles synthétiques

Même générateur que B.10, sur le calendrier de l'exploration :

- deux actifs de volatilités 3,5 % et 4,5 % par jour, de corrélation 0,7 ;
- trésorerie et funding nuls ;
- état planté mesuré sur les volatilités 20 et 60 jours, les fenêtres de la variable de l'arc.

Critères :

- **Contrôle négatif.** 20 graines ; C1 doit échouer dans au moins 17.
- **Contrôle positif.** κ = 0,30, soit un écart de 20 à 29 points entre états. 10 graines ; C1 doit passer dans au moins 8.
- **Puissance à κ = 0,20** (écart de 11 à 20 points) : publiée, sans critère.

### C.11 Calibration synthétique préalable et effet minimal détectable

Le premier jet (logistique C = 0,1, arbres profondeur 2 avec 200 itérations au taux 0,05, contrôle positif à κ = 0,10) n'a jamais été exécuté sur données réelles. Il présentait deux défauts :

- l'état planté (volatilités 7 et 30 jours) ne correspondait à aucune variable de l'arc, dont le rapport de volatilité porte sur 20 et 60 jours. Le contrôle ne mesurait donc rien ;
- une fois l'état aligné, les arbres du premier jet ne détectaient l'effet à aucun niveau (p ≥ 0,27 même à κ = 0,30).

Résultats de la calibration, sur 4 graines par niveau :

| Niveau d'effet | Arbres retenus | Logistique C = 0,01 |
|---|---|---|
| κ = 0,30 | 4 détections sur 4 | 4 détections sur 4 |
| κ = 0,20 | 2 détections sur 4 | 2 détections sur 4 |
| κ = 0,10 | aucune détection | aucune détection |
| κ = 0 (nulle) | aucun faux positif | aucun faux positif |

La logistique, plus simple et plus stable, est retenue en principal.

**Effet minimal détectable annoncé avant le run.** Sept années hors échantillon sur deux actifs corrélés à 0,7 équivalent à quelques centaines d'épisodes indépendants de 7 jours. Seul un effet conditionnel de l'ordre de 20 points de taux de réussite est détectable avec une puissance d'environ 80 %. Un REJET n'exclut pas un effet plus petit. Il signifie qu'aucun filtre appris ne peut être validé sur cet échantillon et qu'en déployer un reviendrait à le faire sans preuve.

## D. Comptage des essais

Registre séparé `results/trials_alts_ml.csv`. Le registre de l'étude d'allocation n'est pas modifié, pour que ses fichiers de décision restent reproductibles à l'identique.

| Arc | Essais |
|---|---|
| A | 54 cellules |
| B | 12 configurations |
| C | 5 configurations |

Le total du programme est publié dans le rapport : 339 essais pour l'étude d'allocation, plus ceux de ce protocole.

## E. Livrables générés par le code

- `results/xs_ls/{tradeable,registered,tradeable_rb3}/` : grille et résumé de `xs_ls` ;
- `results/metalabel/` : prédictions hors échantillon, tests, contrôles ;
- `reports/ALTS_ML.md` : rapport généré par `scripts/make_alts_report.py`.

## F. Références

- Bailey, D. H. et López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk* 15(2).
- Bailey, D. H. et López de Prado, M. (2014). The deflated Sharpe ratio. *Journal of Portfolio Management* 40(5).
- Joubert, J. F. (2022). Meta-labeling: theory and framework. *Journal of Financial Data Science* 4(3).
- Ledoit, O. et Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. *Journal of Empirical Finance* 15, 850-859.
- Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal* 58(4).
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. Chapitres 3 (méta-labeling), 7 (validation croisée purgée) et 10 (taille des paris).
- Moskowitz, T., Ooi, Y. H. et Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics* 104(2).
- Newey, W. et West, K. (1987, 1994). Estimateurs de covariance robustes à l'autocorrélation et choix automatique du nombre de retards.
- Politis, D. et Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association* 89(428).

## G. Journal des modifications

### Modification 1 (24/09/2026, après les runs réels et une revue indépendante) : précisions, sans effet sur les verdicts

Une revue par un agent qui n'avait pas vu le travail a vérifié le code, les données et le rapport. Elle a reproduit les trois verdicts à l'identique et n'a trouvé aucune erreur critique. Les points suivants sont déclarés.

1. **Fin de la période contaminée (C.9).** Le premier run descriptif s'arrêtait à la dernière ligne Yahoo, celle du 24/09/2026, qui était incomplète. Il a été corrigé pour s'arrêter au 23/09/2026, date de fin du run d'ouverture de l'étude d'allocation et date écrite en C.9 (commit `5131a57`).
2. **Taille minimale d'entraînement, non écrite dans la version 1.0.** Elle vaut 1 000 lignes pour l'arc B et 300 pour l'arc C. Elle n'a jamais joué : les premiers échantillons d'entraînement comptent 11 150 et 916 lignes.
3. **Arc B, fin de période.**
   - Les tests de classification (B1, B2, B4) portent sur les décisions étiquetées jusqu'au 03/09/2026, comme l'écrit B.6.
   - Le manchon méta M1 utilise aussi les prédictions du 04 au 10/09/2026. Une prédiction n'a pas besoin d'étiquette, et sans elles M1 redeviendrait R0 sur les 7 derniers jours.
   - Avec la fenêtre de B3 coupée au 04/09/2026, l'écart de Sharpe vaut −0,152 (p = 0,60) au lieu de −0,129 (p = 0,59).
4. **Arc B, durée d'entraînement.** B.6 annonçait environ 10 mois. L'échantillon éligible commence le 30/07/2023, avec moins de 12 noms jusqu'au 27/11/2023 : le premier entraînement couvre donc environ 14 mois.
5. **Diagnostic ajouté hors protocole, après les verdicts.** Rotation et Sharpe brut du benchmark aléatoire enregistré de `xs_ls`, par `scripts/run_xs_ls.py diag`. Ce n'est pas un test.
6. **Rapport corrigé après la revue.**
   - Le carry perd par les coûts, pas faute de funding.
   - L'affirmation sur la fenêtre du tweet dépend du niveau de coût et de l'univers.
   - La puissance est détaillée test par test.
   - La variante `size` est évaluée sur le critère enregistré.
   - L'horodatage du funding décalait 8 heures sur 24 avant le 08/06/2023.
   - Deux remarques de conception sont publiées dans les limites : B2 compare l'AUC à 0,5 et non à z seul ; les bootstraps sont un peu libéraux (6 à 8 % à 5 % nominal).
