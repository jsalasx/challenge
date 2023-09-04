from xgboost import plot_importance
import xgboost as xgb
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
data = pd.read_csv('../data/data.csv')
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


#destination_rate = get_rate_from_column(data, 'SIGLADES')
# destination_rate_values = data['SIGLADES'].value_counts().index
# plt.figure(figsize=(20, 5))
# sns.set(style="darkgrid")
# sns.barplot(x=destination_rate_values, y=destination_rate['Tasa (%)'], alpha=0.75)
# plt.title('Delay Rate by Destination')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Destination', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()

# airlines_rate = get_rate_from_column(data, 'OPERA')
# airlines_rate_values = data['OPERA'].value_counts().index
# plt.figure(figsize=(20, 5))
# sns.set(style="darkgrid")
# sns.barplot(x=airlines_rate_values, y=airlines_rate['Tasa (%)'], alpha=0.75)
# for index, value in enumerate(airlines_rate['Tasa (%)']):
#     # puedes ajustar el + 0.01 según tus preferencias
#     plt.text(index, value + 0.01, str(value), ha='center', va='bottom')
# plt.title('Delay Rate by Airline')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Airline', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()


# month_rate = get_rate_from_column(data, 'MES')
# month_rate_value = data['MES'].value_counts().index
# plt.figure(figsize=(20, 5))
# sns.set(style="darkgrid")
# sns.barplot(x=month_rate_value, y=month_rate['Tasa (%)'], color='blue', alpha=0.75)
# plt.title('Delay Rate by Month')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Month', fontsize=12)
# plt.xticks(rotation=90)
# plt.ylim(0, 10)
# plt.show()


# days_rate = get_rate_from_column(data, 'DIANOM')
# days_rate_value = data['DIANOM'].value_counts().index

# sns.set(style="darkgrid")
# plt.figure(figsize=(20, 5))
# sns.barplot(x=days_rate_value, y=days_rate['Tasa (%)'], color='blue', alpha=0.75)
# for index, value in enumerate(days_rate['Tasa (%)']):
#     # puedes ajustar el + 0.01 según tus preferencias
#     plt.text(index, value + 0.01, str(value), ha='center', va='bottom')
# plt.title('Delay Rate by Day')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Days', fontsize=12)
# plt.xticks(rotation=90)
# plt.ylim(0, 1)
# plt.show()

# high_season_rate = get_rate_from_column(data, 'high_season')
# high_season_rate_values = data['high_season'].value_counts().index

# plt.figure(figsize=(5, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=["no", "yes"], y=high_season_rate['Tasa (%)'])
# plt.title('Delay Rate by Season')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('High Season', fontsize=12)
# plt.xticks(rotation=90)
# plt.ylim(0, 1)
# plt.show()

# flight_type_rate = get_rate_from_column(data, 'TIPOVUELO')
# flight_type_rate_values = data['TIPOVUELO'].value_counts().index
# plt.figure(figsize=(5, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=flight_type_rate_values, y=flight_type_rate['Tasa (%)'])
# plt.title('Delay Rate by Flight Type')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Flight Type', fontsize=12)
# plt.ylim(0, 1)
# plt.show()


# period_day_rate = get_rate_from_column(data, 'period_day')
# period_day_rate_values = data['period_day'].value_counts().index
# plt.figure(figsize=(5, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=period_day_rate_values, y=period_day_rate['Tasa (%)'])
# plt.title('Delay Rate by Period of Day')
# plt.ylabel('Delay Rate [%]', fontsize=12)
# plt.xlabel('Period', fontsize=12)
# plt.ylim(0, 0.5)
# plt.show()


training_data = shuffle(
    data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state=111)

features = pd.concat([
    pd.get_dummies(data['OPERA'], prefix='OPERA'),
    pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
    pd.get_dummies(data['MES'], prefix='MES')],
    axis=1
)
target = data['delay']

x_train, x_test, y_train, y_test = train_test_split(
    features, target, test_size=0.33, random_state=42)

print(f"train shape: {x_train.shape} | test shape: {x_test.shape}")

y_train.value_counts('%')*100
y_test.value_counts('%')*100

xgb_model = xgb.XGBClassifier(random_state=1, learning_rate=0.01)
xgb_model.fit(x_train, y_train)

xgboost_y_preds = xgb_model.predict(x_test)
xgboost_y_preds = [1 if y_pred > 0.5 else 0 for y_pred in xgboost_y_preds]

confusion_matrix(y_test, xgboost_y_preds)
print(classification_report(y_test, xgboost_y_preds))


class DelayModel:

    def __init__(
        self
    ):
        self._model = None  # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union(Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        return

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return
