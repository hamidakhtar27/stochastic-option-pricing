import numpy as np


def gbm_terminal_price(
    S0: float,
    mu: float,
    sigma: float,
    T: float,
    Z: np.ndarray
) -> np.ndarray:
    """
    Compute terminal stock prices under Geometric Brownian Motion.

    Parameters
    ----------
    S0 : float
        Initial stock price
    mu : float
        Drift
    sigma : float
        Volatility
    T : float
        Time to maturity (in years)
    Z : np.ndarray
        Standard normal random variables

    Returns
    -------
    np.ndarray
        Simulated terminal prices S_T
    """
    return S0 * np.exp(
        (mu - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z
    )
