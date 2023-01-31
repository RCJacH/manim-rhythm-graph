import manim as mn
import numpy as np


def squeeze(t, v):
    return (1 - v) / 2 + t * v


class Pulse(mn.VGroup):
    LEVELS = (0, 0.3, -0.5, 1, -1, 0)

    def __init__(
        self,
        levels=None,
        scale=1,
        horizontal_ratio=0.3,
        color=mn.WHITE,
        **kwargs
    ):
        super().__init__()

        levels = levels or self.LEVELS
        positions = [
            [
                squeeze(i / (len(levels) - 1), horizontal_ratio) * 2 - 1,
                x,
                0,
            ]
            for i, x in enumerate(levels)
        ]
        positions = [[-1, 0, 0], *positions, [1, 0, 0]]
        polygon = mn.Polygon(
            *positions[:-1],
            *positions[::-1],
            color=color,
            **kwargs,
        )
        self.add(polygon)
        self.scale(scale)

    @mn.override_animation(mn.Create)
    def _create_override(self, *args, **kwargs):
        return mn.Create(self[0], *args, **kwargs)

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, *args, **kwargs):
        return mn.Uncreate(self[0], *args, **kwargs)

    @mn.override_animation(mn.Transform)
    def _transform_override(self, mobject, *args, **kwargs):
        if isinstance(mobject, mn.Ellipse):
            return mn.Succession(
                self[0].animate().rotate(-mn.PI / 2),
                mn.Transform(self[0], mobject, *args, **kwargs),
            )

        return mn.Transform(self[0], mobject, *args, **kwargs)
