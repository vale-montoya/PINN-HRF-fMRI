"""Modelo Balloon–Windkessel y simulación de la señal BOLD."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class BalloonParameters:
    """Parámetros del modelo Balloon–Windkessel."""

    epsilon: float
    tau: float
    alpha: float
    kappa_s: float = 0.65
    kappa_f: float = 0.41
    e0: float = 0.34
    v0: float = 0.02

    def validate(self) -> None:
        values = {
            "epsilon": self.epsilon,
            "tau": self.tau,
            "alpha": self.alpha,
            "kappa_s": self.kappa_s,
            "kappa_f": self.kappa_f,
            "e0": self.e0,
            "v0": self.v0,
        }
        invalid = [name for name, value in values.items() if not np.isfinite(value)]
        if invalid:
            raise ValueError(f"Parámetros no finitos: {invalid}")
        if self.tau <= 0 or self.alpha <= 0:
            raise ValueError("tau y alpha deben ser positivos.")
        if not 0 < self.e0 < 1:
            raise ValueError("e0 debe pertenecer al intervalo (0, 1).")
        if self.v0 <= 0:
            raise ValueError("v0 debe ser positivo.")


def events_to_stimulus(
    onsets_s: Iterable[float],
    durations_s: Iterable[float],
    amplitudes: Iterable[float] | None = None,
) -> Callable[[float], float]:
    """Crea una función de estímulo por bloques a partir de eventos."""
    onsets = np.asarray(list(onsets_s), dtype=float)
    durations = np.asarray(list(durations_s), dtype=float)

    if onsets.shape != durations.shape:
        raise ValueError("onsets_s y durations_s deben tener igual longitud.")

    if amplitudes is None:
        amps = np.ones_like(onsets)
    else:
        amps = np.asarray(list(amplitudes), dtype=float)

    if amps.shape != onsets.shape:
        raise ValueError("amplitudes debe tener igual longitud que onsets_s.")

    if np.any(durations <= 0):
        raise ValueError("Todas las duraciones deben ser positivas.")

    def stimulus(time_s: float) -> float:
        active = (time_s >= onsets) & (time_s < onsets + durations)
        return float(np.sum(amps[active]))

    return stimulus


def bold_from_states(
    volume: np.ndarray,
    deoxyhemoglobin: np.ndarray,
    *,
    e0: float = 0.34,
    v0: float = 0.02,
) -> np.ndarray:
    """Calcula el cambio BOLD fraccional desde los estados v y q."""
    volume = np.asarray(volume, dtype=float)
    deoxyhemoglobin = np.asarray(deoxyhemoglobin, dtype=float)

    if volume.shape != deoxyhemoglobin.shape:
        raise ValueError("volume y deoxyhemoglobin deben tener igual forma.")
    if np.any(volume <= 0):
        raise ValueError("El volumen normalizado debe ser positivo.")

    k1 = 7.0 * e0
    k2 = 2.0
    k3 = 2.0 * e0 - 0.2

    return v0 * (
        k1 * (1.0 - deoxyhemoglobin)
        + k2 * (1.0 - deoxyhemoglobin / volume)
        + k3 * (1.0 - volume)
    )


def simulate_balloon_windkessel(
    times_s: np.ndarray,
    parameters: BalloonParameters,
    stimulus: Callable[[float], float],
    *,
    max_step: float = 0.02,
    rtol: float = 1e-9,
    atol: float = 1e-11,
) -> dict[str, np.ndarray]:
    """Integra las ODE y devuelve estados y señal BOLD."""
    parameters.validate()
    times = np.asarray(times_s, dtype=float)

    if times.ndim != 1 or len(times) < 2:
        raise ValueError("times_s debe ser un vector 1D con al menos dos puntos.")
    if not np.all(np.isfinite(times)):
        raise ValueError("times_s contiene valores no finitos.")
    if not np.all(np.diff(times) > 0):
        raise ValueError("times_s debe ser estrictamente creciente.")

    def rhs(time_s: float, state: np.ndarray) -> list[float]:
        s, f, v, q = state
        f_safe = max(float(f), 1e-8)
        v_safe = max(float(v), 1e-8)

        extraction = 1.0 - (1.0 - parameters.e0) ** (1.0 / f_safe)
        neural_input = float(stimulus(time_s))

        ds_dt = (
            parameters.epsilon * neural_input
            - parameters.kappa_s * s
            - parameters.kappa_f * (f - 1.0)
        )
        df_dt = s
        dv_dt = (
            f - v_safe ** (1.0 / parameters.alpha)
        ) / parameters.tau
        dq_dt = (
            f * extraction / parameters.e0
            - v_safe ** (1.0 / parameters.alpha) * q / v_safe
        ) / parameters.tau

        return [ds_dt, df_dt, dv_dt, dq_dt]

    solution = solve_ivp(
        fun=rhs,
        t_span=(float(times[0]), float(times[-1])),
        y0=[0.0, 1.0, 1.0, 1.0],
        t_eval=times,
        method="RK45",
        max_step=max_step,
        rtol=rtol,
        atol=atol,
    )

    if not solution.success:
        raise RuntimeError(f"Falló la integración ODE: {solution.message}")

    s, f, v, q = solution.y
    bold = bold_from_states(v, q, e0=parameters.e0, v0=parameters.v0)

    return {
        "time_s": times,
        "s": s,
        "f": f,
        "v": v,
        "q": q,
        "bold_fraction": bold,
    }
