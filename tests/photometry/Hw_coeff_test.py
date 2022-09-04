"""test for Hw_coeff.

"""
import pytest
from telescope_baseline.photometry import Hw_coeff

def test_compute_Hw_relation():
    res, sigma, colors, ar_J_H, ar_Hw_H, residuals=Hw_coeff.compute_Hw_relation(9000.0, 16000.0)
    assert res.x[0]==pytest.approx(-0.045044123313543155)
    assert res.x[1]==pytest.approx(0.947559160226985)
    assert sigma==pytest.approx(0.13499368235730813)
    assert res.fun==pytest.approx(3.304572506299581)

if __name__ == "__main__":
    test_compute_Hw_relation()

