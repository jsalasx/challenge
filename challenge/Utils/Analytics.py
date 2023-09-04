import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
from sklearn.metrics import confusion_matrix, classification_report
warnings.filterwarnings('ignore')
# Numeros de vuelos por aerolinea.


def flightsByAirLine(data: pd.DataFrame, airLine):
    flights_by_airline = data['OPERA'].value_counts()
    return flights_by_airline[airLine]
    # plt.figure(figsize=(10, 2))
    # sns.set(style="darkgrid")
    # sns.barplot(x=flights_by_airline.index, y=flights_by_airline.values, alpha=0.9)
    # plt.title('Flights by Airline')
    # plt.ylabel('Flights', fontsize=12)
    # plt.xlabel('Airline', fontsize=12)
    # plt.xticks(rotation=90)
    # plt.show()

#Numero de vuelos por dia.


def FlightsByDay(data: pd.DataFrame):
    flights_by_day = data['DIA'].value_counts()
    plt.figure(figsize=(10, 2))
    sns.set(style="darkgrid")
    sns.barplot(x=flights_by_day.index, y=flights_by_day.values,
                color='lightblue', alpha=0.8)
    plt.title('Flights by Day')
    plt.ylabel('Flights', fontsize=12)
    plt.xlabel('Day', fontsize=12)
    plt.xticks(rotation=90)
    plt.show()


def FlightsByMonth(data: pd.DataFrame):
# Numero de vuelos por mes
# |`MES`|Número del mes de operación del vuelo.|
    flights_by_month = data['MES'].value_counts()
    plt.figure(figsize=(10, 2))
    sns.set(style="darkgrid")
    sns.barplot(x=flights_by_month.index, y=flights_by_month.values,
                color='lightblue', alpha=0.8)
    plt.title('Flights by Month')
    plt.ylabel('Flights', fontsize=12)
    plt.xlabel('Month', fontsize=12)
    plt.xticks(rotation=90)
    plt.show()

def FlightsByDayInWeek(data: pd.DataFrame):
    #Vuelos por dia de la semana
    flights_by_day_in_week = data['DIANOM'].value_counts()
    days = [
        flights_by_day_in_week.index[2],
        flights_by_day_in_week.index[5],
        flights_by_day_in_week.index[4],
        flights_by_day_in_week.index[1],
        flights_by_day_in_week.index[0],
        flights_by_day_in_week.index[6],
        flights_by_day_in_week.index[3]
    ]
    values_by_day = [
        flights_by_day_in_week.values[2],
        flights_by_day_in_week.values[5],
        flights_by_day_in_week.values[4],
        flights_by_day_in_week.values[1],
        flights_by_day_in_week.values[0],
        flights_by_day_in_week.values[6],
        flights_by_day_in_week.values[3]
    ]
    plt.figure(figsize=(10, 2))
    sns.set(style="darkgrid")
    sns.barplot(x=days, y=values_by_day, color='lightblue', alpha=0.8)
    plt.title('Flights by Day in Week')
    plt.ylabel('Flights', fontsize=12)
    plt.xlabel('Day in Week', fontsize=12)
    plt.xticks(rotation=90)
    plt.show()


def FlightsByType(data: pd.DataFrame):
# Vuelos por tipo internacional o nacional
    flights_by_type = data['TIPOVUELO'].value_counts()
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 2))
    sns.barplot(x=flights_by_type.index, y=flights_by_type.values, alpha=0.9)
    plt.title('Flights by Type')
    plt.ylabel('Flights', fontsize=12)
    plt.xlabel('Type', fontsize=12)
    plt.show()

# Vuelos por cuidad de destino


def FlightsByDestination(data: pd.DataFrame):
    flight_by_destination = data['SIGLADES'].value_counts()
    plt.figure(figsize=(10, 2))
    sns.set(style="darkgrid")
    sns.barplot(x=flight_by_destination.index,
                y=flight_by_destination.values, color='lightblue', alpha=0.8)
    plt.title('Flight by Destination')
    plt.ylabel('Flights', fontsize=12)
    plt.xlabel('Destination', fontsize=12)
    plt.xticks(rotation=90)
    plt.show()
