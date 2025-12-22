# tests/test_black_scholes.py

from src.models.black_scholes import european_call_price, european_put_price


def test_call_put_parity():
    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1.0

    call = european_call_price(S0, K, r, sigma, T)
    put = european_put_price(S0, K, r, sigma, T)

    lhs = call - put
    rhs = S0 - K * (2.718281828459045 ** (-r * T))

    assert abs(lhs - rhs) < 1e-6
