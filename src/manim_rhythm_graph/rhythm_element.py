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
        self, weights=1, colors=mn.RED, style="pie", scale=1, **kwargs
    ):
        super().__init__(**kwargs)
        self._style = RhythmVisualStyles[style.upper()]
        self._scale = scale
        self._calculate(weights, colors)

    def __repr__(self):
        return f"RhythmElement(weights={self.weights}, colors={self.colors}, style={self.style}, scale={self.scale})"

    @property
    def style(self):
        return self._style

    @property
    def scale(self):
        return self._scale

    def _calculate(self, weights, colors):
        self._calculate_weights(weights)
        self._calculate_colors(colors)
        for submob in self.get_all_submobjects():
            submob.set_opacity(0)
            self.remove(submob)
        self["pulse"] = Pulse()
        self["pulse"].scale(self.scale)

    def _calculate_weights(self, weights):
        try:
            weights[0]
        except TypeError:
            weights = int(weights)
            self.rests = weights < 0 and list(range(abs(weights))) or []
            weights = (1.0,) * abs(weights)
        except IndexError:
            return self._calculate_weights(-1)
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
