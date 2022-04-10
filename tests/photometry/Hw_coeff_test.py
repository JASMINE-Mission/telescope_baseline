"""test for Hw_coeff.

"""
import pytest
from telescope_baseline.photometry import Hw_coeff

def test_compute_Hw_relation():
    res, sigma, colors, ar_J_H, ar_Hw_H, residuals=Hw_coeff.compute_Hw_relation(9000.0, 16000.0)
    assert res.x[0]==pytest.approx(-0.06296266744365273)
    assert res.x[1]==pytest.approx(1.0927312678280945)
    assert sigma==pytest.approx(0.06436883637183226)
    assert res.fun==pytest.approx(1.5602719373940506)

if __name__ == "__main__":
    test_compute_Hw_relation()
    
