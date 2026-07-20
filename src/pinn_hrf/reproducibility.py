"""Utilidades de reproducibilidad."""

from __future__ import annotations

import random

import numpy as np
import torch


def set_global_seed(seed: int, *, deterministic: bool = True) -> None:
    """Configura semillas de Python, NumPy y PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    if deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)
