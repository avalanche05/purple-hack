from typing import Callable, Dict, Any
import random


class RandomizedSearch:
    def __init__(self,
                 cost_fn: Callable,
                 num_iterations: int) -> None:
        self.cost_fn = cost_fn
        self.num_iterations = num_iterations
    
    def fit(self):
        pass

    def predict(self, data: Dict[str, Any]):

        resource_ids = data["resource_id"]
        task_ids = data["task_id"]

        best_combination = None
        best_cost = float("inf")

        for _ in range(self.num_iterations):
            random.shuffle(task_ids)
            
            resource_task_pairs = list(zip(resource_ids, task_ids))

            ...
            current_cost = self.cost_fn()

            if current_cost < best_cost:
                best_combination = resource_task_pairs
                best_cost = current_cost
        
        return best_combination


if __name__ == "__main__":
    x  = [1, 2, 3, 4, 5, 6]
    random.shuffle(x)
    print(x)
    random.shuffle(x)
    print(x)
