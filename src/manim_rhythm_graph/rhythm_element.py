from enum import Enum
import itertools
from collections.abc import Iterable
import numpy as np
import manim as mn

from manim_rhythm_graph.pie_mobject import Pie
from manim_rhythm_graph.pulse_mobject import Pulse


class RhythmVisualStyles(Enum):
    PULSE = 1
    PIE = 2


class RhythmElement(mn.VDict):
    def __init__(
        self, weights=1, scale=1, colors=mn.RED, style="pie", **kwargs
    ):
        super().__init__(**kwargs)
        self.set_scale(scale)
        self.style = RhythmVisualStyles[style.upper()]

        self._calculate_weights(weights)
        self._calculate_colors(colors)

    def _calculate_weights(self, weights):
        try:
            weights[0]
        except TypeError:
            weights = int(weights)
            self.rests = weights < 0 and list(range(abs(weights))) or []
            weights = (1.0,) * abs(weights)
        except IndexError:
            self._calculate_weights(-1)
        else:
            self.rests = [i for (i, v) in enumerate(weights) if v < 0]
            weights = [abs(x) for x in weights]
        finally:
            weights = np.array(weights, dtype="float64")
            weights /= weights.sum()
        self.weights = weights

    def _calculate_colors(self, colors):
        if isinstance(colors, str):
            colors = (colors,)
        try:
            colors = itertools.cycle(colors)
        except TypeError as f:
            raise f
        else:
            colors = [
                None if i in self.rests else next(colors)
                for i in range(len(self.weights))
            ]
        self.colors = colors
