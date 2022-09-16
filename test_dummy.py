from dummy import has_no_nans
import numpy as np


def test_has_no_nans():
    assert has_no_nans([0.8, 0.4, 0.2]) is True

    assert has_no_nans([0.8, 0.4, np.nan, 0.1]) is False
