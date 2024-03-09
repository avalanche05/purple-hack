from .common import data, calendar
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


def get_user_hour(user_id: str, date: str):
    return calendar[user_id][date]


def assign_time(tasks: list):
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    step = timedelta(days=1)
    user_time = defaultdict(lambda: start_date)

