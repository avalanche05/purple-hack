from collections import defaultdict
from datetime import datetime
import json
from copy import deepcopy

from .parser import get_data

raw_data: dict = json.load(open("исх.json"))
data = get_data()
data_lists = get_data(is_dict=False)

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


def get_output(tasks: list[dict]):
    tasks = {task["id"]: task for task in tasks}

    def change_tasks(tasks_list: list) -> (datetime, datetime):
        start_date, end_date = None, None
        for task in tasks_list:
            if 'children' in task:
                cur_start, cur_end = change_tasks(task["children"])
                task["startDate"] = cur_start.strftime("%Y-%m-%dT%H:%M:%S")
                task["endDate"] = cur_end.strftime("%Y-%m-%dT%H:%M:%S")
                task["duration"] = (cur_start - cur_end).days
                if start_date is None:
                    start_date = cur_start
                if end_date is None:
                    end_date = cur_end
                start_date = min(start_date, cur_start)
                end_date = max(end_date, cur_end)
            else:
                new_task = tasks[task["id"]]
                if start_date is None:
                    start_date = new_task["start_date"]
                if end_date is None:
                    end_date = new_task["end_date"]
                start_date = min(start_date, new_task["start_date"])
                end_date = max(end_date, new_task["end_date"])
                task.update(
                    {
                        "startDate": new_task["start_date"].strftime("%Y-%m-%dT%H:%M:%S"),
                        "endDate": new_task["end_date"].strftime("%Y-%m-%dT%H:%M:%S"),
                        "duration": new_task["duration"],
                    }
                )

        return start_date, end_date

    result = deepcopy(raw_data)

    change_tasks(result["tasks"]["rows"])

    assignments = []

    for task in tasks.values():
        assignments.append(
            {
                "event": task["id"],
                "resource": task["resource_id"],
                "units": 100,
                "startDate": task["start_date"].strftime("%Y-%m-%dT%H:%M:%S"),
                "endDate": task["end_date"].strftime("%Y-%m-%dT%H:%M:%S"),
                "currentEffort": 144000000,
                "guid": "d6f73a0f-4d88-45cf-9d14-e0878bd0f466",
                "id": "7335019676944236545"
            }
        )

    result["assignments"]["rows"] = assignments

    return result
