"""Métricas comunes para señales BOLD y HRF."""

from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def safe_pearson(observed: np.ndarray, predicted: np.ndarray) -> float:
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if observed.shape != predicted.shape:
        raise ValueError("observed y predicted deben tener igual forma.")
    if observed.size < 2:
        return float("nan")
    if np.std(observed) < 1e-12 or np.std(predicted) < 1e-12:
        return float("nan")

    return float(np.corrcoef(observed, predicted)[0, 1])


def regression_metrics(
    observed: np.ndarray,
    predicted: np.ndarray,
) -> dict[str, float]:
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if observed.shape != predicted.shape:
        raise ValueError("observed y predicted deben tener igual forma.")
    if not np.all(np.isfinite(observed)) or not np.all(np.isfinite(predicted)):
        raise ValueError("Las entradas contienen valores no finitos.")

    mse = mean_squared_error(observed, predicted)
    mae = mean_absolute_error(observed, predicted)

    return {
        "mse_fraction": float(mse),
        "rmse_fraction": float(np.sqrt(mse)),
        "rmse_percent": float(100.0 * np.sqrt(mse)),
        "mae_fraction": float(mae),
        "mae_percent": float(100.0 * mae),
        "r2": float(r2_score(observed, predicted)),
        "pearson_r": safe_pearson(observed, predicted),
    }
