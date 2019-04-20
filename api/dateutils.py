import datetime
import holidays


def is_holiday(date):
    italian_holidays = holidays.Italy(years=date.year)
    return date in italian_holidays


def is_weekend(date):
    return date.weekday() in (5, 6)


def check_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)


def convert_timestamp(ts):
    if check_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts / 1000)
    else:
        return 'N/A'


def format_timestamp(ts, fmt="%H:%M:%S"):
    return convert_timestamp(ts).strftime(fmt)
