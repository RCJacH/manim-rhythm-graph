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
