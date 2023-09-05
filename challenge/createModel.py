from challenge.model import DelayModel
import joblib
import pandas as pd


model = DelayModel()
data = pd.read_csv(filepath_or_buffer="./data/data.csv")
features = model.preprocess(
    data=data
)

joblib.dump(model._model, 'trained_model.pkl')
