import numpy as np
import manim as mn

from .pie_sector import PieSector
from .radii import Radii
from .get_sector_pairs import get_sector_pairs


class Pie(mn.VGroup):
    def __init__(self, weights, radius=1, colors=None, **kwargs):
        stroke_color = kwargs.pop("stroke_color", mn.WHITE)
        stroke_width = kwargs.pop("stroke_width", mn.DEFAULT_STROKE_WIDTH)
        super().__init__(
            stroke_color=stroke_color, stroke_width=stroke_width, **kwargs
        )

        self.radius = radius
        self.weights = self._calculate_weights(weights)
        self.colors = self._calculate_colors(colors)

        self._add_items(
            **kwargs,
        )

    def __repr__(self):
        return (
            f"Pie({self.weights}, radius={self.radius}, colors={self.colors})"
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
            radius=self.radius,
            color=self.stroke_color,
            stroke_color=self.stroke_color,
            stroke_width=self.stroke_width * self.radius
            - self.stroke_width / 2,
            fill_opacity=1,
            z_index=self.z_index,
        )

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
            z_index=self.z_index,
        )
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

    @mn.override_animation(mn.Create)
    def _create_override(self, lag_ratio=0, run_time=1, **kwargs):
        return mn.AnimationGroup(
            mn.Create(
                self.background,
                rate_func=lambda _: 0,
                introducer=False,
                remover=True,
            ),
            mn.Create(self.radii),
            *(mn.Create(x, introducer=False, remover=True) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, lag_ratio=0, run_time=1, **kwargs):
        return mn.AnimationGroup(
            mn.FadeOut(self.background, rate_func=lambda _: 1),
            mn.Uncreate(self.radii),
            *(mn.Uncreate(x, remover=True) for x in self),
            lag_ratio=lag_ratio,
            run_time=run_time,
            remover=True,
            **kwargs,
        )

    def pulsate(self, run_time=1, **kwargs):
        return mn.Succession(
            *(
                x.pulsate(run_time=run_time * self.weights[i], **kwargs)
                for (i, x) in enumerate(self)
            ),
            run_time=run_time,
        )

    def beat(self, **kwargs):
        return self.pulsate(**kwargs)

    def set_opacity(self, opacity, **kwargs):
        self.background.set_opacity(opacity=opacity, **kwargs)
        self.radii.set_opacity(opacity=opacity, **kwargs)
        for c in self:
            c.set_opacity(opacity, **kwargs)

    def reform(self, divisions, radius=None, colors=None, **kwargs):
        pie = self.copy()
        self.background.set_opacity(0)
        del self.background
        for c in self:
            c.set_opacity(0)
            self.remove(c)
            del c

        self.radius = radius or self.radius
        self.weights = self._calculate_weights(divisions)
        self.colors = self._calculate_colors(colors)
        self._add_items(**kwargs)
        pairs = self._get_transform_pairs(pie, self)
        unpaired_radii = [
            x for x in pie.radii if x not in [z for y in pairs for z in y]
        ]
        return mn.AnimationGroup(
            *(
                mn.Transform(
                    y,
                    x,
                    path_func=mn.straight_path,
                    remover=True,
                    introducer=False,
                )
                for x, y in pairs
            ),
            *(mn.Uncreate(x, rate_func=lambda _: 1) for x in unpaired_radii),
            remover=True,
        )

    def _get_transform_pairs(self, pie, pie2):
        new_division = len(pie2.weights)
        old_division = len(pie.weights)
        if old_division == new_division:
            return ((pie2.background, pie.background), *zip(pie2, pie))
        elif old_division < new_division:
            return [(y, x) for (x, y) in self._get_pairs_from(pie, pie2)]
        elif old_division > new_division:
            return self._get_pairs_from(pie2, pie)

    def _get_pairs_from(self, fewer, more):
        pairs = [(fewer.background, more.background)]
        more_array = -(more.angles[:, 0] - mn.PI / 2)
        more_array = np.stack((more_array, (*more_array[1:], mn.TAU)))
        fewer_array = -(fewer.angles[:, 0] - mn.PI / 2)
        fewer_array = np.stack((fewer_array, (*fewer_array[1:], mn.TAU)))
        indice = get_sector_pairs(fewer_array, more_array)

        for i in range(len(indice)):
            cur_pos = indice[i]
            try:
                next_pos = indice[i + 1]
            except IndexError:
                next_pos = -1

            if cur_pos == next_pos or cur_pos == -1:
                start_item = fewer.radii[cur_pos]
            else:
                start_item = fewer[cur_pos]
            pairs.append((start_item, more[i]))
        return pairs
