from manim import *

from manim_rhythm_graph import RhythmElement


class TestRhythmElement(Scene):
    def construct(self):
        ele = RhythmElement(
            weights=5, colors=[RED, BLUE], scale=3, style="pulse"
        )
        self.play(Create(ele))
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_pie())
        self.wait()
        self.play(
            ele.into(
                weights=[2, 1, 3, -2, 2, 2],
                colors=[GOLD, ORANGE, GREEN],
                scale=2,
            )
        )
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_pulse())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_stick())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_pulse())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_pie())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(ele.as_pulse())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(Uncreate(ele))


if __name__ == "__main__":
    with tempconfig({"dry_run": True}):
        TestRhythmElement().render()
        pass
