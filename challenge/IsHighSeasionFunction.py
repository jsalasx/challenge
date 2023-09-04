from datetime import datetime
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
