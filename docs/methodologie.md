# Méthodologie — CreditScore CI

## 1. Contexte métier

Une équipe crédit doit évaluer le risque qu'un emprunteur ne rembourse pas son prêt. Un score statistique peut aider à structurer l'analyse, mais il ne doit pas remplacer l'étude complète du dossier ni la politique de crédit de la banque.

## 2. Question Data

Peut-on estimer la probabilité de défaut à partir des informations connues au moment de la demande de crédit ?

## 3. Source et périmètre des données

Le projet utilise un dataset public de risque de crédit provenant de Kaggle. Il ne s'agit pas de données internes d'une banque ivoirienne. Les résultats sont donc expérimentaux et leur transférabilité au contexte ivoirien n'est pas acquise.

À compléter dans la documentation du notebook :
- URL exacte du dataset ;
- période et population représentée ;
- nombre d'observations initiales et finales ;
- traitement des valeurs manquantes et des valeurs aberrantes ;
- répartition de la cible ;
- définition exacte des unités monétaires.

## 4. Cible et variables

La cible est `loan_status`, où la classe 1 représente le défaut dans le dataset utilisé. Le modèle reçoit les neuf variables suivantes :

| Variable | Description |
|---|---|
| `person_age` | Âge du demandeur |
| `person_income` | Revenu annuel |
| `person_home_ownership` | Statut du logement |
| `person_emp_length` | Ancienneté professionnelle |
| `loan_intent` | Objet du crédit |
| `loan_amnt` | Montant demandé |
| `loan_percent_income` | Part du revenu consacrée au crédit |
| `cb_person_default_on_file` | Antécédent de défaut enregistré |
| `cb_person_cred_hist_length` | Ancienneté de l'historique de crédit |

## 5. Pipeline et inférence

Le fichier `modele_rf.pkl` est chargé par Joblib. Le code de déploiement construit un DataFrame contenant les variables attendues et appelle `predict_proba`. Le prétraitement fait partie du pipeline sauvegardé ; il ne faut pas le refaire manuellement dans le service d'inférence.

Le service actuel convertit les revenus et les montants de FCFA vers USD à l'aide d'un facteur fixe de 600 FCFA/USD, puis calcule le ratio montant/revenu. Ce choix doit être vérifié par rapport aux unités réellement utilisées lors de l'entraînement. Si le dataset et le modèle utilisent une autre échelle, les entrées doivent être corrigées avant d'interpréter les résultats.

## 6. Seuil et décision

Le seuil de 0,40 est une valeur expérimentale utilisée pour afficher une catégorie. Il ne doit pas être assimilé à un seuil d'acceptation ou de refus de crédit approuvé par une banque. Le choix d'un seuil professionnel nécessiterait une analyse des coûts d'erreur, des contraintes métier, de la calibration, de l'équité et de la validation du modèle.

## 7. Évaluation à documenter

Reporter ici uniquement les résultats du modèle réellement déployé :
- ROC-AUC ;
- précision, rappel et F1-score pour la classe défaut ;
- matrice de confusion au seuil retenu ;
- courbe de calibration et Brier score, si pertinents ;
- comparaison à une baseline ;
- validation sur des données représentatives de la population cible.

## 8. Limites et risques

- Décalage possible entre le dataset public et une clientèle bancaire ivoirienne.
- Unités monétaires et hypothèse de conversion à confirmer.
- Probabilités possiblement mal calibrées.
- Risques de biais et d'usage abusif d'une catégorie binaire.
- Absence de validation institutionnelle et de gouvernance bancaire.
- La prédiction ne doit pas être utilisée seule pour prendre une décision d'octroi.

## 9. Prochaines améliorations

1. Vérifier l'origine, les unités et la définition des variables dans le dataset source.
2. Confirmer que le pipeline déployé est celui évalué dans le notebook.
3. Ajouter des tests automatisés sur la validation des entrées et les réponses de l'API.
4. Documenter les résultats du jeu de test sans inventer de métriques.
5. Surveiller les erreurs, les dérives et la qualité des données si le prototype évolue.
