from collections import defaultdict
from datetime import datetime
import json

from .parser import get_data

raw_data: dict = json.load(open("исх.json"))
data = get_data()
data_lists = json.load(open("var2.json"))

default_calendar = defaultdict(lambda: 8)
week_days = []
for calendar in raw_data["calendars"]["rows"]:
    if calendar["id"] == "general":
        week_days = calendar["intervals"]

for day in week_days:
    if day["startDate"] is None:
        continue
    date = datetime.strptime(day["startDate"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    if default_calendar[date] in [0, 8]:
        if day["isWorking"]:
            default_calendar[date] = 7
        else:
            default_calendar[date] = 0
calendar: dict[str, dict[str, int]] = defaultdict(lambda: default_calendar)
