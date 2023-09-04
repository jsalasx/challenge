from xgboost import plot_importance
import xgboost as xgb
from challenge.Utils.GetPeriodDayFunction import get_period_day
from challenge.Utils.IsHighSeasionFunction import is_high_season
from challenge.Utils.GetMinDiffFunction import get_min_diff
from challenge.Utils.GetRateFromColumnFunction import get_rate_from_column
from typing import Tuple, Union, List
import pandas as pd
import numpy as np
import warnings
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
warnings.filterwarnings('ignore')


class DelayModel:

    def __init__(
        self
    ):
        # Model should be saved in this attribute.
        self._model = xgb.XGBClassifier()

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
            return features, data[[target_column]]
        else:
            return features

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

        
        #confusion_matrix(y_test, xgboost_y_preds)
        #print(classification_report(y_test, xgboost_y_preds))
        return list(self._model.predict(features))
