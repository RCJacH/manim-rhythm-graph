from manim import *

from manim_rhythm_graph import Pie


class TestSingle(Scene):
    def construct(self):
        pie = Pie(3, radius=3)

        self.play(Create(pie))
        self.play(pie.beat())
        self.play(pie.beat())
        self.play(Uncreate(pie))


class TestReformEqual(Scene):
    def construct(self):
        pie = Pie(3, radius=2)

        self.play(Create(pie))
        self.play(pie.beat())
        self.play(pie.reform([1, 2, 3], radius=3, colors=[GREEN, GREEN, BLUE]))
        self.play(pie.beat())
        self.play(pie.reform([6, 4, 5], radius=1.5, colors=[RED, GOLD, GRAY]))
        self.play(pie.beat())
        self.play(Uncreate(pie))


class TestReformFewer(Scene):
    def construct(self):
        pie = Pie(4, radius=2)

        self.play(Create(pie))
        self.play(pie.beat())
        self.play(pie.reform([2, 1, 3], radius=1.5, colors=[BLUE, BLUE, GRAY]))
        self.play(pie.beat())
        self.play(pie.reform([4, 3], radius=3, colors=[TEAL_B, GOLD]))
        self.play(pie.beat())
        self.play(Uncreate(pie))
        pass


class TestReformMore(Scene):
    def construct(self):
        pie = Pie(2, radius=2)

        self.play(Create(pie))
        self.play(pie.beat())
        self.play(pie.reform([1, 2, 3], radius=1.5, colors=[BLUE, BLUE, GRAY]))
        self.play(pie.beat())
        self.play(
            pie.reform(
                [4, 5, 6, 3],
                radius=3,
                colors=[
                    GRAY,
                    YELLOW,
                    TEAL_B,
                    GOLD,
                ],
            )
        )
        self.play(pie.beat())
        self.play(Uncreate(pie))


if __name__ == "__main__":
    with tempconfig({"dry_run": True}):
        TestSingle().render()
        # TestReformEqual().render()
        # TestReformFewer().render()
        # TestReformMore().render()
        pass
