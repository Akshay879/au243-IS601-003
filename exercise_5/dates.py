from datetime import datetime, timedelta, date

def my_datetime(dt):
    return dt.strftime("%Y %m %d %H %M %S")

def saturdays():
    today = date.today()
    next_year = date(today.year + 1, 1, 1)
    days_until_saturday = (5 - today.weekday()) % 7 
    first_saturday = today + timedelta(days=days_until_saturday)
    saturdays_list = []
    current_saturday = first_saturday
    while current_saturday < next_year:
        saturdays_list.append(current_saturday)
        current_saturday += timedelta(weeks=1)

    return saturdays_list

def first_or_fifteenth(given_date):
    if given_date.day in [1, 15] and given_date.weekday() not in [5, 6]:
        return True
    return False