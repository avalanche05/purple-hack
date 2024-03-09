import json
import re
from datetime import datetime
from pprint import pprint


def get_price_from_name(name: str) -> float:
    res = ""
    for i in range(name.rfind("(") + 1, len(name)):
        if name[i].isdigit() or name[i] == ".":
            res += name[i]
        else:
            break

    return float(res)


def get_tasks(data: list) -> list:
    result = []
    for task in data:
        if 'children' in task:
            result.extend(get_tasks(task['children']))
        else:
            result.append(task)
    return result


def main():
    tasks = dict()
    users = dict()
    dependencies = dict()

    with open("исх.json") as file_input:
        data = json.load(file_input)
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
                "project_role_id": user["projectRoleId"],
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

        with open("var1.json", "w") as var1_file:
            json.dump(var1, var1_file)
        with open("var2.json", "w") as var2_file:
            json.dump(var2, var2_file)


if __name__ == '__main__':
    main()
