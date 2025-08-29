import random
import numpy as np

# Usage: set Python/NumPy RNGs for reproducible runs
def set_seed(seed: int = 42):
    random.seed(seed)
    try:
        np.random.seed(seed)
    except Exception:
        pass
