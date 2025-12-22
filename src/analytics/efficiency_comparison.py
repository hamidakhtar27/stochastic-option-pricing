# src/analytics/efficiency_comparison.py

import numpy as np
import matplotlib.pyplot as plt

from src.monte_carlo.simulator import (
    monte_carlo_european_call,
    monte_carlo_european_call_antithetic,
    monte_carlo_european_call_control_variate
)
from src.models.black_scholes import european_call_price


def efficiency_experiment(
    S0, K, r, sigma, T,
    n_paths=20_000,
    n_runs=50
):
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

    return (
        np.array(plain),
        np.array(anti),
        np.array(control),
        european_call_price(S0, K, r, sigma, T)
    )


def main():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    plain, anti, control, bs = efficiency_experiment(
        S0=S0,
        K=K,
        r=r,
        sigma=sigma,
        T=T,
        n_paths=20_000,
        n_runs=50
    )

    print("Variance comparison (same computational budget):")
    print("Plain MC:      ", np.var(plain))
    print("Antithetic MC: ", np.var(anti))
    print("Control Var:   ", np.var(control))

    plt.figure()
    plt.boxplot(
    [plain, anti, control],
    tick_labels=["Plain", "Antithetic", "Control"],
    showfliers=False
)

    
    plt.axhline(bs, linestyle="--", label="Black–Scholes")
    plt.ylabel("Option Price")
    plt.title("Monte Carlo Efficiency Comparison")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
