import numpy as np

def has_no_nans(numbers: list) -> bool:
    return not np.isnan(numbers).any()
