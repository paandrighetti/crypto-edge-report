# Alts en long/short et méta-labeling : rapport

Rapport généré le 24/09/2026 par `research/scripts/make_alts_report.py`, à partir de `research/results/xs_ls/` et `research/results/metalabel/`.

Protocole : `research/PROTOCOL_ALTS_ML.md`, version 1.0. Il a été commité avant tout run sur données réelles (commit `1f832b2`). Les contrôles synthétiques ont été exécutés et commités avant les runs réels des arcs B et C (commit `49ad94f`).

La demande du 24/09/2026 a été lue en trois arcs :

- **A.** Alts en long/short.
- **B.** Filtrage par apprentissage (méta-labeling) du signal de tendance sur Hyperliquid.
- **C.** Le même filtrage appliqué à la stratégie retenue par l'étude d'allocation, A4_BE_V50_L1.

| Terme | Signification |
|---|---|
| Sharpe | rendement moyen divisé par l'écart-type, annualisé en base 365 jours |
| Sharpe déflaté | probabilité que le vrai Sharpe dépasse le maximum attendu par hasard sur N essais (Bailey et López de Prado 2014) |
| PSR | Sharpe probabiliste : P(vrai Sharpe > 0) (Bailey et López de Prado 2012) |
| pb | point de base, 0,01 % |
| G | levier brut, somme des valeurs absolues des positions rapportée aux fonds propres |
| perte log. | perte logarithmique moyenne des probabilités prédites (log-loss). ΔLL = perte du modèle de base moins perte du méta-modèle : positive si le méta-modèle prédit mieux |
| AUC | aire sous la courbe ROC : 0,5 = pas mieux que le hasard, 1 = classement parfait |
| h | horizon de l'étiquette, en jours |
| t NW | statistique t avec erreurs types de Newey-West, robustes à l'autocorrélation |
| κ | intensité de l'effet planté dans les données synthétiques, en fraction de la volatilité quotidienne |
| G0, G1 | étapes du programme : recherche, puis portefeuille fictif suivi en temps réel |

## Verdicts

| Arc | Question | Verdict | Chiffres clés |
|---|---|---|---|
| A | Long/short dollar-neutre sur les perpétuels Hyperliquid, 54 cellules | REJET | meilleure cellule mom14/50/quintile : Sharpe net 0,24 à 15 pb, déflaté 0,032, 2/4 années positives |
| B | Méta-labeling du manchon de tendance Hyperliquid | REJET | ΔLL −0,0064 (p = 0,94) ; AUC 0,534 contre 0,558 pour z seul ; Sharpe du manchon 0,69 contre 0,82 sans filtre |
| C | Méta-labeling de A4_BE_V50_L1 | REJET | ΔLL −0,0042 (p = 0,79) ; croissance log. +2,0 %/an (t NW = 0,38) ; 4 années sur 7 |

**Conséquence.**

- L'allocation retenue par l'étude, A4_BE_V50_L1, ne change pas.
- Aucun des trois arcs ne passe en G1.
- Les trois arcs sont clos sur ces données.

## 1. Données Hyperliquid : un défaut du cache, corrigé avant le run

Le cache `hl_cache` compte 234 perpétuels, dont 232 avec au moins 30 clôtures. Il contient des bougies à volume nul et sans transaction avant l'ouverture de chaque marché :

- 22 800 jours-coin répartis sur 124 coins ;
- jusqu'à 999 jours pour AXS, DASH, ICP, XMR et ZEC ;
- des prix qui bougent, mais qui ne sont pas négociables.

La règle d'univers de `xs_ls` les classait dans le top N dès que moins de N coins se négociaient. Cela représente 1 784, 5 366 et 9 978 jours-coin d'univers sans volume pour N = 30, 50 et 80.

**Deux versions ont été lancées :**

- « négociable » (principale) : les données sont masquées avant la première transaction de chaque coin ;
- « enregistrée » : toutes les bougies, telles que le chargeur d'origine les lit.

Les trois hypothèses du README de `xs_ls` sont vérifiées :

- horodatage à l'ouverture ;
- volume en unités de base ;
- funding en fraction par intervalle, de 8 h jusqu'au 07/06/2023 puis horaire.

Pour ce dernier point, la jambe funding des cellules carry7 vaut de 13 % à 23 % par an, un ordre de grandeur plausible et non des centaines de pourcents. La seule adaptation du code est la lecture du funding : une colonne unique nommée d'après le coin.

## 2. Arc A : long/short cross-sectionnel (`xs_ls`, pré-enregistré le 17/09/2026)

