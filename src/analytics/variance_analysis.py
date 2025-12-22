# src/analytics/variance_analysis.py

import numpy as np

from src.monte_carlo.simulator import (
    monte_carlo_european_call,
    monte_carlo_european_call_antithetic
)
from src.models.black_scholes import european_call_price


def variance_comparison(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    n_paths: int,
    n_runs: int = 50
):
    """
    Compare variance of plain Monte Carlo vs antithetic variates.
    """

    plain_estimates = []
    anti_estimates = []

    for seed in range(n_runs):
        plain_price = monte_carlo_european_call(
            S0=S0,
            K=K,
            r=r,
            sigma=sigma,
            T=T,
            n_paths=n_paths,
            seed=seed
        )

        anti_price = monte_carlo_european_call_antithetic(
            S0=S0,
            K=K,
            r=r,
            sigma=sigma,
            T=T,
            n_paths=n_paths,
            seed=seed
        )

        plain_estimates.append(plain_price)
        anti_estimates.append(anti_price)

    return (
        np.array(plain_estimates),
        np.array(anti_estimates),
        european_call_price(S0, K, r, sigma, T)
    )

# src/analytics/variance_analysis.py

import numpy as np
import matplotlib.pyplot as plt

from src.monte_carlo.simulator import (
    monte_carlo_european_call,
    monte_carlo_european_call_antithetic
)
from src.models.black_scholes import european_call_price


def variance_comparison(
    S0, K, r, sigma, T,
    n_paths, n_runs=50
):
    plain_estimates = []
    anti_estimates = []

    for seed in range(n_runs):
        plain_estimates.append(
            monte_carlo_european_call(
                S0, K, r, sigma, T,
                n_paths=n_paths,
                seed=seed
            )
        )

        anti_estimates.append(
            monte_carlo_european_call_antithetic(
                S0, K, r, sigma, T,
                n_paths=n_paths,
                seed=seed
            )
        )

    return (
        np.array(plain_estimates),
        np.array(anti_estimates),
        european_call_price(S0, K, r, sigma, T)
    )


def main():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    plain, anti, bs = variance_comparison(
        S0, K, r, sigma, T,
        n_paths=50_000,
        n_runs=50
    )

    print("Plain MC variance:     ", np.var(plain))
    print("Antithetic variance:  ", np.var(anti))

    plt.figure()
    plt.hist(plain, bins=15, alpha=0.6, label="Plain MC")
    plt.hist(anti, bins=15, alpha=0.6, label="Antithetic MC")
    plt.axvline(bs, linestyle="--", label="Black–Scholes")
    plt.legend()
    plt.title("Variance Reduction via Antithetic Variates")
    plt.show()


if __name__ == "__main__":
    main()
