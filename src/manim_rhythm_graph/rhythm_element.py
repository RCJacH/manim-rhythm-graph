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
        self, weights=1, colors=mn.RED, scale=1, style="pie", **kwargs
    ):
        super().__init__(**kwargs)
        self._scale = 1
        self._calculate(weights, colors, scale, style)

    def __repr__(self):
        return f"RhythmElement(weights={self.weights}, colors={self.colors}, style={self.style}, scale={self.scale})"

    @property
    def style(self):
        return self._style

    @property
    def scale(self):
        return self._scale

    def pulsate(self, **kwargs):
        return self[self.style].pulsate(**kwargs)

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs):
        return mn.Create(self[self.style], **kwargs)

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs):
        return mn.Uncreate(self[self.style], **kwargs)

    def _calculate(self, weights=None, colors=None, scale=None, style=None):
        scale = scale or self._scale
        style = style or self._style
        self.stroke_width /= self.scale
        self.stroke_width *= scale
        self._scale = scale
        self._style = RhythmVisualStyles[style.upper()]
        if weights is not None:
            self._calculate_weights(weights)
        if colors is not None:
            self._calculate_colors(colors)
        for submob in self.get_all_submobjects():
            submob.set_opacity(0)
            self.remove(submob)

        pulse = Pulse(
            height=self.scale,
            color=self.stroke_color,
            stroke_width=self.stroke_width,
        )
        pulse.set_opacity(self.style == RhythmVisualStyles.PULSE)
        self[RhythmVisualStyles.PULSE] = pulse

        pie = Pie(
            weights=self.weights,
            colors=self.colors,
            radius=self.scale,
            stroke_width=self.stroke_width,
            stroke_color=self.stroke_color,
        )
        pie.set_opacity(self.style == RhythmVisualStyles.PIE)
        self[RhythmVisualStyles.PIE] = pie

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
