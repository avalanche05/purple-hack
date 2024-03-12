encoded_tasks_example = {
    "7332181498130530308": {
        "component": 1,
        "height": 2,
        "effort_sum": 3,
    },
}


def dfs(vertex: str, par: str, comp: int, height: int, effort_sum: int, graph: dict, task_to_effort: dict) -> None:
    
    encoded_tasks_example[vertex] = {
        "component": comp,
        "height": height,
        "effort_sum": effort_sum
    }
    for to in graph.get(vertex, []):
        if to != par:
            dfs(to, vertex, comp, height + 1, effort_sum + task_to_effort.get(vertex), graph, task_to_effort)


def encode_tasks(graph: dict, task_to_effort: dict, roots: list):
    comp = 0
    for root in roots:
        dfs(root, "-1", comp, 0, task_to_effort.get(root), graph, task_to_effort)
        comp += 1