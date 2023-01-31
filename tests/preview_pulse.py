import numpy as np
from manim import *

from manim_rhythm_graph.pulse_mobject import Pulse
from manim_rhythm_graph import RhythmElement


class TestDrawPulse(Scene):
    def construct(self):
        ele = RhythmElement(scale=3, style="pulse")
        pulse = Pulse(scale=3)
        self.play(Create(ele))
        self.wait()
        self.play(ele.as_pie())
        self.wait()
        self.play(ele.as_pulse())
        self.wait()
        self.play(ele.as_stick())
        self.wait()
        self.play(ele.as_pulse())
        self.wait()
        self.play(Uncreate(ele))


if __name__ == "__main__":
    with tempconfig({"dry_run": True}):
        TestDrawPulse().render()
        pass
