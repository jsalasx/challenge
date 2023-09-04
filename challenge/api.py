import fastapi
from challenge.model import DelayModel
import pandas as pd
from challenge.apiDTO import FlightData
from sklearn.utils import shuffle
app = fastapi.FastAPI()

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
    
    model = DelayModel()
    data = pd.read_csv(filepath_or_buffer="./data/data.csv")
    features = model.preprocessApi(
        data=data
    )
    
    expected_features = features.columns.tolist()

    # Supongamos que 'predict_df' es el DataFrame con el que quieres hacer la predicción
    predict_df = predict_df.reindex(columns=expected_features).fillna(0)
    
    
    print("df")
    print(predict_df)
    predicted_targets = model.predict(
        predict_df
    )
    print("PREDECIDO")
    print(predicted_targets)

    return {"received_data": "Ok"}
    