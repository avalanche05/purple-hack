import json
from .tasks import assign_time
from .graph_dependencies.topological_sort import top_sort


def get_base_data(is_dict=True) -> dict | list:
    task_ids = []
    task_user = {}
    with open("исх.json") as file_input:
        data = json.load(file_input)
        assignments = data.get("assignments", {}).get("rows", [])
        for assignment in assignments:
            task_user[assignment.get("event")] = assignment.get("resource")
            task_ids.append((assignment.get("startDate"), assignment.get("event")))

    base_assign_time = assign_time([task_id[1] for task_id in sorted(task_ids)], task_user, top_sort.graph)
    return base_assign_time
