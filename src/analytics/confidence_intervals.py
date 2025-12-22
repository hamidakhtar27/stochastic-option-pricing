# src/analytics/confidence_intervals.py

import numpy as np
from typing import Tuple


def confidence_interval(
    samples: np.ndarray,
    alpha: float = 0.05
) -> Tuple[float, float, float]:
    """
    Compute mean estimate and two-sided confidence interval.

    Parameters
    ----------
    samples : np.ndarray
        Monte Carlo samples
    alpha : float
        Significance level (default 0.05 for 95% CI)

    Returns
    -------
    mean : float
    lower : float
    upper : float
    """
    mean = np.mean(samples)
    std = np.std(samples, ddof=1)
    n = len(samples)

    z = 1.96  # for 95% CI
    margin = z * std / np.sqrt(n)

    return mean, mean - margin, mean + margin

from src.monte_carlo.simulator import (
    monte_carlo_european_call,
    monte_carlo_european_call_antithetic,
    monte_carlo_european_call_control_variate
)


def mc_confidence_intervals(
    S0, K, r, sigma, T,
    n_paths=20_000,
    n_runs=50
):
    """
    Compute confidence intervals for different Monte Carlo estimators.
    """

    plain, anti, control = [], [], []

    for seed in range(n_runs):
        plain.append(
            monte_carlo_european_call(
                S0, K, r, sigma, T,
                n_paths=n_paths,
                seed=seed
            )
        )

        anti.append(
            monte_carlo_european_call_antithetic(
                S0, K, r, sigma, T,
                n_paths=n_paths,
                seed=seed
            )
        )

        control.append(
            monte_carlo_european_call_control_variate(
                S0, K, r, sigma, T,
                n_paths=n_paths,
                seed=seed
            )
        )

    return {
        "plain": confidence_interval(np.array(plain)),
        "antithetic": confidence_interval(np.array(anti)),
        "control": confidence_interval(np.array(control)),
    }

import matplotlib.pyplot as plt
from src.models.black_scholes import european_call_price
from src.monte_carlo.simulator import monte_carlo_european_call


def error_decay_experiment(
    S0, K, r, sigma, T,
    path_list,
    seed=42
):
    errors = []
    sqrt_N = []

    bs = european_call_price(S0, K, r, sigma, T)

    for n in path_list:
        mc_price = monte_carlo_european_call(
            S0, K, r, sigma, T,
            n_paths=n,
            seed=seed
        )
        errors.append(abs(mc_price - bs))
        sqrt_N.append(np.sqrt(n))

    return np.array(sqrt_N), np.array(errors)


def plot_error_decay():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    path_list = [1_000, 5_000, 10_000, 50_000, 100_000, 200_000]

    sqrt_N, errors = error_decay_experiment(
        S0, K, r, sigma, T, path_list
    )

    plt.figure()
    plt.plot(sqrt_N, errors, marker="o")
    plt.xlabel("√N")
    plt.ylabel("Absolute Pricing Error")
    plt.title("Monte Carlo Error Decay (∝ 1/√N)")
    plt.grid(True)
    plt.show()
