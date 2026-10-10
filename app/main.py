from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .schemas import CreditRequest, PredictionResponse
from .services import ModelService
import os
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="CreditScore CI", version="1.0.0")

# Montage des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialisation du service
MODEL_PATH = "modele_rf.pkl"
try:
    model_service = ModelService(MODEL_PATH)
except Exception as e:
    logger.critical(f"Échec de l'initialisation : {e}")
    model_service = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    if model_service is None or model_service.model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "healthy", "model_loaded": True}

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_credit_risk(payload: CreditRequest):
    if model_service is None:
        raise HTTPException(status_code=503, detail="Service de prédiction indisponible")
    
    try:
        result = model_service.predict(payload.dict())
        return result
    except Exception as e:
        logger.error(f"Erreur de prédiction : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la prédiction.")