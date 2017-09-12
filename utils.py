import os
from datetime import timedelta


def is_working_day(day):
    return day.weekday() < 5


def day_generator(fromdate, todate):
    return (fromdate + timedelta(x) for x in range((todate - fromdate).days))


def get_working_days(*args):
    days = day_generator(*args)
    working_days = (day for day in days if day.weekday() < 5)
    return working_days


def get_working_days_amount(*args):
    working_days = get_working_days(*args)
    res = sum(1 for day in working_days)
    return res


def remove_empty_sub_dirs(dir_path):
    sub_dirs = os.listdir(dir_path)
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(dir_path, sub_dir)
        not os.listdir(sub_dir_path) and os.rmdir(sub_dir_path)
