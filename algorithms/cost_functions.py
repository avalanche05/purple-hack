from typing import Callable, Union


Number = Union[float, int]


def cost_len_fn(args) -> Number:
    pass


def cost_resource_fn(args) -> Number:
    pass


def cost_fn(args) -> Number:
    pass


def combined_cost_fn(fn1: Callable,
                     fn2: Callable,
                     fn3: Callable) -> Callable:
    
    def _fn(args):
        return 0.5 * fn1(args) + 0.3 * fn2(args) + 0.2 * fn3(args)
    
    return _fn
