from datetime import datetime


def format_date(date):
    if len(date) == 4:
        return datetime.strptime(date, '%Y').date().replace(month=1, day=1)
    return datetime.strptime(date, '%Y-%m-%d').date()


