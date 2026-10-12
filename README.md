# CreditScore  — Évaluation du risque de crédit

> Prototype de Machine Learning qui estime la probabilité statistique de défaut d'un demandeur de crédit à partir de son profil et des caractéristiques du crédit demandé.

## 🎯 Objectif

Le projet explore comment la Data Science peut aider une équipe crédit à analyser le risque de défaut et à structurer une première estimation du risque à partir des informations disponibles au moment de la demande.

**CreditScore  est un prototype pédagogique.** Il ne remplace ni l'analyse d'un analyste crédit ni les règles de décision d'un établissement financier.

## 🧩 Problématique métier

**Comment estimer la probabilité qu'un demandeur de crédit fasse défaut à partir des informations disponibles au moment de sa demande, afin de mieux éclairer l'analyse du risque ?**

Une telle estimation pourrait, après validation sur des données adaptées au contexte concerné, contribuer à :
- prioriser les dossiers pour une analyse complémentaire ;
- comparer les profils selon un score de risque ;
- soutenir le suivi de la qualité du portefeuille ;
- alimenter une réflexion sur les politiques d'octroi.

Le score ne doit pas être utilisé seul pour accepter ou refuser un crédit.

## 📊 Données

- **Source :** dataset public de risque de crédit disponible sur Kaggle.
- **Nature :** données tabulaires de demandeurs et de prêts.
- **Cible :** `loan_status` (la classe 1 représente le défaut dans le dataset utilisé pour le projet).
- **Variables d'entrée :** âge, revenu annuel, statut du logement, ancienneté professionnelle, objet du crédit, montant demandé, part du revenu consacrée au crédit, antécédent de défaut et ancienneté de l'historique de crédit.
- **Contexte géographique :** le dataset n'est pas fourni par une banque ivoirienne et ne doit pas être présenté comme représentant directement sa clientèle.

Les montants sont affichés dans l'interface en FCFA. Le service applique actuellement un facteur de conversion fixe de **600 FCFA pour 1 USD** pour transformer les montants saisis en FCFA vers l'échelle USD attendue par le modèle. Ce facteur est une hypothèse de conversion technique, pas un taux de change en temps réel. Avant tout usage sérieux, il faut confirmer l'unité et l'échelle des montants du dataset original, puis valider cette conversion.

## 🔬 Méthodologie

Le projet suit une démarche centrée sur le problème métier :

1. Compréhension de la problématique de risque de crédit
2. Identification de la cible et des variables disponibles
3. Préparation des données et traitement des valeurs manquantes
4. Analyse exploratoire et préparation des variables
5. Entraînement et évaluation du modèle dans le notebook de travail
6. Sauvegarde du pipeline de Machine Learning
7. Intégration du pipeline dans une API FastAPI
8. Création d'une interface web de saisie
9. Déploiement de l'application sur Render
10. Vérification du comportement de l'API et des limites du prototype

### Variables envoyées au modèle

```text
person_age
person_income
person_home_ownership
person_emp_length
loan_intent
loan_amnt
cb_person_default_on_file
cb_person_cred_hist_length
```

La cible `loan_status` n'est pas une variable d'entrée. La part du revenu consacrée au crédit est calculée comme le montant du crédit divisé par le revenu annuel, après conversion cohérente des montants.

## 🤖 Modèle

Le fichier `modele_rf.pkl` contient un pipeline Scikit-learn chargé par l'application à l'aide de Joblib. Le pipeline regroupe le prétraitement et le modèle de classification.

Le service utilise `predict_proba` pour obtenir une probabilité estimée de défaut. Un seuil expérimental de **0,40 (40 %)** est ensuite appliqué pour afficher une classe descriptive :
- probabilité supérieure ou égale à 40 % : « Défaut probable » ;
- probabilité inférieure à 40 % : « Non-défaut probable ».

Ce seuil est expérimental et ne représente pas une politique d'octroi validée par une banque.

## 📈 Évaluation

Les performances du modèle doivent être documentées à partir des résultats réellement obtenus sur un jeu de test indépendant. Les métriques pertinentes incluent notamment :
- ROC-AUC ;
- précision et rappel de la classe défaut ;
- F1-score ;
- matrice de confusion ;
- calibration des probabilités, si l'application doit présenter les sorties comme des probabilités interprétables.

Aucune métrique n'est annoncée ici sans référence vérifiée aux résultats de l'expérience utilisée pour le modèle déployé.

## 🏗️ Architecture

```text
Profil du demandeur
       │
       ▼
Interface HTML / CSS / JavaScript
       │
       ▼
API FastAPI — validation des entrées
       │
       ▼
Service de prédiction
       │
       ├── Conversion monétaire (hypothèse fixe à vérifier)
       ├── Construction des 9 variables attendues
       └── Pipeline Scikit-learn : modele_rf.pkl
       │
       ▼
Probabilité estimée + classe descriptive
```

## 🖥️ Application et API

- **Interface web :** formulaire de profil et de demande de crédit.
- **Contrôle de santé :** `GET /api/health`.
- **Prédiction :** `POST /api/predict`.
- **Documentation interactive FastAPI :** `/docs` sur l'instance en cours d'exécution.

## 🛠️ Technologies

- Python
- Pandas / NumPy
- Scikit-learn / Joblib
- FastAPI / Pydantic
- Uvicorn
- HTML / CSS / JavaScript
- Render pour l'hébergement

## 🚀 Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/Sela80/CreditScore.git
cd CreditScore
```

### 2. Créer un environnement virtuel et installer les dépendances

```bash
python -m venv .venv
```

Sous Windows :

```bash
.venv\\Scripts\\activate
```

Sous macOS / Linux :

```bash
source .venv/bin/activate
```

Puis :

```bash
pip install -r requirements.txt
```

## 📁 Structure du dépôt

```text
CreditScore/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
├── modele_rf.pkl
├── requirements.txt
├── render.yaml
├── .gitignore
└── README.md
```

## ⚠️ Limites et précautions

- Le dataset est public et issu de Kaggle ; il ne représente pas automatiquement les demandeurs de crédit d'une banque ivoirienne.
- Les unités monétaires du dataset et la conversion FCFA/USD doivent être vérifiées avant d'interpréter les scores.
- Le seuil de 40 % est expérimental et n'est pas une règle de décision bancaire validée.
- Une probabilité fournie par un modèle n'est pas nécessairement bien calibrée.
- Les performances peuvent varier sur une population différente de celle d'entraînement.
- Les biais, la protection des données, l'explicabilité, la conformité et la validation métier doivent être examinés avant tout usage opérationnel.
- Le résultat ne constitue pas une décision d'octroi de crédit.

## 🔗 Démonstration

L'application est déployée sur Render : **[Ouvrir CreditScore CI](https://creditscore-y913.onrender.com)**.

- Application : https://creditscore-y913.onrender.com
- Vérification de l'API : https://creditscore-y913.onrender.com/api/health
- Documentation interactive : https://creditscore-y913.onrender.com/docs

## 👤 Auteur

**Kouakou Gédéon Sela**

Aspiring Data Scientist | Python · SQL · Machine Learning · Power BI | Data Science appliquée à la Banque & Finance |

- GitHub : https://github.com/Sela80
- Projet : https://github.com/Sela80/CreditScore

---

### 📌 Projet de portfolio

Projet pédagogique réalisé pour mettre en pratique une démarche complète de Data Science appliquée au risque de crédit : compréhension métier, préparation des données, modélisation, interprétation et intégration dans une application web. Les résultats doivent être validés avant toute utilisation réelle.
