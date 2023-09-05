from xgboost import plot_importance
import xgboost as xgb
from challenge.Utils.GetPeriodDayFunction import get_period_day
from challenge.Utils.IsHighSeasionFunction import is_high_season
from challenge.Utils.GetMinDiffFunction import get_min_diff
from typing import Tuple, List
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
warnings.filterwarnings('ignore')

class DelayModel:

    def __init__(
        self
    ):
        # Model should be saved in this attribute.
        self._model = xgb.XGBClassifier(
            random_state=1, learning_rate=0.01, scale_pos_weight=5)

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> (Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
        
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

        # OK
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        # OK
        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        # OK
        data['min_diff'] = data.apply(get_min_diff, axis=1)
        threshold_in_minutes = 15
        # OK
        data['delay'] = np.where(
        data['min_diff'] > threshold_in_minutes, 1, 0)

        training_data = shuffle(
            data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state=111)


        features = pd.concat([
            pd.get_dummies(training_data['OPERA'], prefix='OPERA'),
            pd.get_dummies(training_data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(training_data['MES'], prefix='MES')],
            axis=1
        )
        if target_column:
            target = data[[target_column]]
        else:
            target = data[["delay"]]
        
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
        if target_column:
            return features[top_10_features],target
        else :
            x_train2, x_test2, y_train2, y_test2 = train_test_split(
                features[top_10_features], target, test_size=0.33, random_state=42)
            # xgb_model_2 = xgb.XGBClassifier(
            # random_state=1, learning_rate=0.01, scale_pos_weight=4.6)
            self._model.fit(x_train2, y_train2)
            return features[top_10_features]

   


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
        self._model.fit(features,target)
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

        xgboost_y_preds = self._model.predict(features)
        xgboost_y_preds = [1 if y_pred > 0.5 else 0 for y_pred in xgboost_y_preds]
        return xgboost_y_preds

    def preprocessApi(
            self,
            data: pd.DataFrame,
            target_column: str = None
        ) -> (Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
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

        # OK
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        # OK
        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        # OK
        data['min_diff'] = data.apply(get_min_diff, axis=1)
        threshold_in_minutes = 15
        # OK
        data['delay'] = np.where(
            data['min_diff'] > threshold_in_minutes, 1, 0)

        training_data = shuffle(
            data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state=111)

        features = pd.concat([
            pd.get_dummies(training_data['OPERA'], prefix='OPERA'),
            pd.get_dummies(training_data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(training_data['MES'], prefix='MES')],
            axis=1
        )
        if target_column:
            target = data[[target_column]]
        else:
            target = data[["delay"]]
        if target_column:
            return features, target
        else:
            x_train2, x_test2, y_train2, y_test2 = train_test_split(
                features, target, test_size=0.33, random_state=42)
            # xgb_model_2 = xgb.XGBClassifier(
            # random_state=1, learning_rate=0.01, scale_pos_weight=4.6)
            self._model.fit(x_train2, y_train2)
            return features
