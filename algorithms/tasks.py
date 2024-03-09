from .common import data, calendar
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


def get_user_hour(user_id: str, date: str):
    return calendar[user_id][date]


def assign_time(task_ids: list, task_user: dict) -> list[dict]:
    res = []
    init_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
    step = timedelta(days=1)
    user_time = defaultdict(lambda: init_date)

    for task_id in task_ids:
        task: dict = data["tasks"][task_id]
        effort_time = task["effort"]
        user_id = task_user[task_id]
        start_date = user_time[user_id]
        duration = 0
        while effort_time > 0:
            hours = get_user_hour(task_id, user_time[user_id].strftime("%Y-%m-%d"))
            effort_time -= hours
            if hours:
                duration += 1
            user_time[user_id] += step
        end_date = user_time[user_id]
        task.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "resource_id": user_id,
                "resource_price": data["resources"][user_id]["price"],
                "duration": duration,
            }
        )
        res.append(task)
    return res
