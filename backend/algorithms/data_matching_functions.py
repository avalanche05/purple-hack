from typing import Dict, List, Any
import random

from .common import data as common_data


def create_project_role_ids(resources: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """For each project_role create a list of resourse_ids with this project_role"""

    resources_by_project_roles: Dict[str, List[str]] = {}
    for resource in resources:
        project_role = resource.get("project_role_id")
        if project_role not in resources_by_project_roles:
            resources_by_project_roles[project_role] = [resource.get("id")]
        else:
            resources_by_project_roles[project_role].append(resource.get("id"))

    return resources_by_project_roles


def match_task_id_to_resourse_id(data: Dict[str, List[Dict[str, Any]]],
                                 resources_by_project_roles: Dict[str, List[str]], optimize_type="time") -> Dict[
    str, str]:
    """Randomly assign resourse_id to each task_id based on project_role"""

    for project_role_id, project_role_id_list in resources_by_project_roles.items():
        if optimize_type == "price":
            min_price = min(
                t["price"] for t in common_data["resources"].values() if t["project_role_id"] == project_role_id)
            project_role_id_list = list(
                filter(lambda x: common_data["resources"][x]["price"] == min_price, project_role_id_list))
        if optimize_type == "resource":
            min_price = min(
                t["price"] for t in common_data["resources"].values() if t["project_role_id"] == project_role_id)
            project_role_id_list = list(
                filter(lambda x: common_data["resources"][x]["price"] == min_price, project_role_id_list))[:1]
        random.shuffle(project_role_id_list)
        resources_by_project_roles[project_role_id] = project_role_id_list

    last_ids = dict(zip(resources_by_project_roles.keys(), [0] * len(resources_by_project_roles)))
    tasks_to_resources = {}

    for task in data.get("tasks"):
        project_role_id = task.get("project_role_id")
        last_id = last_ids.get(project_role_id)
        # print(resources_by_project_roles)
        tasks_to_resources[task.get("id")] = resources_by_project_roles[project_role_id][last_id]
        last_ids[project_role_id] += 1

        if last_ids[project_role_id] == len(resources_by_project_roles.get(project_role_id)):
            random.shuffle(resources_by_project_roles[project_role_id])
            last_ids[project_role_id] = 0
    return tasks_to_resources