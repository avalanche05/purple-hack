def create_graph(dependencies, is_task) -> dict:
    graph = {}
    for edge in dependencies:
        to_id = edge.get("to")
        from_id = edge.get("from")
        if is_task.get(from_id) and is_task.get(to_id):
            if from_id not in graph:
                graph[from_id] = [to_id]
            else:
                graph[from_id].append(to_id)

    return graph


def get_tasks(is_task) -> set:
    tasks = set()
    for task_id, is_task_flag in is_task.items():
        if is_task_flag:
            tasks.add(task_id)

    return tasks


def get_all_roots(dependencies, is_task) -> set:
    roots = get_tasks(is_task)
    for edge in dependencies:
        to_id = edge.get("to")
        if to_id in roots:
            roots.remove(to_id)

    return roots


def get_all_leaves(dependencies, is_task) -> set:
    leaves = get_tasks(is_task)
    for edge in dependencies:
        from_id = edge.get("from")
        if from_id in leaves:
            leaves.remove(from_id)

    return leaves


def create_roots_leaves_graph(task_tree, is_task, roots, leaves):
    #  по id проекта получить ребенка
    roots = {}
    leaves = {}
    for project_id, task_list in task_tree:
        for task_id in task_list:
            if is_task.get(task_id):
                if task_id in roots:
                    if project_id not in roots:
                        roots[project_id] = [task_id]
                    else:
                        roots[project_id].append(task_id)
                if task_id in leaves:
                    if project_id not in roots:
                        leaves[project_id] = [task_id]
                    else:
                        leaves[project_id].append(task_id)

    return roots, leaves


def projects_tree_dfs(project_id, project_gr, is_root, is_leaf):
    #  param in: data
    if len(project_gr) == 0:
        return
    for project in project_gr[project_id]:
        pass


def projects_tree_dp(project_gr, is_root, is_leaf):
    #  param in: data
    pass
