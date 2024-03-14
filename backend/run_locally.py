from copy import deepcopy
from pprint import pprint

from backend.app.utils.calculate import process_json
import json
from datetime import datetime

duration = 1
price = 0
resource = 0


def get_start_end(task_id: str, tasks: list):
    for task in tasks:
        if task["id"].strip() == task_id.strip():
            return datetime.strptime(task["startDate"], "%Y-%m-%dT%H:%M:%S"), datetime.strptime(task["endDate"],
                                                                                                "%Y-%m-%dT%H:%M:%S")
        if "children" in task:
            r = get_start_end(task_id, task["children"])
            if r is not None:
                return r


def check_dependencies(dependencies, tasks):
    checks = []
    for dependency in dependencies:
        from_start, from_end = get_start_end(dependency["from"], tasks)
        to_start, to_end = get_start_end(dependency["to"], tasks)

        if from_end > to_start:
            checks.append(dependency)
    return checks

with open("проверочное задание.json") as input_file:
    inp_data = json.load(input_file)
    final_res = process_json(deepcopy(inp_data), duration, price, resource)

    checks = check_dependencies(final_res["dependencies"]["rows"], final_res["tasks"]["rows"])
    count = 0
    while len(checks) > 0 and count < 5:
        print("COUNT", len(checks))
        pprint(checks)
        res = process_json(deepcopy(inp_data), duration, price, resource)
        new_checks = check_dependencies(res["dependencies"]["rows"], res["tasks"]["rows"])

        if len(new_checks) < len(checks):
            checks = new_checks
            final_res = res
        count += 1
    with open("result.json", "w") as output_file:
        json.dump(res, output_file)
