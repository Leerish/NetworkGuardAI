import sys
import os
import certifi
import pymongo
import pandas as pd

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile , Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)


load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")


ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory= "./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train", tags=["training"])
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(content="Training is successful", media_type="text/plain")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PREPROCESSOR_PATH = os.path.join(BASE_DIR, "final_model", "preprocessor.pkl")
        MODEL_PATH = os.path.join(BASE_DIR, "final_model", "model.pkl")
        
        print("[DEBUG] Preprocessor path:", PREPROCESSOR_PATH)
        print("[DEBUG] File exists?", os.path.exists(PREPROCESSOR_PATH))
        
        preprocessor = load_object(PREPROCESSOR_PATH)
        final_model = load_object(MODEL_PATH)
        
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prediction_output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "output.csv")
        df.to_csv(output_path)
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run("main:app", host="localhost", port=8000, reload=True)
