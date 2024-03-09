from typing import Callable
import math
import random

from data_matching_functions import create_project_role_ids, match_task_id_to_resourse_id
from cost_functions import cost_fn, cost_len_fn, cost_resource_fn, combined_cost_fn


class SimulatedAnnealing:
    def __init__(self,
                 cost_fn: Callable,
                 temperature: float,
                 temperature_decay: float = 0.99,
                 num_iterations: int = 1000):
        self.temp = temperature
        self.temp_decay = temperature_decay
        self.num_iterations = num_iterations
        self.cost_fn = cost_fn

    def fit(self, *args) -> None:
        pass

    def predict_sequence(self, task_ids, tasks_to_resources):
        task_sequence = task_ids.copy()
        random.shuffle(task_sequence)
        ans = assign_time(task_ids, tasks_to_resources)

        for i in range(self.num_iterations):
            self.temp *= self.temp_decay
            first_id = random.randint(0, len(task_ids))
            second_id = random.randint(0, len(task_ids))

            if can_swap(task_ids[first_id], task_ids[second_id]):
                annealed_task_sequence = task_sequence.copy()
                annealed_task_sequence[first_id], annealed_task_sequence[second_id] = annealed_task_sequence[second_id], \
                annealed_task_sequence[first_id]
                annealed_ans = assign_time(annealed_task_sequence, tasks_to_resources)
                if annealed_ans < ans or random.uniform(0, 1) < math.exp((annealed_ans - ans) / self.temp):
                    task_sequence = annealed_task_sequence
                    ans = annealed_ans

        return ans

    def predict_resource(self, data):
        resources_py_project_roles = create_project_role_ids(data)
        tasks_to_resources = match_task_id_to_resourse_id(data, resources_py_project_roles)
        project_roles = list(resources_py_project_roles.keys())
        ans = self.cost_fn(...)

        for i in range(self.num_iterations):
            self.temp *= self.temp_decay
            annealed_tasks_to_resources = tasks_to_resources.copy()
            project_role_id = random.choice(project_roles)
            first_id = resources_py_project_roles[project_role_id][
                random.randint(0, len(resources_py_project_roles[project_role_id]))]  # task id
            second_id = resources_py_project_roles[project_role_id][
                random.randint(0, len(resources_py_project_roles[project_role_id]))]
            annealed_tasks_to_resources[first_id], annealed_tasks_to_resources[second_id] = \
                annealed_tasks_to_resources[second_id], annealed_tasks_to_resources[first_id]

            # annealed_ans = self.cost_fn(...)
            sequence_simulated_annealing = SimulatedAnnealing(1.0, 1000)
            annealed_ans = sequence_simulated_annealing.predict_sequence(...)

            if annealed_ans < ans or random.uniform(0, 1) < math.exp((annealed_ans - ans) / self.temp):
                tasks_to_resources = annealed_tasks_to_resources
                ans = annealed_ans


if __name__ == "__main__":
    simulated_annealing = SimulatedAnnealing(1.0, 1000)
    simulated_annealing.predict(data)
