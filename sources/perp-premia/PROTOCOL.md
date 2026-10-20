# Protocole pré-enregistré : test de deux primes de risque sur perpétuels crypto

Date de rédaction : 2026-09-08. Ce document est figé avant la première exécution sur données réelles.
Toute modification ultérieure des paramètres doit être consignée dans la section « Amendements » avec la date et la raison, et compte comme un essai supplémentaire dans le calcul du Sharpe déflaté.

## 1. Question

Existe-t-il, pour un acteur retail, un rendement résiduel positif net de coûts et de fiscalité,
au-delà de la détention passive de BTC, dans l'une des deux primes documentées suivantes :

- H1 (carry) : long spot, short perpétuel, encaissement du funding (Schmeling, Schrimpf, Todorov 2023, BIS).
- H2 (momentum temporel) : position dans le sens du rendement passé à 1 à 4 semaines (Moskowitz, Ooi, Pedersen 2012 ; Liu, Tsyvinski 2021).

## 2. Données

- Source : Binance USDT-M perpétuels (prix, volume, funding toutes les 8 h) et Binance spot (prix), via ccxt.
- Fréquence : quotidienne, UTC, clôture.
- Période : du 2019-09-10 (lancement des perpétuels Binance) à la date d'exécution.
- Limite connue : ccxt n'expose que les contrats actifs. Les contrats délistés sont absents.
  Ce biais du survivant surestime légèrement le momentum. Il est documenté ici et rappelé dans les résultats.

## 3. Univers point-in-time

À chaque date t, un symbole est éligible si :
- il possède au moins 60 jours d'historique avant t ;
- sa médiane glissante 30 jours de volume en dollars est supérieure ou égale à 10 millions.

## 4. Règles des stratégies (fixées)

Rebalancement : hebdomadaire (tous les 7 jours calendaires). Entre deux rebalancements, les poids sont conservés.
Décision à la clôture de t, rendement réalisé sur t+1. Aucune information postérieure à t n'entre dans la décision.

### H1 carry

- Signal : moyenne du funding quotidien sur les 7 derniers jours, annualisée (× 365).
- Entrée : signal supérieur à 10 % annualisé et symbole dans le premier décile du signal parmi les éligibles.
- Poids : égalitaire, 50 % du capital par jambe (spot long, perp short), donc exposition brute maximale 100 %.
- Rendement quotidien d'une position : r_spot − r_perp + funding_reçu.
- Coûts : 10 points de base par jambe et par transaction (frais 5 + glissement 5), appliqués sur la variation absolue des poids, deux jambes.

### H2 momentum temporel

- Signal : signe du rendement du perpétuel sur les 14 derniers jours.
- Poids : signe × (20 % / volatilité annualisée glissante 30 jours), plafonné à 2, divisé par le nombre d'éligibles.
- Rendement quotidien d'une position : poids × (r_perp − funding), le long paie le funding, le short le reçoit.
- Coûts : 10 points de base par transaction sur la variation absolue des poids.

## 5. Essais déclarés (pour le Sharpe déflaté)

- Carry : lookback ∈ {3, 7, 14} jours × seuil ∈ {5 %, 10 %, 20 %} = 9 configurations.
- Momentum : lookback ∈ {7, 14, 21, 28} jours = 4 configurations.
- Total : 13 essais. Configuration primaire : carry (7 j, 10 %), momentum (14 j).
- Toute configuration ajoutée après coup incrémente ce compteur.

## 6. Découpage temporel

- In-sample : 2019-09-10 au 2022-12-31 (contient les baisses de 2020 et de 2022).
- Out-of-sample : 2023-01-01 à la date d'exécution.
- Les paramètres ne sont pas optimisés sur l'in-sample : ils sont fixés ci-dessus. Le découpage sert à mesurer la stabilité.

## 7. Métriques

- Rendement annualisé, volatilité, Sharpe (base 365), drawdown maximal.
- Alpha et bêta contre BTC spot (régression, erreurs Newey-West, 10 retards), t-stat de l'alpha.
- Sharpe déflaté (Bailey, López de Prado 2014) avec N = 13 essais, skewness et kurtosis empiriques.
- Intervalle de confiance bootstrap par blocs (blocs de 20 jours, 2000 tirages) du Sharpe.
- Rendement annualisé après fiscalité française (30 % sur les années positives).

## 8. Critères de décision (fixés avant exécution)

Une hypothèse est retenue uniquement si, pour sa configuration primaire :

1. Sharpe net out-of-sample supérieur au Sharpe de BTC spot sur la même période ;
2. t-stat Newey-West de l'alpha out-of-sample supérieure à 2 ;
3. Sharpe déflaté sur l'échantillon complet supérieur ou égal à 0,95 ;
4. drawdown maximal inférieur à 50 % ;
5. rendement annualisé après fiscalité positif.

Si un seul critère échoue, l'hypothèse est rejetée. Pas de recherche de paramètres a posteriori pour la sauver.

## 9. Amendements

(vide)

## Références

- Bailey D., Borwein J., López de Prado M., Zhu Q. (2014). Pseudo-Mathematics and Financial Charlatanism. Notices of the AMS.
- Bailey D., López de Prado M. (2014). The Deflated Sharpe Ratio. Journal of Portfolio Management.
- Harvey C., Liu Y., Zhu H. (2016). ... and the Cross-Section of Expected Returns. Review of Financial Studies.
- Liu Y., Tsyvinski A. (2021). Risks and Returns of Cryptocurrency. Review of Financial Studies.
- Moskowitz T., Ooi Y., Pedersen L. (2012). Time Series Momentum. Journal of Financial Economics.
- Schmeling M., Schrimpf A., Todorov K. (2023). Crypto Carry. BIS Working Papers.
