import itertools
import numpy as np
import manim as mn

from manim_rhythm_graph.pie_mobject import Pie
from manim_rhythm_graph.pulse_mobject import Pulse


class RhythmElement(mn.VDict):
    def __init__(
        self, weights=1, scale=1, colors=mn.RED, representation="Pie", **kwargs
    ):
        super().__init__(**kwargs)
        self.rests = []
        self.set_scale(scale)
