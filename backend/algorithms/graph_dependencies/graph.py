def create_graph(dependencies, is_task) -> dict:
    graph = {}
    for edge in dependencies:
        from_id = edge.get("from")
        if from_id not in graph:  # check if is_task
            graph[from_id] = [edge.get("to")]
        else:
            graph[from_id].append(edge.get("to"))

    return graph


def get_roots(blockers, dependencies, is_task) -> list:
    roots = set(blockers.keys())  # check if task
    for edge in dependencies:
        to_id = edge.get("to")
        if to_id in roots:
            roots.remove(to_id)

    return list(roots)
<<<<<<< HEAD


def get_leaves(graph, dependencies, is_task) -> list:
    leaves = set(graph.keys())  #add checker if is_task
    for edge in dependencies:
        from_id = edge.get("from")
        if from_id in leaves:
            leaves.remove(from_id)

    return list(leaves)


def get_roots_and_leaves_by_project(project_gr, project_id):
    #  по id проекта получить ребенка
    roots = []
    leaves = []
    for task in task_tree[project_id]:
        if

def projects_tree_dfs(project_id, project_gr, is_root, is_leaf):
    #  param in: data
    if len(project_gr) == 0:
        return
    for project in project_gr[project_id]:
        pass


def projects_tree_dp(project_gr, is_root, is_leaf):
    #  param in: data
=======
>>>>>>> e6edbf16e77feb8c6650122344f233ab770a73e5
