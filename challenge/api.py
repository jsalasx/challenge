import fastapi
from challenge.model import DelayModel
import pandas as pd
from challenge.apiDTO import FlightData
from sklearn.utils import shuffle
from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
import joblib
app = fastapi.FastAPI()

model = DelayModel()
data = pd.read_csv(filepath_or_buffer="./data/data.csv")
features = model.preprocess(
    data=data
)
joblib.dump(model._model, 'trained_model.pkl')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(input: FlightData) -> dict:
    predict_df = pd.DataFrame([flight.dict() for flight in input.flights])
    predict_df = pd.concat([
        pd.get_dummies(predict_df['OPERA'], prefix='OPERA'),
        pd.get_dummies(predict_df['TIPOVUELO'], prefix='TIPOVUELO'),
        pd.get_dummies(predict_df['MES'], prefix='MES')],
        axis=1
    )
    
    expected_features = features.columns.tolist()
    predict_df = predict_df.reindex(columns=expected_features).fillna(0)
    predicted_targets = model.predict(
        predict_df
    )
    resp = {"predict": predicted_targets}
    return resp
    