Règle : Sharpe net ≥ 1,0 à 15 pb, Sharpe déflaté ≥ 0,95, au moins 3 années positives sur 4, |bêta BTC| < 0,2, appliquée à la meilleure cellule.

| Version | Meilleure cellule | Sharpe net 15 pb | Sharpe déflaté | Années positives | Bêta BTC | Verdict |
|---|---|---|---|---|---|---|
| négociable (principale) | mom14/50/quintile | 0,24 | 0,032 | 2/4 | −0,066 | REJET |
| enregistrée | mom60/80/rank | 0,17 | 0,023 | 2/4 | −0,059 | REJET |
| négociable, rebalancement tous les 3 jours (robustesse) | mom14/50/quintile | 0,58 | 0,103 | 2/4 | −0,067 | REJET |

**Meilleure cellule de la version principale (mom14/50/quintile), par an, à G = 1 :**

- jambe prix +37,3 % ;
- funding −3,0 % ;
- coûts −28,1 %, pour une rotation de 0,51 fois le capital par jour.

Son Sharpe brut vaut 1,34. Le Sharpe net vaut 0,90 à 6 pb, 0,24 à 15 pb et −0,48 à 25 pb. Aucune des 54 cellules n'atteint 1,0, même à 6 pb. Sharpe net par année civile : 2023 −0,98, 2024 0,87, 2025 0,54, 2026 −0,58.

Médianes par signal sur la grille de la version principale :

| Signal | Sharpe brut | Sharpe net 15 pb | Rotation par jour |
|---|---|---|---|
| carry3 | −0,16 | −1,46 | 0,42 |
| carry7 | 0,15 | −0,63 | 0,26 |
| mom14 | 1,01 | −0,02 | 0,44 |
| mom30 | 0,64 | −0,12 | 0,33 |
| mom60 | 0,55 | −0,02 | 0,24 |
| mom7 | 0,54 | −0,88 | 0,60 |
| resmom30 | 0,89 | 0,05 | 0,32 |
| rev1 | −0,10 | −3,84 | 1,45 |
| rev3 | −0,04 | −2,26 | 0,88 |

**Lecture.**

- Un momentum cross-sectionnel existe avant coûts sur les alts Hyperliquid, surtout sur 14 jours. C'est cohérent avec le facteur momentum documenté sur les cryptomonnaies (Liu, Tsyvinski et Wu 2022).
- Il ne survit pas à une rotation quotidienne au coût de référence.
- Le carry, qui achète le funding bas et vend le funding haut, encaisse 13 % à 25 % de funding par an, mais perd 11 % à 27 % sur les prix : les coins à funding élevé font mieux que ceux à funding bas.
- Avant coûts, le funding couvre cette perte dans 8 cellules carry sur 12 :
  - toutes les cellules carry7, avec +1,9 % à +9,1 % par an ;
  - Sharpe brut jusqu'à 0,54.
- Ce sont les coûts (−11 % à −30 % par an à 15 pb) qui rendent toutes les cellules carry perdantes : Sharpe net de −1,76 à −0,37.

**Fenêtre du tweet (08/07/2026 → 10/09/2026), à G = 2,5 et 15 pb :**

- Sharpe médian de la grille : −2,84 ;
- cellules à Sharpe ≥ 3,5 : 0 sur 54 ;
- rendement médian −17,6 %, maximum +11,8 %.

Le tweet annonçait +15,6 % en backtest et +20,5 % en réel. Sur cette fenêtre de 65 rendements quotidiens :

- à 15 pb, la meilleure des 54 cellules fait +11,8 % ;
- au coût le plus bas de la grille (6 pb), une seule cellule le dépasse : mom7/30/quintile, avec +23,7 % ;
- cette cellule est hors de l'univers top 50 du bot, où la meilleure cellule fait +2,6 %.

Une cellule sur 54 au-dessus d'un seuil, sur quelques semaines, relève de la sélection. Les constructions testées ne reproduisent donc pas le résultat du tweet : soit le bot fait autre chose, soit son chiffre tient à la chance sur les 64 jours annoncés.

**Benchmark aléatoire.** Les meilleures cellules battent 100 % des 200 signaux aléatoires persistants (φ = 0,9), dont le Sharpe net médian vaut −2,1.

Diagnostic ajouté après les verdicts, hors protocole, sur 20 tirages, top 50 et quintiles (`run_xs_ls.py diag`) :

- ces signaux tournent autant que la meilleure cellule : 0,58 fois le capital par jour, contre 0,51 ;
- leur Sharpe brut médian vaut −0,25, avec un intervalle à 90 % de [−1,21 ; 0,86], contre 1,34 pour la meilleure cellule.

