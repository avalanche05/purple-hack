from graph import create_graph, get_roots


class TopSort:
    def __init__(self, data: dict):
        self.graph = create_graph(data.get("dependencies"))
        self.roots = get_roots(self.graph, data.get("dependencies"))
        self.tin = {}
        self.tout = {}
        self.time = 0

    def dfs(self, vertex: str, par: str) -> None:
        self.tin[vertex] = self.time
        self.time += 1
        for to in self.graph.get(vertex, []):
            if to != par:
                self.dfs(to, vertex)

        self.tout[vertex] = self.time
        self.time += 1

    def top_sort(self) -> None:
        for root in self.roots:
            self.dfs(root, "-1")

    def is_parent(self, upper_vertex: str, lower_vertex: str) -> bool:
        return self.tin[upper_vertex] <= self.tin[lower_vertex] and self.tout[upper_vertex] >= self.tout[lower_vertex]
