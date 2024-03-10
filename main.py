from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.common import data_lists
from algorithms.cost_functions import cost_len_fn, cost_resource_fn, cost_fn
from algorithms.common import get_output
import json
from copy import deepcopy

if __name__ == "__main__":
    min_ans = None
    min_assigned_time_list = []

    for _ in range(5):
        simulated_annealing = SimulatedAnnealing(cost_len_fn, 1.0, 0.99, 100)
        ans, assigned_time_list = simulated_annealing.predict_resource(deepcopy(data_lists))
        if min_ans is None or ans < min_ans:
            min_ans = ans
            min_assigned_time_list = assigned_time_list

    start_date = min(min_assigned_time_list, key=lambda x: x["start_date"])["start_date"]
    end_date = max(min_assigned_time_list, key=lambda x: x["end_date"])["end_date"]
    res = get_output(min_assigned_time_list)
    with open("result.json", "w") as result_file:
        try:
            json.dump(res, result_file)
        except Exception as err:
            print("result ", err, res)
