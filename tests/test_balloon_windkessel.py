import numpy as np

from pinn_hrf.balloon_windkessel import (
    BalloonParameters,
    events_to_stimulus,
    simulate_balloon_windkessel,
)


def test_baseline_without_stimulus_is_zero_bold():
    times = np.linspace(0.0, 5.0, 51)
    parameters = BalloonParameters(
        epsilon=0.15,
        tau=0.98,
        alpha=0.32,
    )

    result = simulate_balloon_windkessel(
        times,
        parameters,
        stimulus=lambda _: 0.0,
    )

    assert np.allclose(result["f"], 1.0, atol=1e-8)
    assert np.allclose(result["v"], 1.0, atol=1e-8)
    assert np.allclose(result["q"], 1.0, atol=1e-8)
    assert np.allclose(result["bold_fraction"], 0.0, atol=1e-8)


def test_block_stimulus_produces_positive_response():
    times = np.linspace(0.0, 30.0, 301)
    parameters = BalloonParameters(
        epsilon=0.15,
        tau=0.98,
        alpha=0.32,
    )
    stimulus = events_to_stimulus(
        onsets_s=[1.0],
        durations_s=[1.0],
    )

    result = simulate_balloon_windkessel(
        times,
        parameters,
        stimulus,
    )

    assert np.max(result["bold_fraction"]) > 0.0
