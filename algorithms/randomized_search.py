from typing import Callable


def cost_fn_interface():
    pass


class RandomizedSearch:
    def __init__(self,
                 cost_fn: Callable) -> None:
        self.cost_fn