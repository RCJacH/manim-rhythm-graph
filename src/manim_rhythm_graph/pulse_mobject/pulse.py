import math
import manim as mn
import numpy as np

from manim_rhythm_graph import Pie


class Pulse(mn.VGroup):
    def __init__(self, height=1, color=None, **kwargs):
        super().__init__()
        self.stroke_width = kwargs.pop(
            "stroke_width", mn.DEFAULT_STROKE_WIDTH * height
        )
        self.color = color or mn.WHITE

        ellipse = mn.Ellipse(
            width=height * 2,
            height=0,
            stroke_width=self.stroke_width,
            color=self.color,
            **kwargs,
        )
        ellipse.rotate(mn.PI / 2)
        ellipse.force_direction("CW")
        self.add(ellipse)

    def beat(self, **kwargs):
        return self.pulsate(**kwargs)

    def pulsate(self, **kwargs):
        return mn.Indicate(
            self,
            scale_factor=1.04,
            color=mn.interpolate_color(self.color, mn.YELLOW, 0.25),
            rate_func=lambda t: mn.rate_functions.there_and_back(
                mn.rate_functions.ease_in_out_quart(t**0.25)
            ),
            **kwargs,
        )

    def set_opacity(self, opacity, **kwargs):
        self[0].set_opacity(opacity, **kwargs)
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs):
        return mn.AnimationGroup(
            mn.Create(self[0]),
            rate_func=lambda t: 0.5
            * mn.rate_functions.ease_out_sine(t**1.2),
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs):
        return mn.AnimationGroup(
            mn.Uncreate(self[0]),
            rate_func=lambda t: mn.rate_functions.smooth(0.5 + t * 0.5, 5),
            **kwargs,
        )

    @mn.override_animation(mn.Transform)
    def _transform_override(self, mobject2, run_time=1, **kwargs):
        if not isinstance(mobject2, Pie):
            return mn.Transform(self[0], mobject2, run_time=run_time, **kwargs)
        circ = mn.Ellipse(
            width=self.height,
            height=self.height,
            color=self.color,
            stroke_width=self.stroke_width,
        )
        circ.rotate(mn.PI / 2)
        circ.force_direction("CW")
        ellipse = self[0].copy()

        self.remove(self[0])
        self.add(circ)

        animation = mn.AnimationGroup(
            mn.Transform(
                ellipse,
                circ,
                run_time=run_time * 0.6,
                rate_func=lambda t: mn.rate_functions.ease_out_quart(t * 0.6),
                introducer=False,
                remover=True,
            ),
            mn.Create(
                mobject2,
                run_time=run_time,
            ),
            mn.FadeIn(self[0], run_time=0),
            lag_ratio=0,
        )

        return animation
