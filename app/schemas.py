from pydantic import BaseModel, Field, validator
from typing import List

class CreditRequest(BaseModel):
    person_age: int = Field(..., gt=18, lt=100, description="Âge du demandeur")
    person_income: float = Field(..., gt=0, description="Revenu annuel en FCFA")
    person_home_ownership: str = Field(..., description="Statut du logement")
    person_emp_length: int = Field(..., ge=0, description="Ancienneté professionnelle")
    loan_intent: str = Field(..., description="Objet du crédit")
    loan_amnt: float = Field(..., gt=0, description="Montant du crédit en FCFA")
    cb_person_default_on_file: str = Field(..., description="Antécédent de défaut")
    cb_person_cred_hist_length: int = Field(..., ge=0, description="Ancienneté crédit")

    @validator('person_home_ownership')
    def validate_home_ownership(cls, v):
        allowed = {"RENT", "MORTGAGE", "OWN", "OTHER"}
        if v not in allowed:
            raise ValueError(f"Statut invalide. Choix autorisés : {allowed}")
        return v

    @validator('loan_intent')
    def validate_loan_intent(cls, v):
        allowed = {"EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"}
        if v not in allowed:
            raise ValueError(f"Objet invalide. Choix autorisés : {allowed}")
        return v

    @validator('cb_person_default_on_file')
    def validate_default(cls, v):
        if v not in {"Y", "N"}:
            raise ValueError("Doit être 'Y' ou 'N'")
        return v

class PredictionResponse(BaseModel):
    success: bool
    default_probability: float = None
    threshold: float = None
    predicted_class: str = None
    message: str