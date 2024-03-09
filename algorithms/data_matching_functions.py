import random


def create_project_role_ids(data) -> dict:
    tasks_by_project_roles = {}
    for task in data.get("tasks"):
        project_role = task.get("project_role_id")
        if project_role not in tasks_by_project_roles:
            tasks_by_project_roles[project_role] = [task.get("id")]
        else:
            tasks_by_project_roles[project_role].append(task.get("id"))

    return tasks_by_project_roles


def match_task_id_to_resourse_id(data, tasks_by_project_roles):
    for project_role_id, project_role_id_list in tasks_by_project_roles.items():
        random.shuffle(project_role_id_list)

    last_ids = dict(zip(tasks_by_project_roles.keys(), [0] * len(tasks_by_project_roles)))
    tasks_to_resourses = {}  # {"task_id": "resourse_id"}

    for task in data.get("tasks"):
        project_role_id = task.get("project_role_id")
        last_id = last_ids.get(project_role_id)
        tasks_to_resourses[task["id"]] = tasks_by_project_roles[last_id]
        if last_id == len(tasks_by_project_roles.get(project_role_id)):
            random.shuffle(tasks_by_project_roles[project_role_id])
            last_ids["project_role_id"] = 0

    return tasks_to_resourses

