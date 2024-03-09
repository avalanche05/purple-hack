from datetime import timedelta, datetime
from typing import Callable, Union, List, Dict, Any
from .common import data
import pprint

Number = Union[float, int]


def count_working_days(start_date: datetime, end_date: datetime) -> int:
    current_date = start_date
    working_days = 0

    while current_date <= end_date:
        if current_date.weekday() < 5:
            working_days += 1
        current_date += timedelta(days=1)

    return working_days


def cost_len_fn(infos: List[Dict[str, Any]]) -> int:
    total_cost = 0
    start_date = infos[0].get("start_date")
    end_date = infos[0].get("end_date")

    for info in infos:
        start_date = min(start_date, info.get("start_date"))
        end_date = max(end_date, info.get("end_date"))

    return (end_date - start_date).days


def cost_resource_fn(infos: List[Dict[str, Any]]) -> int:
    resourses = set()

    for info in infos:
        resourses.add(info["resource_id"])

    return len(resourses)


def cost_fn(infos: List[Dict[str, Any]]) -> Number:
    total_cost = 0

    for task in infos:
        resource_id = task["resource_id"]
        total_cost += task["effort"] * data["resources"][resource_id]["price"]

    return total_cost


def combined_cost_fn(fn1: Callable[[List[Dict[str, Any]]], int],
                     fn2: Callable[[List[Dict[str, Any]]], int],
                     fn3: Callable[[List[Dict[str, Any]]], int]) -> Callable[[List[Dict[str, Any]]], int]:
    def _fn(infos: List[Dict[str, Any]]) -> int:
        return 0.5 * fn1(infos) + 0.3 * fn2(infos) + 0.2 * fn3(infos)

    return _fn
