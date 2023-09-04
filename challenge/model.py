from GetPeriodDayFunction import get_period_day
import pandas as pd
from typing import Tuple, Union, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
warnings.filterwarnings('ignore')


#data = pd.read_csv('../data/dataAux.csv')
data = pd.read_csv('../data/data.csv')
#data.info()

# Numeros de vuelos por aerolinea.
# flights_by_airline = data['OPERA'].value_counts()
# plt.figure(figsize=(10, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=flights_by_airline.index, y=flights_by_airline.values, alpha=0.9)
# plt.title('Flights by Airline')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Airline', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()

# Numero de vuelos por dia.
# flights_by_day = data['DIA'].value_counts()
# plt.figure(figsize=(10, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=flights_by_day.index, y=flights_by_day.values,
#             color='lightblue', alpha=0.8)
# plt.title('Flights by Day')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Day', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()

# Numero de vuelos por mes 
# |`MES`|Número del mes de operación del vuelo.|
# flights_by_month = data['MES'].value_counts()
# plt.figure(figsize=(10, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=flights_by_month.index, y=flights_by_month.values,
#             color='lightblue', alpha=0.8)
# plt.title('Flights by Month')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Month', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()

# Vuelos por dia de la semana
# flights_by_day_in_week = data['DIANOM'].value_counts()
# days = [
#     flights_by_day_in_week.index[2],
#     flights_by_day_in_week.index[5],
#     flights_by_day_in_week.index[4],
#     flights_by_day_in_week.index[1],
#     flights_by_day_in_week.index[0],
#     flights_by_day_in_week.index[6],
#     flights_by_day_in_week.index[3]
# ]
# values_by_day = [
#     flights_by_day_in_week.values[2],
#     flights_by_day_in_week.values[5],
#     flights_by_day_in_week.values[4],
#     flights_by_day_in_week.values[1],
#     flights_by_day_in_week.values[0],
#     flights_by_day_in_week.values[6],
#     flights_by_day_in_week.values[3]
# ]
# plt.figure(figsize=(10, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=days, y=values_by_day, color='lightblue', alpha=0.8)
# plt.title('Flights by Day in Week')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Day in Week', fontsize=12)
# plt.xticks(rotation=90)
# plt.show()

# Vuelos por tipo internacional o nacional
# flights_by_type = data['TIPOVUELO'].value_counts()
# sns.set(style="darkgrid")
# plt.figure(figsize=(10, 2))
# sns.barplot(x=flights_by_type.index, y=flights_by_type.values, alpha=0.9)
# plt.title('Flights by Type')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Type', fontsize=12)
# plt.show()

# Vuelos por cuidad de destino
# flight_by_destination = data['SIGLADES'].value_counts()
# plt.figure(figsize=(10, 2))
# sns.set(style="darkgrid")
# sns.barplot(x=flight_by_destination.index,
#             y=flight_by_destination.values, color='lightblue', alpha=0.8)
# plt.title('Flight by Destination')
# plt.ylabel('Flights', fontsize=12)
# plt.xlabel('Destination', fontsize=12)
# plt.xticks(rotation=90)

# plt.show()

#OK



data['period_day'] = data['Fecha-I'].apply(get_period_day)

#OK
def is_high_season(fecha):
    fecha_año = int(fecha.split('-')[0])
    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    range1_min = datetime.strptime(
        '15-Dec', '%d-%b').replace(year=fecha_año, hour=00, minute=00, second=00)
    range1_max = datetime.strptime(
        '31-Dec', '%d-%b').replace(year=fecha_año, hour=23, minute=59, second=59)
    range2_min = datetime.strptime(
        '1-Jan', '%d-%b').replace(year=fecha_año, hour=00, minute=00, second=00)
    range2_max = datetime.strptime(
        '3-Mar', '%d-%b').replace(year=fecha_año, hour=23, minute=59, second=59)
    range3_min = datetime.strptime(
        '15-Jul', '%d-%b').replace(year=fecha_año, hour=00, minute=00, second=00)
    range3_max = datetime.strptime(
        '31-Jul', '%d-%b').replace(year=fecha_año, hour=23, minute=59, second=59)
    range4_min = datetime.strptime(
        '11-Sep', '%d-%b').replace(year=fecha_año, hour=00, minute=00, second=00)
    range4_max = datetime.strptime(
        '30-Sep', '%d-%b').replace(year=fecha_año, hour=23, minute=59, second=59)

    if ((fecha >= range1_min and fecha <= range1_max) or
        (fecha >= range2_min and fecha <= range2_max) or
        (fecha >= range3_min and fecha <= range3_max) or
            (fecha >= range4_min and fecha <= range4_max)):
        return 1
    else:
        return 0  

data['high_season'] = data['Fecha-I'].apply(is_high_season)
#OK
def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return np.round(min_diff,2)


data['min_diff'] = data.apply(get_min_diff, axis=1)
threshold_in_minutes = 15
#OK
data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)



def get_rate_from_column(data, column):
    delays = {}
    for _, row in data.iterrows():
        if row['delay'] == 1:
            if row[column] not in delays:
                delays[row[column]] = 1
            else:
                delays[row[column]] += 1
    total = data[column].value_counts().to_dict()

    rates = {}
    for name, total in total.items():
        if name in delays:
            rates[name] = round(delays[name] / total, 2)
        else:
            rates[name] = 0

    return pd.DataFrame.from_dict(data=rates, orient='index', columns=['Tasa (%)'])


# destination_rate = get_rate_from_column(data, 'SIGLADES')
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


# class DelayModel:

#     def __init__(
#         self
#     ):
#         self._model = None # Model should be saved in this attribute.

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