# src/analytics/plot_convergence.py

import matplotlib.pyplot as plt

from src.analytics.convergence import convergence_experiment


def main():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    path_list = [1_000, 5_000, 10_000, 50_000, 100_000, 200_000]

    mc_prices, bs_price = convergence_experiment(
        S0, K, r, sigma, T, path_list
    )

    plt.figure()
    plt.plot(path_list, mc_prices, marker="o", label="Monte Carlo Price")
    plt.axhline(bs_price, linestyle="--", label="Black–Scholes Price")
    plt.xscale("log")
    plt.xlabel("Number of Monte Carlo Paths (log scale)")
    plt.ylabel("Option Price")
    plt.title("Monte Carlo Convergence to Black–Scholes")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
