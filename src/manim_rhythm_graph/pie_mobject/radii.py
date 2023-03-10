import manim as mn

from .pie_sector import PieSector


class Radii(mn.VGroup):
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
                    radius=self.radius,
                    start_angle=a,
                    angle=0,
                    color=color,
                    stroke_color=self.stroke_color,
                    stroke_width=self.stroke_width,
                    **kwargs,
                )
                for a in self.angles
            )
        )

    def __repr__(self):
        return f"Radii(angles={self.angles}, radius={self.radius}, stroke_color={self.stroke_color}, stroke_width={self.stroke_width})"

    def set_opacity(self, opacity, **kwargs):
        for c in self:
            c.set_opacity(opacity, **kwargs)
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self, lag_ratio=0, rate_func=lambda _: 0, **kwargs):
        return mn.AnimationGroup(
            *(mn.Create(x, rate_func=rate_func) for x in self),
            lag_ratio=lag_ratio,
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(
        self, lag_ratio=0, rate_func=lambda t: t > 0.6, remover=True, **kwargs
    ):
        return mn.AnimationGroup(
            *(mn.Uncreate(x, remover=remover) for x in self),
            lag_ratio=lag_ratio,
            rate_func=rate_func,
            **kwargs,
        )
