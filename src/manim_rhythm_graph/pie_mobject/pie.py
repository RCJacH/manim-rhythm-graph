import numpy as np
import manim as mn

from .pie_sector import PieSector


class Radii(mn.Group):
    def __init__(
        self, angles, radius, stroke_color, stroke_width, color=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.angles = [*angles[:, 0], angles[-1].sum()]
        self.radius = radius
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.add(
            *(
                PieSector(
                    radius=radius,
                    start_angle=a,
                    angle=0,
                    color=color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    **kwargs,
                )
                for a in self.angles
            )
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, lag_ratio=0, rate_func=lambda _: 1, **kwargs):
        return mn.AnimationGroup(
            *(mn.Uncreate(x, remover=True, rate_func=rate_func) for x in self),
            lag_ratio=lag_ratio,
            remover=True,
            **kwargs,
        )


class Pie(mn.VGroup):
    def __init__(self, divisions, radius=1, colors=None, **kwargs):
        stroke_color = kwargs.pop("stroke_color", mn.WHITE)
        stroke_width = kwargs.pop("stroke_width", mn.DEFAULT_STROKE_WIDTH)
        super().__init__(
            stroke_color=stroke_color, stroke_width=stroke_width, **kwargs
        )

        self.radius = radius
        self.weights = self._calculate_weights(divisions)
        self.colors = self._calculate_colors(colors)

        self._add_items(
            **kwargs,
        )

    def _calculate_weights(self, weights):
        try:
            weights[0]
        except TypeError:
            weights = np.array((1.0,) * int(weights), dtype="float64")
        else:
            weights = np.array(weights, dtype="float64")
        finally:
            weights /= weights.sum()
        return weights

    def _calculate_colors(self, colors):
        try:
            colors[0]
        except TypeError:
            colors = (mn.RED,) * self.weights.size
        else:
            if len(colors) != self.weights.size:
                raise IndexError(
                    "The length of colors and weights do not match."
                )
        return colors

    def _add_bg(self):
        self.background = mn.Circle(
            radius=self.radius, color=self.stroke_color, z_index=self.z_index
        )

    def _add_items(self, **kwargs):
        self._add_bg()

        self.angles = self.weights * -mn.TAU
        self.start_angles = np.cumsum((0, *self.angles[:-1])) + mn.PI / 2

        self.add(
            *(
                PieSector(
                    radius=self.radius,
                    start_angle=a + sa,
                    angle=-a,
                    stroke_color=self.stroke_color,
                    stroke_width=self.stroke_width,
                    color=self.colors[i],
                    z_index=self.z_index + 1,
                    **kwargs,
                )
                for i, (sa, a) in enumerate(
                    zip(self.start_angles, self.angles)
                )
            )
        )

    @mn.override_animation(mn.Create)
    def _create_override(self, lag_ratio=0, run_time=1, **kwargs):
        return mn.AnimationGroup(
            mn.FadeIn(
                self.background,
                rate_func=lambda t: t == 1,
            ),
            *(mn.Create(x) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, lag_ratio=0, run_time=1, **kwargs):
        return mn.AnimationGroup(
            mn.FadeOut(self.background, rate_func=lambda _: 1),
            *(mn.Uncreate(x, remover=True) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            remover=True,
            **kwargs,
        )

    def beat(self, run_time=1, **kwargs):
        return mn.Succession(
            *(
                x.beat(run_time=run_time / self.weights[i], **kwargs)
                for (i, x) in enumerate(self)
            ),
            run_time=run_time,
        )
