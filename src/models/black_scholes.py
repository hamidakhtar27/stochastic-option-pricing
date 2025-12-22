import numpy as np
from scipy.stats import norm


def d1(S0, K, r, sigma, T):
    return (
        np.log(S0 / K)
        + (r + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))


def d2(S0, K, r, sigma, T):
    return d1(S0, K, r, sigma, T) - sigma * np.sqrt(T)


def european_call_price(S0, K, r, sigma, T):
    """
    Black–Scholes price for a European call option.
    """
    D1 = d1(S0, K, r, sigma, T)
    D2 = d2(S0, K, r, sigma, T)
    return S0 * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)


def european_put_price(S0, K, r, sigma, T):
    """
    Black–Scholes price for a European put option.
    """
    D1 = d1(S0, K, r, sigma, T)
    D2 = d2(S0, K, r, sigma, T)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S0 * norm.cdf(-D1)
