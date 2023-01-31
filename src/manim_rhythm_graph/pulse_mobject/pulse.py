import manim as mn
import numpy as np


def squeeze(t, v):
    return (1 - v) / 2 + t * v


class Pulse(mn.VGroup):
    LEVELS = (0, 0.3, -0.5, 1, -1, 0)

    def __init__(
        self, levels=None, scale=1, horizontal_ratio=0.3, color=None, **kwargs
    ):
        super().__init__()
        self.stroke_width = kwargs.pop(
            "stroke_width", mn.DEFAULT_STROKE_WIDTH * scale
        )
        self.color = color or mn.WHITE

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
            stroke_color=self.color,
            stroke_width=self.stroke_width,
            **kwargs,
        )
        self.add(polygon)
        self.scale(scale)

    def set_opacity(self, opacity, **kwargs):
        self[0].set_stroke(opacity=opacity, **kwargs)
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self, *args, **kwargs):
        return mn.Create(self[0], *args, **kwargs)

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, *args, **kwargs):
        return mn.Uncreate(self[0], *args, **kwargs)

    @mn.override_animation(mn.Transform)
    def _transform_override(self, mobject2, *args, **kwargs):
        target_name = type(mobject2).__name__
        if target_name == "Pie":
            return self._transform_to_pie(mobject2, *args, **kwargs)
        if target_name == "Stick":
            target = mobject2[0].copy()
            mobject2.set_opacity(0)
            return mn.Succession(
                mn.ClockwiseTransform(self[0], target),
                mobject2.animate(
                    run_time=0.001, rate_func=lambda _: 1
                ).set_opacity(1),
                *args,
                **kwargs,
            )

        return mn.Transform(self[0], mobject2, *args, **kwargs)

    def _transform_to_pie(self, pie, *args, run_time=1, **kwargs):
        circ = mn.Ellipse(
            width=self.height,
            height=self.height,
            stroke_color=self.color,
            stroke_width=self.stroke_width,
        )
        circ.rotate(mn.PI / 2)
        circ.force_direction("CW")

        return mn.AnimationGroup(
            mn.ClockwiseTransform(
                self[0],
                circ,
                run_time=run_time * 0.7,
                rate_func=lambda t: mn.rate_functions.ease_out_quart(t),
                remover=True,
            ),
            mn.Create(pie),
            circ.animate(
                run_time=0.001, rate_func=lambda _: 1, remover=True
            ).set_opacity(0),
            *args,
            run_time=run_time,
            **kwargs,
        )
