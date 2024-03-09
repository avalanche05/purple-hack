from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.common import data_lists
from algorithms.cost_functions import cost_len_fn
from algorithms.common import get_output
import json
import math

if __name__ == "__main__":
    simulated_annealing = SimulatedAnnealing(cost_len_fn, 1.0, 0.99, 10000)
    ans, assigned_time_list = simulated_annealing.predict_resource(data_lists)
    print(ans)

    with open("result.json", "w") as result_file:
        json.dump(get_output(assigned_time_list), result_file)


