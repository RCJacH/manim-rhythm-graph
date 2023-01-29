import pytest
import manim as mn

from manim_rhythm_graph import RhythmElement


@pytest.fixture(scope="module")
def scene():
    return mn.Scene()


@pytest.fixture(scope="function", autouse=True)
def render(request, monkeypatch):
    if "scene" not in request.fixturenames:
        return request.node._obj(
            **{
                k: request._fixture_defs[k].cached_result[0]
                for k in request.node._fixtureinfo.argnames
                if k in request._fixture_defs
            },
            **request.node.callspec.params
        )

    scene = request._fixture_defs["scene"].cached_result[0]

    def _wrapper(*args, **kwargs):
        return request.node._obj(
            scene, *args, **request.node.callspec.params, **kwargs
        )

    with mn.tempconfig({"dry_run": True}):
        monkeypatch.setattr(scene, "construct", _wrapper)
        scene.render()


@pytest.mark.parametrize(
    "weights, result",
    [
        (1, [1]),
        (4, (0.25,) * 4),
        (6, (1 / 6,) * 6),
        (-12, (1 / 12,) * 12),
        ([1, 2, 3, 4], [1 / 10, 2 / 10, 3 / 10, 4 / 10]),
        ([2, -2, 5, -6], [2 / 15, 2 / 15, 5 / 15, 6 / 15]),
        ([], (-1,)),
    ],
)
def test_weights(weights, result):
    ele = RhythmElement(weights=weights)
    assert (ele.weights == result).all()


@pytest.mark.parametrize(
    "weights, result",
    [
        (1, []),
        (4, []),
        (-12, list(range(12))),
        ([1, 2, 3, 4], []),
        ([2, -2, 5, -6], [1, 3]),
        ([], [0]),
    ],
)
def test_rest(weights, result):
    ele = RhythmElement(weights=weights)
    assert ele.rests == result


@pytest.mark.parametrize(
    "weights, colors, result",
    [
        (1, mn.BLUE, [mn.BLUE]),
        ([2, 1], [mn.BLUE, mn.RED], [mn.BLUE, mn.RED]),
        ([2, 2, 2, 2], [mn.BLUE, mn.RED], [mn.BLUE, mn.RED, mn.BLUE, mn.RED]),
        (
            [-2, 3, -4, 5, -6],
            [mn.YELLOW, mn.GOLD],
            [None, mn.YELLOW, None, mn.GOLD, None],
        ),
        (
            [7, 7, -3, 3, -3],
            [mn.DARK_BLUE, mn.TEAL],
            [mn.DARK_BLUE, mn.TEAL, None, mn.DARK_BLUE, None],
        ),
    ],
)
def test_colors(weights, colors, result):
    ele = RhythmElement(weights=weights, colors=colors)
    assert ele.colors == result


@pytest.mark.parametrize(
    "kwargs, result",
    [(dict(scale=2), dict(height=4)), (dict(scale=0.1), dict(height=0.2))],
)
def test_properties(kwargs, result):
    ele = RhythmElement(**kwargs)
    for k, v in result.items():
        assert getattr(ele, k) == v
