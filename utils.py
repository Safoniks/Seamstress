import os
from datetime import timedelta


def is_working_day(day):
    return day.weekday() < 5


def get_working_days(fromdate, todate):
    daygenerator = (fromdate + timedelta(x) for x in range((todate - fromdate).days + 1))
    res = sum(1 for day in daygenerator if day.weekday() < 5)
    return res


def remove_empty_sub_dirs(dir_path):
    sub_dirs = os.listdir(dir_path)
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(dir_path, sub_dir)
        not os.listdir(sub_dir_path) and os.rmdir(sub_dir_path)
