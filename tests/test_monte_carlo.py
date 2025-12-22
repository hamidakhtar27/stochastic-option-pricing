# tests/test_monte_carlo.py

from src.monte_carlo.simulator import monte_carlo_european_call
from src.models.black_scholes import european_call_price


def test_monte_carlo_converges_to_black_scholes():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    mc_price = monte_carlo_european_call(
        S0=S0,
        K=K,
        r=r,
        sigma=sigma,
        T=T,
        n_paths=200_000,
        seed=123
    )

    bs_price = european_call_price(S0, K, r, sigma, T)

    # Allow small statistical error
    assert abs(mc_price - bs_price) < 0.1
