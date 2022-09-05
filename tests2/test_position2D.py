from telescope_baseline.tools.pipeline_v2.position2d import Position2D


def test_pos():
    p = Position2D(1.0, 0.1)
    assert abs(p.x - 1.0) < 1e-6
    assert abs(p.y - 0.1) < 1e-6
