import manim as mn
import numpy as np

from manim_rhythm_graph import Pie


class VerticalLine(mn.VGroup):
    def __init__(self, height=1, color=None, **kwargs):
        super().__init__()
        self.stroke_width = (
            kwargs.pop("stroke_width", mn.DEFAULT_STROKE_WIDTH) * height
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
        ellipse.flip()
        self.add(ellipse)

    @mn.override_animation(mn.Create)
    def _create_override(self, run_time=1, **kwargs):
        array = np.array([0, self.height / 2, 0])
        line = mn.Line(
            self[0].arc_center + array,
            self[0].arc_center - array,
            color=self.color,
            stroke_width=self.stroke_width,
        )
        return mn.Succession(
            mn.Create(line, remover=True, Introducer=False, **kwargs),
            mn.Transform(
                line,
                self[0],
                replace_mobject_with_target_in_scene=True,
                run_time=0,
            ),
            lag_ratio=0,
            run_time=run_time,
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs):
        return mn.Uncreate(self[0], **kwargs)

    @mn.override_animation(mn.Transform)
    def _transform_override(self, mobject2, run_time=1, **kwargs):
        if not isinstance(mobject2, Pie):
            return mn.Transform(self[0], mobject2, run_time=run_time, **kwargs)
        circ = mn.Circle(
            radius=self.height / 2,
            color=self.color,
            stroke_width=self.stroke_width,
        )
        circ.rotate(mn.PI / 2)
        circ.flip()

        animation = mn.AnimationGroup(
            mn.Transform(
                self[0],
                circ,
                run_time=run_time * 0.5,
                replace_mobject_with_target_in_scene=False,
                remover=True,
            ),
            mn.Create(mobject2, run_time=run_time),
            lag_ratio=0,
            run_time=run_time,
            remover=True,
        )

        return animation
