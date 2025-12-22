# src/monte_carlo/simulator.py

import numpy as np


def generate_standard_normals(
    n_paths: int,
    seed: int | None = None
) -> np.ndarray:
    """
    Generate standard normal random variables.

    Parameters
    ----------
    n_paths : int
        Number of Monte Carlo paths
    seed : int or None
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Array of standard normal random variables
    """
    if seed is not None:
        np.random.seed(seed)

    return np.random.standard_normal(n_paths)


# src/monte_carlo/simulator.py

import numpy as np
from src.models.gbm import gbm_terminal_price


def monte_carlo_european_call(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    n_paths: int,
    seed: int | None = None
) -> float:
    """
    Monte Carlo price of a European call option (terminal-only).

    Parameters
    ----------
    S0 : float
        Initial stock price
    K : float
        Strike price
    r : float
        Risk-free rate
    sigma : float
        Volatility
    T : float
        Time to maturity
    n_paths : int
        Number of Monte Carlo simulations
    seed : int or None
        Random seed

    Returns
    -------
    float
        Monte Carlo estimate of call option price
    """
    if seed is not None:
        np.random.seed(seed)

    Z = np.random.standard_normal(n_paths)

    ST = gbm_terminal_price(
        S0=S0,
        mu=r,              # risk-neutral drift
        sigma=sigma,
        T=T,
        Z=Z
    )

    payoff = np.maximum(ST - K, 0.0)

    discounted_price = np.exp(-r * T) * payoff.mean()

    return discounted_price


def monte_carlo_european_call_antithetic(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    n_paths: int,
    seed: int | None = None
) -> float:
    """
    Monte Carlo price of a European call option using antithetic variates.

    n_paths refers to the TOTAL number of simulated paths.
    Internally, we simulate n_paths / 2 pairs (Z, -Z).
    """

    if n_paths % 2 != 0:
        raise ValueError("n_paths must be even for antithetic variates.")

    if seed is not None:
        np.random.seed(seed)

    half = n_paths // 2
    Z = np.random.standard_normal(half)
    Z_antithetic = -Z

    Z_all = np.concatenate([Z, Z_antithetic])

    ST = gbm_terminal_price(
        S0=S0,
        mu=r,
        sigma=sigma,
        T=T,
        Z=Z_all
    )

    payoff = np.maximum(ST - K, 0.0)

    return np.exp(-r * T) * payoff.mean()

def monte_carlo_european_call_control_variate(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    n_paths: int,
    seed: int | None = None
) -> float:
    """
    Monte Carlo pricing using discounted stock price as a control variate.
    """

    if seed is not None:
        np.random.seed(seed)

    Z = np.random.standard_normal(n_paths)

    ST = gbm_terminal_price(
        S0=S0,
        mu=r,
        sigma=sigma,
        T=T,
        Z=Z
    )

    # Primary estimator
    X = np.exp(-r * T) * np.maximum(ST - K, 0.0)

    # Control variate: discounted stock price
    Y = np.exp(-r * T) * ST
    EY = S0  # known expectation under risk-neutral measure

    # Optimal beta
    cov = np.cov(X, Y, ddof=1)[0, 1]
    var = np.var(Y, ddof=1)
    beta = cov / var if var > 0 else 0.0

    # Control variate estimator (pathwise)
    X_cv = X + beta * (EY - Y)

    return X_cv.mean()
