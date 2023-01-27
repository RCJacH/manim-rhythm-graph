from manim import *

from manim_rhythm_graph.pie_mobject.pie_sector import PieSector


class TestSingle(Scene):
    def construct(self):
        pie = PieSector(radius=3, color=None)

        self.play(Create(pie))
        self.play(pie.beat())
        self.play(Uncreate(pie))


if __name__ == "__main__":
    with tempconfig({"dry_run": True}):
        TestSingle().render()
