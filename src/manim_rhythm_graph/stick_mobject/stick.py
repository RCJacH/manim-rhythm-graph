import math
import manim as mn
import numpy as np


class Stick(mn.VGroup):
    def __init__(self, height=1, color=None, **kwargs):
        super().__init__()
        self.stroke_width = kwargs.pop(
            "stroke_width", mn.DEFAULT_STROKE_WIDTH * height
        )
        self.color = color or mn.WHITE

        ellipse = mn.Ellipse(
            width=height * 2,
            height=0,
            stroke_color=self.color,
            stroke_width=self.stroke_width,
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
        self[0].set_stroke_opacity(opacity, **kwargs)
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
    def _transform_override(self, mobject2, *args, **kwargs):
        if type(mobject2).__name__ == "Pie":
            return self._transform_to_pie(mobject2, *args, **kwargs)

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
            mn.Transform(
                self[0],
                circ,
                run_time=run_time * 0.6,
                rate_func=lambda t: mn.rate_functions.ease_out_quart(t * 0.6),
                replace_mobject_with_target_in_scene=True,
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
