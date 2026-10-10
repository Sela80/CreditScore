import joblib
import pandas as pd
import os
import logging

# Configuration du log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Taux de conversion Kaggle (USD) vers interface (FCFA)
USD_TO_XOF = 600.0
SEUIL_EXPERIMENTAL = 0.40

class ModelService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path):
            logger.error(f"Modèle introuvable : {self.model_path}")
            raise FileNotFoundError("Le fichier modele_rf.pkl est introuvable.")
        
        try:
            self.model = joblib.load(self.model_path)
            logger.info("Modèle chargé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle : {e}")
            raise

    def predict(self, data: dict) -> dict:
        if self.model is None:
            raise RuntimeError("Le modèle n'est pas chargé.")

        # 1. Conversion monétaire (FCFA -> USD pour le modèle)
        income_usd = data["person_income"] / USD_TO_XOF
        loan_amnt_usd = data["loan_amnt"] / USD_TO_XOF
        
        # 2. Calcul de la variable dérivée
        loan_percent_income = loan_amnt_usd / income_usd if income_usd > 0 else 0.0

        # 3. Construction du DataFrame dans l'ordre exact
        features = {
            "person_age": data["person_age"],
            "person_income": income_usd,
            "person_home_ownership": data["person_home_ownership"],
            "person_emp_length": data["person_emp_length"],
            "loan_intent": data["loan_intent"],
            "loan_amnt": loan_amnt_usd,
            "loan_percent_income": loan_percent_income,
            "cb_person_default_on_file": data["cb_person_default_on_file"],
            "cb_person_cred_hist_length": data["cb_person_cred_hist_length"]
        }
        
        X = pd.DataFrame([features])

        # 4. Prédiction
        if hasattr(self.model, "predict_proba"):
            probas = self.model.predict_proba(X)[0]
            classes = self.model.classes_
            
            # Trouver l'index de la classe positive (1)
            if 1 in classes:
                idx_default = list(classes).index(1)
            else:
                idx_default = 1 # Fallback par défaut si la classe 1 n'est pas nommée ainsi
                
            prob_default = float(probas[idx_default])
        else:
            raise ValueError("Le modèle ne supporte pas predict_proba.")

        # 5. Classification selon le seuil
        predicted_class = "Défaut probable" if prob_default >= SEUIL_EXPERIMENTAL else "Non-défaut probable"

        return {
            "success": True,
            "default_probability": round(prob_default, 4),
            "threshold": SEUIL_EXPERIMENTAL,
            "predicted_class": predicted_class,
            "message": "Estimation statistique. Ne constitue pas une décision d'octroi."
        }