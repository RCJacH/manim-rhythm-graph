import manim as mn


class PieSlice(mn.Sector):
    def interpolate(
        self, mobject1, mobject2, alpha, path_func=mn.straight_path
    ):
        if not (
            isinstance(mobject1, PieSlice) and isinstance(mobject2, PieSlice)
        ):
            return super().interpolate(
                mobject1, mobject2, alpha, path_func=path_func
            )

        for attr in (
            "start_angle",
            "angle",
            "inner_radius",
            "outer_radius",
        ):
            v1 = getattr(mobject1, attr)
            v2 = getattr(mobject2, attr)
            setattr(self, attr, path_func(v1, v2, alpha))

        self.arc_center = path_func(
            mobject1.get_arc_center(), mobject2.get_arc_center(), alpha
        )
        self.interpolate_color(mobject1, mobject2, alpha)
        self.clear_points()
        self.generate_points()
        return self


class PieSector(mn.VDict):
    def __init__(
        self, start_angle=0, angle=mn.PI / 2, radius=1, color=None, **kwargs
    ):
        color = color or mn.GRAY_D
        stroke_color = kwargs.pop("stroke_color", mn.WHITE)
        stroke_width = kwargs.pop("stroke_width", mn.DEFAULT_STROKE_WIDTH)
        super().__init__(
            stroke_color=stroke_color, stroke_width=stroke_width, **kwargs
        )

        self.start_angle = start_angle
        self.angle = angle
        self.radius = radius
        self.color = color
        stroke = PieSlice(
            outer_radius=radius,
            start_angle=start_angle,
            angle=angle,
            stroke_color=stroke_color,
            stroke_width=stroke_width * radius - stroke_width / 2,
            fill_color=color,
            fill_opacity=0,
            z_index=self.z_index + 1,
        )

        fill = PieSlice(
            outer_radius=radius,
            start_angle=start_angle,
            angle=angle,
            stroke_color=stroke_color,
            stroke_width=0,
            fill_color=color,
            fill_opacity=1,
            z_index=self.z_index,
        )

        self.add([("fill", fill), ("stroke", stroke)])

    def __repr__(self):
        return f"PieSector(start_angle={self.start_angle}, angle={self.angle}, radius={self.radius}, color={self.color}, stroke_width={self.stroke_width}, stroke_color={self.stroke_color})"

    def beat(self, **kwargs):
        return mn.Indicate(
            self,
            scale_factor=0.95,
            color=mn.interpolate_color(self.color, mn.WHITE, 0.8),
            rate_func=lambda t: 1
            - mn.rate_functions.ease_in_out_quart(t * 0.8),
            **kwargs,
        )

    @mn.override_animation(mn.Create)
    def _create_override(self, lag_ratio=0.38, **kwargs):
        return mn.AnimationGroup(
            mn.Create(
                self["stroke"],
                rate_func=lambda t: mn.rate_functions.ease_in_cubic(0.1 + t),
            ),
            mn.Create(self["fill"]),
            lag_ratio=lag_ratio,
            **kwargs,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, lag_ratio=0.3, **kwargs):
        return mn.AnimationGroup(
            mn.Uncreate(self["fill"]),
            mn.Uncreate(
                self["stroke"],
                run_time=0.5,
                rate_func=lambda t: 0.1
                + mn.rate_functions.ease_out_sine(t) * 0.9,
            ),
            lag_ratio=lag_ratio,
            **kwargs,
        )
