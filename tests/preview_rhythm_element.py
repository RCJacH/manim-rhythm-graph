from manim import *

from manim_rhythm_graph import RhythmElement


class TestRhythmElement(Scene):
    def construct(self):
        ele = RhythmElement(3, scale=3, style="pulse")
        self.play(Create(ele))
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
        self.play(ele.as_pie())
        self.wait()
        self.play(ele.pulsate())
        self.wait()
        self.play(Uncreate(ele))


if __name__ == "__main__":
    with tempconfig({"dry_run": True}):
        TestRhythmElement().render()
        pass
