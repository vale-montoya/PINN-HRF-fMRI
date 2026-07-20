"""Pruebas y tamaños de efecto usados en las comparaciones pareadas."""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata


def holm_correction(p_values: list[float] | np.ndarray) -> np.ndarray:
    """Ajusta valores p mediante el procedimiento secuencial de Holm."""
    values = np.asarray(p_values, dtype=float)

    if values.ndim != 1:
        raise ValueError("p_values debe ser un vector unidimensional.")
    if np.any((values < 0) | (values > 1)):
        raise ValueError("Los valores p deben pertenecer a [0, 1].")

    n_tests = len(values)
    order = np.argsort(values)
    adjusted_sorted = np.empty(n_tests, dtype=float)
    running_maximum = 0.0

    for rank, original_index in enumerate(order):
        candidate = (n_tests - rank) * values[original_index]
        running_maximum = max(running_maximum, candidate)
        adjusted_sorted[rank] = min(running_maximum, 1.0)

    adjusted = np.empty(n_tests, dtype=float)
    adjusted[order] = adjusted_sorted
    return adjusted


def rank_biserial_paired(
    first: np.ndarray,
    second: np.ndarray,
) -> float:
    """Correlación biserial por rangos para diferencias pareadas."""
    differences = np.asarray(first, dtype=float) - np.asarray(second, dtype=float)
    differences = differences[~np.isclose(differences, 0.0)]

    if len(differences) == 0:
        return 0.0

    ranks = rankdata(np.abs(differences))
    positive_sum = np.sum(ranks[differences > 0])
    negative_sum = np.sum(ranks[differences < 0])

    return float(
        (positive_sum - negative_sum)
        / (positive_sum + negative_sum)
    )