À rotation égale, le Sharpe brut de la meilleure cellule dépasse le 95e centile des signaux aléatoires (0,86 < 1,34) : le benchmark confirme un signal avant coûts. Il ne corrige pas la sélection de la meilleure des 54 cellules et ne dit pas si le signal paie ses coûts. C'est le rôle du Sharpe net et du Sharpe déflaté, qui échouent.

## 3. Arc B : méta-labeling du manchon de tendance Hyperliquid

**Manchon brut.** C'est le manchon canonique `trend_backtest.run_pipeline`, sans modification :

- signal z sur 30 et 90 jours ;
- univers éligible par liquidité ;
- 12 noms, cible de volatilité, coûts de 5,5 pb, funding.

**Méta-modèle.** Il estime, pour chaque coin éligible et chaque jour, la probabilité que le côté donné par z soit gagnant sur h jours, funding compris. Il est entraîné en walk-forward mensuel purgé. La période hors échantillon compte 703 jours de décision étiquetés (01/10/2024 → 03/09/2026) et 42 613 jours-coin ; le taux de réussite de z y est de 51,8 %. Les Sharpe des manchons portent sur les rendements du 02/10/2024 au 10/09/2026.

Configuration principale : arbres de gradient, h = 7, étiquette nette du funding.

| Critère | Valeur | Seuil | Résultat |
|---|---|---|---|
| B1 perte log. | ΔLL = −0,0064, p = 0,94, t NW = −1,95 | ΔLL > 0, p < 0,05 | échoue |
| B2 AUC du méta | 0,534 [0,502 ; 0,565] | borne basse > 0,5 | passe |
| B3 Sharpe du manchon | 0,69 contre 0,82, écart −0,13, p = 0,59 | écart > 0, p < 0,05 | échoue |
| B4 stabilité | ΔLL par tiers : −0,0053, −0,0084, −0,0054 | > 0 dans 2 tiers sur 3 | échoue |
| B5 PSR du manchon méta | 0,842 | ≥ 0,95 | échoue |

Les 12 configurations (2 modèles × 3 horizons × 2 étiquettes) :

| Configuration | ΔLL | p | AUC méta | Sharpe méta | Écart de Sharpe | p |
|---|---|---|---|---|---|---|
| gbm_h1_net | −0,0009 | 0,89 | 0,527 | 0,24 | −0,58 | 0,80 |
| logit_h1_net | −0,0008 | 0,84 | 0,527 | 0,02 | −0,81 | 0,90 |
| gbm_h1_price | −0,0008 | 0,89 | 0,524 | 0,36 | −0,46 | 0,75 |
| logit_h1_price | −0,0008 | 0,84 | 0,523 | −0,04 | −0,86 | 0,90 |
| gbm_h3_net | −0,0019 | 0,85 | 0,534 | 0,73 | −0,09 | 0,57 |
| logit_h3_net | −0,0018 | 0,85 | 0,533 | 0,68 | −0,14 | 0,62 |
| gbm_h3_price | −0,0020 | 0,87 | 0,525 | 0,10 | −0,72 | 0,88 |
| logit_h3_price | −0,0019 | 0,87 | 0,527 | 0,74 | −0,08 | 0,59 |
| gbm_h7_net | −0,0064 | 0,94 | 0,534 | 0,69 | −0,13 | 0,59 |
| logit_h7_net | −0,0087 | 0,97 | 0,535 | 0,99 | +0,17 | 0,40 |
| gbm_h7_price | −0,0073 | 0,97 | 0,520 | 0,23 | −0,60 | 0,81 |
| logit_h7_price | −0,0087 | 0,97 | 0,526 | 1,03 | +0,21 | 0,35 |

**Lecture.**

- Dans aucune configuration le méta-modèle ne prédit mieux que z seul hors échantillon : ΔLL est négatif partout. Sur la configuration principale, l'AUC de z seul (0,558) dépasse celle du méta-modèle (0,534).
- Les variables de prix, de volume et de funding n'ajoutent pas d'information détectable. Elles ajoutent du bruit.
- Le meilleur écart de Sharpe (logit_h7_price, +0,21) n'est pas significatif (p = 0,35), et sa perte logarithmique est plus mauvaise que celle de z seul.
- Le manchon brut, sans filtre, fait 0,82 de Sharpe, +11,6 % par an pour 14,1 % de volatilité et −14,1 % de baisse maximale sur la même période. Ce chiffre est descriptif : il ne passe aucun test de ce protocole.

