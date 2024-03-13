import json
from collections import defaultdict
from datetime import datetime
from typing import Any
from copy import deepcopy


def get_price_from_name(name: str) -> float:
    res = ""
    for i in range(name.rfind("(") + 1, len(name)):
        if name[i].isdigit() or name[i] == ".":
            res += name[i]
        else:
            break

    if res.strip().replace(".", "").isdigit():
        return float(res)
    else:
        return 2000


def get_tasks(data: list) -> list:
    result = []
    for task in data:
        if 'children' in task:
            result.extend(get_tasks(task['children']))
        else:
            result.append(task)
    return result


task_tree = defaultdict(list)


def get_leaf(node_id):
    if not task_tree[node_id]:
        return node_id
    return get_leaf(task_tree[node_id][0])


def get_data(d, is_dict=True) -> dict | list:
    tasks = dict()
    users = dict()
    dependencies = dict()

    data = deepcopy(d)
    for task in get_tasks(data["tasks"]["rows"]):
        tasks[task["id"]] = {
            "id": task["id"],
            "effort": task["effort"],
            "project_role_id": None,
        }

    for user in data["resources"]["rows"]:
        price = get_price_from_name(user["name"])
        users[user["id"]] = {
            "id": user["id"],
            "price": price,
            "project_role_id": user.get("projectRoleId", "-"),
            "hours": 8,
        }

    for assignment in data["assignments"]["rows"]:
        task_id = assignment["event"]
        user_id = assignment["resource"]
        project_role_id = users[user_id]["project_role_id"]
        tasks[task_id]["project_role_id"] = project_role_id

    for dependency in data["dependencies"]["rows"]:
        dependencies[dependency["id"]] = {
            "id": dependency["id"],
            "from": dependency["from"],
            "to": dependency["to"],
        }

    start_date = datetime.strptime(data["project"]["startDate"], "%Y-%m-%d")
    var1 = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "resources": users,
        "tasks": tasks,
        "dependencies": dependencies,
    }

    var2 = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "resources": list(users.values()),
        "tasks": list(tasks.values()),
        "dependencies": list(dependencies.values()),
    }

    if is_dict:
        return var1
    else:
        return var2
