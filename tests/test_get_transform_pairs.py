import numpy as np
import pytest

from manim_rhythm_graph.pie_mobject.get_transform_pairs import (
    get_sector_pairs,
)


class TestPos:
    @pytest.mark.parametrize(
        "more_pos, less_pos, expectation",
        [
            ([0, 0.3, 0.6], [0, 0.5], [0, 0.5, 0.5]),
            ([0, 0.8, 0.9], [0, 0.5], [0, 0.5, 1]),
            ([0, 0.1, 0.2], [0, 0.75], [0, 0, 0.75]),
            ([0, 0.1, 0.2, 0.9], [0, 0.75], [0, 0, 0.75, 0.75]),
            ([0, 0.25, 0.5, 0.75], [0, 0.5], [0, 0.5, 0.5, 1]),
            ([0, 0.25, 0.5, 0.75], [0, 0.2, 0.5], [0, 0.2, 0.5, 1]),
            (
                [0, 1 / 6, 1 / 12, 0.5, 4 / 6, 5 / 6],
                [0, 0.2, 0.4, 0.6, 0.8],
                [0, 0.2, 0.2, 0.4, 0.6, 0.8],
            ),
        ],
    )
    def test_shrinking(self, more_pos, less_pos, expectation):
        more_array = np.stack([more_pos, (*more_pos[1:], 1)], dtype="float64")
        less_array = np.stack([less_pos, (*less_pos[1:], 1)], dtype="float64")
        expectation = np.array(expectation, dtype="float64")
        indice = [-1 if x == 1 else less_pos.index(x) for x in expectation]
        assert get_sector_pairs(less_array, more_array) == indice
