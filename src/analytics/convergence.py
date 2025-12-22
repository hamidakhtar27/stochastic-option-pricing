# src/analytics/convergence.py

import numpy as np
import matplotlib.pyplot as plt

from src.monte_carlo.simulator import monte_carlo_european_call
from src.models.black_scholes import european_call_price


def convergence_experiment(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    path_list: list[int],
    seed: int = 42
):
    """
    Run Monte Carlo convergence experiment for European call option.
    """

    mc_prices = []

    for n_paths in path_list:
        price = monte_carlo_european_call(
            S0=S0,
            K=K,
            r=r,
            sigma=sigma,
            T=T,
            n_paths=n_paths,
            seed=seed
        )
        mc_prices.append(price)

    bs_price = european_call_price(S0, K, r, sigma, T)

    return np.array(mc_prices), bs_price
