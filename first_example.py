from datetime import datetime as dt
from datetime import timedelta

def fetch_dates(start_date, total_days):
    total_dates = []
    for day in range(1, total_days+1):
        date = dt.strptime(start_date, '%d-%m-%Y') + timedelta(days=day)
        total_dates.append(date.strftime('%d-%m-%Y'))
        
    return total_dates

date = input("Enter the starting date: ")
total_days = int(input("Enter the days to be added: "))
total_dates = fetch_dates(date, total_days)
print(total_dates)
