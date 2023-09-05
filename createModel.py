from challenge.model import DelayModel
import joblib
import pandas as pd


model = DelayModel()
data = pd.read_csv(filepath_or_buffer="./data/data.csv")
features, target = model.preprocessApi(
    data=data,
    target_column="delay"
)
model.fit(features=features, target=target)
joblib.dump(model._model, './trained_model_final1.pkl')
