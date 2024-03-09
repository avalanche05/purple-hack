from .graph import create_graph, get_roots
from ..common import data_lists


class TopSort:
    def __init__(self, data: dict):
        self.graph = create_graph(data.get("dependencies"))
        self.roots = get_roots(self.graph, data.get("dependencies"))
        self.task_sequence = []
        self.tin = {}
        self.tout = {}
        self.time = 0
        self.blokers = {}
        self.top_sort()

    def dfs(self, vertex: str, par: str) -> None:
        self.tin[vertex] = self.time
        self.time += 1
        self.task_sequence.append(vertex)

        for to in self.graph.get(vertex, []):
            if to != par:
                if to not in self.blokers:
                    self.blokers[to] = [vertex]
                else:
                    self.blokers[to].append(vertex)

                self.dfs(to, vertex)

        self.tout[vertex] = self.time
        self.time += 1

    def top_sort(self) -> None:
        for root in self.roots:
            self.dfs(root, "-1")

    def gen_sequence(self) -> list:
        return self.task_sequence

    def is_parent(self, upper_vertex: str, lower_vertex: str) -> bool:
        return self.tin[upper_vertex] <= self.tin[lower_vertex] and self.tout[upper_vertex] >= self.tout[lower_vertex]

    def can_swap(self, upper_vertex: str, lower_vertex: str, upper_idx: int, lower_idx: int, task_sequence: list) -> bool:
        res = True
        for i in range(upper_idx):
            res &= not self.is_parent(upper_vertex, task_sequence[i])
        for i in range(upper_idx + 1, len(task_sequence)):
            res &= not self.is_parent(task_sequence[i], upper_vertex)

        for i in range(lower_idx):
            res &= not self.is_parent(lower_vertex, task_sequence[i])
        for i in range(lower_idx + 1, len(task_sequence)):
            res &= not self.is_parent(task_sequence[i], lower_vertex)
        return not self.is_parent(lower_vertex, lower_vertex)


top_sort = TopSort(data_lists)
