from enum import Enum
from typing import Callable, Optional

import numpy as np
from pydantic import BaseModel


class LinkFunctionChoices(Enum):
    identity = "identity"
    power = "power"


class TrackingConfig(BaseModel):
    appear_weight: float = -0.5
    disappear_weight: float = -0.75
    division_weight: float = -1.0
    dismiss_weight_guess: Optional[float] = None
    include_weight_guess: Optional[float] = None
    solution_gap: float = 0.001
    time_limit: int = 36000
    method: int = -1
    n_threads: int = 0
    link_function: LinkFunctionChoices = "identity"
    power: float = 4
    bias: float = -0.005

    @property
    def apply_link_function(self) -> Callable[[np.ndarray], np.ndarray]:
        if self.link_function == LinkFunctionChoices.identity:
            return lambda x: x
        elif self.link_function == LinkFunctionChoices.power:
            return lambda x: np.power(x, self.power) + self.bias
        else:
            raise NotImplementedError