## 4. Arc C : méta-labeling de A4_BE_V50_L1

**Filtre testé.** Le méta-modèle estime, pour BTC et ETH, la probabilité qu'une position ouverte par le cadran batte la trésorerie sur 7 jours, après l'exécution décalée d'un jour. La position est annulée quand cette probabilité passe sous 0,5.

**Évaluation.** Walk-forward annuel purgé, sur la période hors échantillon 2018-2024. Moteur, coûts et décalage sont ceux de l'étude d'allocation. La réplication des rendements quotidiens de A4 publiés par l'étude est exacte (écart maximal nul).

**Filtre principal.** Il retire 13,4 % des positions. Le taux de réussite de base est de 53,0 %.

| Critère | Valeur | Seuil | Résultat |
|---|---|---|---|
| C1 perte log. | ΔLL = −0,0042, p = 0,79 | ΔLL > 0, p < 0,05 | échoue |
| C2 croissance log. | +2,0 %/an, t NW = 0,38 | > 0, t ≥ 2 | échoue |
| C3 années positives | 4 sur 7 | ≥ 5 | échoue |
| C4 baisse maximale | −56,4 % contre −61,5 % | pas plus de 5 points pire | passe |

Écart annuel de croissance logarithmique, filtre moins A4 : 2018 +9,1 %, 2019 +2,9 %, 2020 +9,2 %, 2021 +22,9 %, 2022 −2,9 %, 2023 −15,3 %, 2024 −11,7 %.

| Configuration | ΔLL | p | Croissance log. | t NW | Années > 0 | Rendement annuel filtre | Rendement annuel A4 |
|---|---|---|---|---|---|---|---|
| gbm_h7_filter | −0,0109 | 0,96 | −2,5 % | −0,40 | 3 | 28,6 % | 31,9 % |
| logit_h7_filter | −0,0042 | 0,79 | +2,0 % | 0,38 | 4 | 34,6 % | 31,9 % |
| logit_h7_size | −0,0042 | 0,79 | −18,3 % | −1,28 | 2 | 9,8 % | 31,9 % |
| gbm_h14_filter | −0,0191 | 0,96 | −2,8 % | −0,40 | 2 | 28,3 % | 31,9 % |
| logit_h14_filter | −0,0103 | 0,87 | +2,0 % | 0,39 | 4 | 34,6 % | 31,9 % |

**Variante `size`.** Elle dimensionne par la taille de pari de López de Prado au lieu de filtrer, ce qui réduit fortement l'exposition :

- Sharpe 1,22 contre 0,88 ;
- baisse maximale −14,1 % contre −61,5 % ;
- mais −18,3 % par an de croissance logarithmique (t NW = −1,28), le critère enregistré, qui est celui de l'objectif de richesse médiane.

Son modèle est celui du filtre principal, dont la perte logarithmique ne bat pas la base. Le gain de Sharpe n'a pas été testé par le protocole ; il vient d'une exposition moyenne réduite, pas d'une prévision validée.

**Période contaminée (2025-01-01 → 2026-09-23), descriptive seulement.** Le modèle a été entraîné sur 2016-2024 :

- A4 29,9 % par an, filtre −2,8 % ;
- écart de croissance −29,0 % par an (t NW = −2,03) ;
- baisse maximale −37,0 % contre −28,8 %.

Hors de l'échantillon d'estimation, le filtre détruit de la valeur : c'est le comportement attendu d'un modèle qui a appris du bruit.

## 5. Contrôles synthétiques et puissance

| Contrôle | Résultat | Critère | Conforme |
|---|---|---|---|
| B, aucune prévisibilité (20 graines) | 0 faux positif(s) sur B1 | ≤ 3 | oui |
| B, effet planté κ = 0,20 (10 graines) | 10 détections sur B1 | ≥ 8 | oui |
| B, effet planté κ = 0,10 (10 graines) | 0 sur B1, 9 sur B3 | publié | sans objet |
| C, aucune prévisibilité (20 graines) | 0 faux positif(s) sur C1 | ≤ 3 | oui |
| C, effet planté κ = 0,30 (10 graines) | 10 détections sur C1 | ≥ 8 | oui |
| C, effet planté κ = 0,20 (10 graines) | 7 détections sur C1 | publié | sans objet |

La machinerie détecte un effet conditionnel fort et ne produit pas de faux positif sur les critères de perte logarithmique. Sa puissance face à un effet modéré dépend du test.

**Arc B.**

