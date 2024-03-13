import json

from algorithms.common import init, get_output, data_lists
from algorithms.cost_functions import combined_cost_fn, cost_len_fn, cost_resource_fn, cost_fn
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.graph_dependencies import topological_sort
from algorithms import cost_functions


def process_json(data: dict, duration: float, price: float, resource: float) -> dict:
    init(data)
    with open("data_lists.json", "w") as f:
        json.dump(data_lists, f)
    print(data_lists.get("is_task"))
    topological_sort.init()
    cost_functions.init()

    print(duration, price, resource)
    num_iterations = 300
    if duration == 1 and price == 0 and resource == 0:
        simulated_annealing = SimulatedAnnealing(cost_len_fn, 1.0, 0.99, num_iterations)
        ans, assigned_time_list = simulated_annealing.predict_resource(data_lists)
    elif duration == 0 and price == 1 and resource == 0:
        simulated_annealing = SimulatedAnnealing(cost_len_fn, 1.0, 0.99, num_iterations)
        ans, assigned_time_list = simulated_annealing.predict_resource(data_lists, "price")
    elif duration == 0 and price == 0 and resource == 1:
        print("INN")
        simulated_annealing = SimulatedAnnealing(cost_len_fn, 1.0, 0.99, num_iterations)
        ans, assigned_time_list = simulated_annealing.predict_resource(data_lists, "resource")
    else:
        simulated_annealing = SimulatedAnnealing(
            combined_cost_fn(cost_len_fn, cost_fn, cost_resource_fn, duration, price, resource), 1.0, 0.99, num_iterations)
        ans, assigned_time_list = simulated_annealing.predict_resource(data_lists)

    return get_output(assigned_time_list)
