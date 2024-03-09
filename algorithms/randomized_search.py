from typing import Callable, Dict, Any, List
import random
from data_matching_functions import create_project_role_ids, match_task_id_to_resourse_id


class RandomizedSearch:
    def __init__(self,
                 cost_fn: Callable,
                 num_iterations: int) -> None:
        self.cost_fn = cost_fn
        self.num_iterations = num_iterations
    
    def fit(self, *args) -> None:
        pass

    def predict(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        tasks_by_project_roles = create_project_role_ids(data)
        tasks_to_resourses = match_task_id_to_resourse_id(data, tasks_by_project_roles)

        best_combination = tasks_to_resourses
        best_cost = self.cost_fn(...)

        for _ in range(self.num_iterations):
            
            curr_tasks2res = match_task_id_to_resourse_id(data, tasks_by_project_roles)
            current_cost = self.cost_fn()

            if current_cost < best_cost:
                best_combination = curr_tasks2res
                best_cost = current_cost
        
        return best_combination


if __name__ == "__main__":
    x  = [1, 2, 3, 4, 5, 6]
    random.shuffle(x)
    print(x)
    random.shuffle(x)
    print(x)
