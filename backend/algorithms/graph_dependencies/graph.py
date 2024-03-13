def create_graph(dependencies) -> dict:
    graph = {}
    for edge in dependencies:
        from_id = edge.get("from")
        if from_id not in graph:
            graph[from_id] = [edge.get("to")]
        else:
            graph[from_id].append(edge.get("to"))

    return graph


def get_roots(gr, dependencies) -> list:
    roots = set(gr.keys())
    for edge in dependencies:
        to_id = edge.get("to")
        if to_id in roots:
            roots.remove(to_id)

    return list(roots)
