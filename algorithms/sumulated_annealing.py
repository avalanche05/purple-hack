import math
import random

from data_matching_functions import create_project_role_ids, match_task_id_to_resource_id
from cost_functions import cost_fn, cost_len_fn, cost_resource_fn, combined_cost_fn


class SimulatedAnnealing:
    def __init__(self,
                 temp: float,
                 num_iterations: int):
        self.temp = temp
        self.num_iterations = num_iterations

    def predict_task_to_resource(self, data) -> dict:
        tasks_by_project_roles = create_project_role_ids(data)
        tasks_to_resources = match_task_id_to_resource_id(data, tasks_by_project_roles)
        ans = combined_cost_fn(...)

        for i in range(self.num_iterations):
            self.temp *= 0.99
            annealed_tasks_to_resources = tasks_to_resources.copy()
            project_role_id = random.randint(0, len(tasks_by_project_roles))

            first_id = tasks_by_project_roles[project_role_id][random.randint(0, len(tasks_by_project_roles[project_role_id]))]  # task id
            second_id = tasks_by_project_roles[project_role_id][random.randint(0, len(tasks_by_project_roles[project_role_id]))]
            annealed_tasks_to_resources[first_id], annealed_tasks_to_resources[second_id] = \
                annealed_tasks_to_resources[second_id], annealed_tasks_to_resources[first_id]

            annealed_ans = combined_cost_fn(...)
            if annealed_ans > ans or random.uniform(0, 1) < math.exp((annealed_ans - ans) / self.temp):
                tasks_to_resources = annealed_tasks_to_resources
                ans = annealed_ans

        return tasks_to_resources

        def predict_task_priority(self, tasks_to_resources):
            task_priorities = [x for x in range(len(tasks_to_resources))]
            ans =




if __name__ == "__main__":
    simulated_annealing = SimulatedAnnealing(1.0, 1000)
    simulated_annealing.predict(data)
