from typing import Dict, List, Any
import random


def create_project_role_ids(data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """For each project_role create a list of tasks_ids with this project_role"""

    tasks_by_project_roles: Dict[str, List[str]] = {}
    for task in data.get("tasks"):
        project_role = task.get("project_role_id")
        if project_role not in tasks_by_project_roles:
            tasks_by_project_roles[project_role] = [task.get("id")]
        else:
            tasks_by_project_roles[project_role].append(task.get("id"))

    return tasks_by_project_roles


def match_task_id_to_resourse_id(data: Dict[str, List[Dict[str, Any]]],
                                 tasks_by_project_roles: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Randomly assign resourse_id to each task_id based on project_role"""

    for project_role_id, project_role_id_list in tasks_by_project_roles.items():
        random.shuffle(project_role_id_list)

    last_ids = dict(zip(tasks_by_project_roles.keys(), [0] * len(tasks_by_project_roles)))
    tasks_to_resourses = {}

    for task in data.get("tasks"):
        project_role_id = task.get("project_role_id")
        last_id = last_ids.get(project_role_id)
        tasks_to_resourses[task["id"]] = tasks_by_project_roles[last_id]
        if last_id == len(tasks_by_project_roles.get(project_role_id)):
            random.shuffle(tasks_by_project_roles[project_role_id])
            last_ids["project_role_id"] = 0

    return tasks_to_resourses

