from datetime import datetime
def get_period_day(date):
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
    morning_min = datetime.strptime("05:00:00", '%H:%M:%S').time()
    morning_max = datetime.strptime("11:59:59", '%H:%M:%S').time()
    afternoon_min = datetime.strptime("12:00:00", '%H:%M:%S').time()
    afternoon_max = datetime.strptime("18:59:59", '%H:%M:%S').time()
    evening_min = datetime.strptime("19:00:00", '%H:%M:%S').time()
    evening_max = datetime.strptime("23:59:59", '%H:%M:%S').time()
    night_min = datetime.strptime("00:00:00", '%H:%M:%S').time()
    night_max = datetime.strptime("4:59:59", '%H:%M:%S').time()

    if (date_time >= morning_min and date_time <= morning_max):
        return 'mañana'
    elif (date_time >= afternoon_min and date_time <= afternoon_max):
        return 'tarde'
    elif (
        (date_time >= evening_min and date_time <= evening_max) or
        (date_time >= night_min and date_time <= night_max)
    ):
        return 'noche'
