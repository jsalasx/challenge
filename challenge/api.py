import fastapi
from challenge.model import DelayModel
import pandas as pd
from challenge.apiDTO import FlightData
from fastapi.responses import JSONResponse
from fastapi import Request, status
import joblib
from fastapi.exceptions import RequestValidationError
app = fastapi.FastAPI()

model = joblib.load('trained_model_final1.pkl')

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error" + str(exc)},
    )
@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK2"
    }

@app.post("/predict", status_code=200)
async def post_predict(input: FlightData) -> any:
    predict_df = pd.DataFrame([flight.dict() for flight in input.flights])
    predict_df = pd.concat([
        pd.get_dummies(predict_df['OPERA'], prefix='OPERA'),
        pd.get_dummies(predict_df['TIPOVUELO'], prefix='TIPOVUELO'),
        pd.get_dummies(predict_df['MES'], prefix='MES')],
        axis=1
    )
    
    expected_features = model.get_booster().feature_names
    predict_df = predict_df.reindex(columns=expected_features).fillna(0)
    predicted_targets = model.predict(
        predict_df
    )
    xgboost_y_preds = [1 if y_pred >
                       0.5 else 0 for y_pred in predicted_targets]
    resp = {"predict": xgboost_y_preds}
    return resp    