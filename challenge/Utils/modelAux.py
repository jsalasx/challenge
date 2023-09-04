from xgboost import plot_importance
import xgboost as xgb
import matplotlib.pyplot as plt
from GetPeriodDayFunction import get_period_day
from IsHighSeasionFunction import is_high_season
from GetMinDiffFunction import get_min_diff
from GetRateFromColumnFunction import get_rate_from_column
from typing import Tuple, Union, List
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
warnings.filterwarnings('ignore')

#data = pd.read_csv('../data/dataAux.csv')
data = pd.read_csv('data/data.csv')
# data.info()

# OK
data['period_day'] = data['Fecha-I'].apply(get_period_day)
# OK
data['high_season'] = data['Fecha-I'].apply(is_high_season)
# OK
data['min_diff'] = data.apply(get_min_diff, axis=1)
threshold_in_minutes = 15
# OK
data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)



training_data = shuffle(
    data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state=111)

features = pd.concat([
    pd.get_dummies(training_data['OPERA'], prefix='OPERA'),
    pd.get_dummies(training_data['TIPOVUELO'], prefix='TIPOVUELO'),
    pd.get_dummies(training_data['MES'], prefix='MES')],
    axis=1
)
target = data['delay']
x_train, x_test, y_train, y_test = train_test_split(
    features, target, test_size=0.33, random_state=42)

print(f"train shape: {x_train.shape} | test shape: {x_test.shape}")
top_10_features = [
    "OPERA_Latin American Wings",
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]
x_train, x_test, y_train, y_test = train_test_split(
    features[top_10_features], target, test_size=0.33, random_state=42)

print(f"train shape: {x_train.shape} | test shape: {x_test.shape}")

y_train.value_counts('%')*100
y_test.value_counts('%')*100
xgb_model = xgb.XGBClassifier(random_state=1, learning_rate=0.01)
xgb_model.fit(x_train, y_train)
xgboost_y_preds = xgb_model.predict(x_test)
xgboost_y_preds = [1 if y_pred > 0.5 else 0 for y_pred in xgboost_y_preds]
confusion_matrix(y_test, xgboost_y_preds)
print(classification_report(y_test, xgboost_y_preds))

plt.figure(figsize=(10, 5))
plot_importance(xgb_model)

top_10_features = [
    "OPERA_Latin American Wings",
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]
n_y0 = len(y_train[y_train == 0])
n_y1 = len(y_train[y_train == 1])
scale = n_y0/n_y1
print(scale)

x_train2, x_test2, y_train2, y_test2 = train_test_split(
    features[top_10_features], target, test_size=0.33, random_state=42)

xgb_model_2 = xgb.XGBClassifier(
    random_state=1, learning_rate=0.01, scale_pos_weight=4.6)
xgb_model_2.fit(x_train2, y_train2)

xgboost_y_preds_2 = xgb_model_2.predict(x_test2)

#print(list(xgboost_y_preds_2))

confusion_matrix(y_test2, xgboost_y_preds_2)

print(classification_report(y_test2, xgboost_y_preds_2))

# class DelayModel:

#     def __init__(
#         self
#     ):
#         self._model = None  # Model should be saved in this attribute.

#     def preprocess(
#         self,
#         data: pd.DataFrame,
#         target_column: str = None
#     ) -> Union(Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
#         """
#         Prepare raw data for training or predict.

#         Args:
#             data (pd.DataFrame): raw data.
#             target_column (str, optional): if set, the target is returned.

#         Returns:
#             Tuple[pd.DataFrame, pd.DataFrame]: features and target.
#             or
#             pd.DataFrame: features.
#         """
#         return

#     def fit(
#         self,
#         features: pd.DataFrame,
#         target: pd.DataFrame
#     ) -> None:
#         """
#         Fit model with preprocessed data.

#         Args:
#             features (pd.DataFrame): preprocessed data.
#             target (pd.DataFrame): target.
#         """
#         return

#     def predict(
#         self,
#         features: pd.DataFrame
#     ) -> List[int]:
#         """
#         Predict delays for new flights.

#         Args:
#             features (pd.DataFrame): preprocessed data.
        
#         Returns:
#             (List[int]): predicted targets.
#         """
#         return