- κ = 0,10 correspond à un écart de 5 à 9 points de taux de réussite entre états.
- À ce niveau, le test de perte logarithmique ne détecte rien, mais le test économique B3 détecte l'effet dans 9 graines sur 10.
- Sous l'hypothèse nulle, B3 donne 2 faux positifs sur 20.

**Arc C.** À κ = 0,20, soit 11 à 20 points d'écart, C1 détecte l'effet dans 7 graines sur 10. À κ = 0,30, soit 20 à 29 points, il le détecte dans 10 sur 10.

**Conséquence.** Les REJET des arcs B et C excluent un effet fort. Ils n'excluent pas un effet de quelques points. Mais un tel effet ne peut pas être validé sur ces échantillons, et déployer un filtre non validable revient à le faire sans preuve.

## 6. Essais comptés

Registre `results/trials_alts_ml.csv` : arc A 54, arc B 12, arc C 5, soit 71 essais.

Avec les 339 essais de l'étude d'allocation, le programme en compte 410. Le registre de l'étude d'allocation n'est pas modifié, pour que ses fichiers de décision restent reproductibles à l'identique.

## 7. Limites

- **Valorisation quotidienne.** Ni chemin intrajournalier, ni liquidation, ni marge. À G = 2,5, la baisse maximale de la meilleure cellule de l'arc A atteint déjà −58 % en quotidien.
- **Coûts.** Coûts proportionnels constants, sans impact de marché : aucun test de capacité.
- **Périodes hors échantillon courtes.** 23 mois pour l'arc B, 7 ans sur deux actifs corrélés pour l'arc C. Les effets minimaux détectables sont annoncés dans le protocole (B.11, C.11).
- **Hyperparamètres.** Ceux des méta-modèles ont été fixés sur données synthétiques, avant tout run réel. Un autre choix raisonnable pourrait donner un chiffre différent. Les 12 et 5 configurations publiées donnent toutes le même verdict.
- **Étiquettes.** Celles de l'arc B sont dominées par le facteur de marché commun aux coins d'un même jour. C'est ce qui limite l'apprentissage de variables de marché, retirées du modèle.
- **Horodatage du funding.** La somme journalière rattache le paiement de 00 h 00 au jour suivant. Cela décale une heure sur 24 depuis le 08/06/2023, et 8 heures sur 24 avant, quand le funding était payé toutes les 8 heures. La même convention sert à `xs_ls` et aux étiquettes et au manchon de l'arc B. L'effet est négligeable devant les écarts mesurés.
- **Tests.** Dans une simulation du relecteur, les tests par bootstrap rejettent 6 à 8 % du temps à 5 % nominal. Ils sont donc un peu libéraux, ce qui ne change rien à des REJET.
- **Critère B2.** Il compare l'AUC du méta-modèle à 0,5, pas à celle de z seul. Il passe sur données réelles (borne basse 0,502) alors que z seul fait mieux. Un futur protocole devra tester l'écart d'AUC.

## Reproduire

```bash
cd research
python scripts/build_hl_panel.py --cache <STRAAT>/hl_cache --check   # identité du panneau avec le chargeur xs_ls
python scripts/run_xs_ls.py                                          # arc A (trois versions)
python scripts/run_xs_ls.py diag                                     # diagnostic du benchmark aléatoire (hors protocole)
python scripts/run_metalabel.py controls                             # contrôles synthétiques
python scripts/run_metalabel.py hl                                   # arc B
python scripts/run_metalabel.py a4                                   # arc C
ALLOC_UNLOCK_HOLDOUT=I_ACCEPT_ONE_SHOT python scripts/run_metalabel.py a4_contaminated
python scripts/make_alts_report.py
```

## Références

- Bailey, D. H. et López de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk* 15(2).
- Bailey, D. H. et López de Prado, M. (2014). The deflated Sharpe ratio. *Journal of Portfolio Management* 40(5).
- Joubert, J. F. (2022). Meta-labeling: theory and framework. *Journal of Financial Data Science* 4(3).
- Ledoit, O. et Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. *Journal of Empirical Finance* 15, 850-859.
- Liu, Y., Tsyvinski, A. et Wu, X. (2022). Common risk factors in cryptocurrency. *Journal of Finance* 77(2).
- López de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley, chapitres 3, 7 et 10.
- Moskowitz, T., Ooi, Y. H. et Pedersen, L. H. (2012). Time series momentum. *Journal of Financial Economics* 104(2).
- Politis, D. et Romano, J. (1994). The stationary bootstrap. *Journal of the American Statistical Association* 89(428).

Ce n'est pas un conseil en investissement.
