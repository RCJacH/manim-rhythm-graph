from sys import float_info
import numpy as np
import manim as mn

from .pie_sector import PieSector
from .radii import Radii
from .get_transform_pairs import get_transform_pairs


INSTANT = float_info.min


class Pie(mn.VGroup):
    def __init__(self, weights, colors, radius=1, **kwargs):
        stroke_color = kwargs.pop("stroke_color", mn.WHITE)
        stroke_width = kwargs.pop("stroke_width", mn.DEFAULT_STROKE_WIDTH)
        super().__init__(
            stroke_color=stroke_color, stroke_width=stroke_width, **kwargs
        )

        self._calculate(weights, colors, radius)

    def __repr__(self):
        return (
            f"Pie({self.weights}, radius={self.radius}, colors={self.colors})"
        )

    def beat(self, **kwargs):
        return self.pulsate(**kwargs)

    def pulsate(self, run_time=1, **kwargs):
        self.background.set_fill(opacity=1)
        return mn.Succession(
            *(
                x.pulsate(run_time=run_time * self.weights[i], **kwargs)
                for (i, x) in enumerate(self)
            ),
            run_time=run_time,
        )

    def set_opacity(self, opacity, **kwargs):
        self.background.set_opacity(opacity=opacity, **kwargs)
        self.radii.set_opacity(opacity=opacity, **kwargs)
        for c in self:
            c.set_opacity(opacity, **kwargs)
        return self

    @mn.override_animation(mn.Create)
    def _create_override(
        self,
        lag_ratio=0,
        run_time=1,
        introducer=True,
        **kwargs,
    ):
        self.background.set_opacity(opacity=0)
        return mn.AnimationGroup(
            mn.Create(self.radii, introducer=False),
            *(mn.Create(x) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            introducer=introducer,
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(
        self, lag_ratio=0, run_time=1, remover=True, **kwargs
    ):
        self.background.set_opacity(0)
        return mn.AnimationGroup(
            mn.Uncreate(self.radii, remover=remover),
            *(mn.Uncreate(x, remover=remover) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )

    @mn.override_animation(mn.Transform)
    def _transform_override(self, mobject2, *args, remover=True, **kwargs):
        if type(mobject2).__name__ == "Pie":
            return self._transform_to_pie(mobject2, *args, **kwargs)
        if type(mobject2).__name__ == "Stick":
            return self._transform_to_stick(mobject2, *args, **kwargs)
        if type(mobject2).__name__ == "Pulse":
            return self._transform_to_pulse(mobject2, *args, **kwargs)

        bg = self.background.copy()
        bg.set_fill_opacity(0)
        return mn.AnimationGroup(
            mn.Uncreate(self),
            mn.Transform(
                bg,
                mobject2,
                replace_mobject_with_target_in_scene=False,
                remover=remover,
                **kwargs,
            ),
        )

    def _calculate(self, weights=None, colors=None, radius=None, **kwargs):
        if weights is not None:
            self.weights = weights
        if colors is not None:
            self.colors = colors
        if radius is not None:
            self.radius = radius

        try:
            self.background.set_opacity(0)
        except AttributeError:
            pass
        else:
            del self.background

        for c in self:
            c.set_opacity(0)
            self.remove(c)
            del c

        self._add_items(**kwargs)

    def _add_bg(self):
        ellipse = mn.Ellipse(
            height=self.radius * 2,
            width=self.radius * 2,
            color=self.stroke_color,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width,
            fill_opacity=1,
            z_index=self.z_index,
        )
        ellipse.rotate(mn.PI / 2)
        ellipse.force_direction("CW")
        self.background = ellipse

    def _add_items(self, **kwargs):
        self._add_bg()

        angles = self.weights * -mn.TAU
        start_angles = np.cumsum((0, *angles[:-1])) + mn.PI / 2
        self.angles = np.stack((start_angles, angles)).transpose()

        self.radii = Radii(
            self.angles,
            self.radius,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width,
            z_index=self.z_index + 3,
        )
        self.radii.set_opacity(0)
        self.add(
            *(
                PieSector(
                    radius=self.radius,
                    start_angle=a.sum(),
                    angle=-a[1],
                    stroke_color=self.stroke_color,
                    stroke_width=self.stroke_width,
                    color=self.colors[i],
                    z_index=self.z_index + 1,
                    **kwargs,
                )
                for i, a in enumerate(self.angles)
            )
        )

    def _transform_to_pie(self, pie, *args, **kwargs):
        pairs = get_transform_pairs(self, pie)
        return mn.AnimationGroup(
            *(
                mn.Transform(
                    y,
                    x,
                    path_func=mn.straight_path,
                    replace_mobject_with_target_in_scene=True,
                    remover=True,
                )
                for x, y in pairs
            ),
            mn.FadeOut(self.radii, rate_func=lambda _: 1),
            mn.FadeIn(pie.radii, rate_func=lambda t: t == 1),
            *args,
            **kwargs,
        )

    def _transform_to_pulse(
        self, pulse, *args, run_time=1, lag_ratio=0.6, **kwargs
    ):
        circ = mn.Ellipse(
            width=self.height,
            height=self.height,
            stroke_color=self.color,
            stroke_width=self.stroke_width,
        )
        circ.force_direction("CW")

        return mn.AnimationGroup(
            mn.Uncreate(self, remover=False),
            mn.CounterclockwiseTransform(
                circ,
                pulse,
                run_time=run_time,
                rate_func=lambda t: mn.rate_functions.ease_out_quart(t),
                replace_mobject_with_target_in_scene=True,
            ),
            *args,
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )

    def _transform_to_stick(
        self, stick, *args, run_time=1, lag_ratio=0.6, **kwargs
    ):
        circ = mn.Ellipse(
            width=self.height,
            height=self.height,
            stroke_color=self.color,
            stroke_width=self.stroke_width,
        )
        circ.rotate(mn.PI / 2)
        circ.force_direction("CW")

        return mn.AnimationGroup(
            mn.Uncreate(self, remover=False),
            mn.Transform(
                circ,
                stick,
                run_time=run_time,
                rate_func=lambda t: mn.rate_functions.ease_out_quart(t),
                replace_mobject_with_target_in_scene=True,
            ),
            *args,
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )
