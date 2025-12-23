# src/visualization/dashboard.py

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from src.models.black_scholes import european_call_price
from src.monte_carlo.simulator import (
    monte_carlo_european_call,
    monte_carlo_european_call_antithetic,
    monte_carlo_european_call_control_variate
)
from src.analytics.confidence_intervals import confidence_interval


@st.cache_data(show_spinner=False)
def run_pricing(func, S0, K, r, sigma, T, n_paths, runs):
    return np.array([
        func(S0, K, r, sigma, T, n_paths, seed=i)
        for i in range(runs)
    ])


def main():
    # ==================================================
    # Page config (MUST BE FIRST)
    # ==================================================
    st.set_page_config(
        page_title="Stochastic Option Pricing Dashboard",
        layout="wide"
    )

    st.title("📈 Stochastic Simulation & Option Pricing Framework")
    st.markdown(
        """
        Industry-grade quantitative dashboard for Monte Carlo option pricing,
        variance reduction, statistical confidence intervals, efficiency analysis,
        and sensitivity visualization.
        """
    )

    # ==================================================
    # Sidebar controls
    # ==================================================
    st.sidebar.header("Option Parameters")

    S0 = st.sidebar.slider("Initial Price (S₀)", 50.0, 150.0, 100.0)
    K = st.sidebar.slider("Strike (K)", 50.0, 150.0, 100.0)
    r = st.sidebar.slider("Risk-free Rate (r)", 0.0, 0.10, 0.05)
    sigma = st.sidebar.slider("Volatility (σ)", 0.05, 0.50, 0.20)
    T = st.sidebar.slider("Time to Maturity (T, years)", 0.25, 2.0, 1.0)

    n_paths = st.sidebar.selectbox(
        "Number of Monte Carlo Paths",
        [5_000, 10_000, 20_000, 50_000],
        index=1
    )

    method = st.sidebar.radio(
        "Pricing Method",
        ["Plain Monte Carlo", "Antithetic Variates", "Control Variate"]
    )

    pricing_funcs = {
        "Plain Monte Carlo": monte_carlo_european_call,
        "Antithetic Variates": monte_carlo_european_call_antithetic,
        "Control Variate": monte_carlo_european_call_control_variate,
    }

    price = pricing_funcs[method](S0, K, r, sigma, T, n_paths, seed=42)
    bs_price = european_call_price(S0, K, r, sigma, T)

    tab1, tab2, tab3 = st.tabs(
        ["📊 Pricing & Comparison", "📉 Efficiency", "🔥 Sensitivity"]
    )

    # ==================================================
    # TAB 1
    # ==================================================
    with tab1:
        st.metric(f"{method} Price", f"{price:.4f}")
        st.metric("Black–Scholes Price", f"{bs_price:.4f}")

        rows = []
        for name, func in pricing_funcs.items():
            start = time.perf_counter()
            samples = run_pricing(func, S0, K, r, sigma, T, n_paths, 15)
            elapsed = (time.perf_counter() - start) * 1000

            mean, lo, hi = confidence_interval(samples)
            rows.append({
                "Method": name,
                "Price": round(mean, 5),
                "CI Width": round(hi - lo, 6),
                "Abs Error vs BS": round(abs(mean - bs_price), 6),
                "Time (ms)": round(elapsed, 1),
            })

        st.dataframe(pd.DataFrame(rows).set_index("Method"))

    # ==================================================
    # TAB 2
    # ==================================================
    with tab2:
        st.subheader("Efficiency Analysis")

        path_grid = [5_000, 10_000, 20_000, 50_000]
        fig, ax = plt.subplots()

        for name, func in pricing_funcs.items():
            widths = []
            for n in path_grid:
                samples = run_pricing(func, S0, K, r, sigma, T, n, 10)
                _, lo, hi = confidence_interval(samples)
                widths.append(hi - lo)
            ax.plot(path_grid, widths, marker="o", label=name)

        ax.set_xscale("log")
        ax.set_xlabel("Number of Paths")
        ax.set_ylabel("CI Width")
        ax.legend()
        st.pyplot(fig)

    # ==================================================
    # TAB 3
    # ==================================================
    with tab3:
        st.subheader("Volatility × Maturity Sensitivity")

        vol_grid = np.linspace(0.1, 0.5, 6)
        T_grid = np.linspace(0.25, 2.0, 6)
        heatmap = np.zeros((len(T_grid), len(vol_grid)))

        for i, t in enumerate(T_grid):
            for j, vol in enumerate(vol_grid):
                heatmap[i, j] = monte_carlo_european_call_control_variate(
                    S0, K, r, vol, t, n_paths=10_000, seed=42
                )

        fig, ax = plt.subplots()
        im = ax.imshow(heatmap, origin="lower", aspect="auto", cmap="plasma")
        fig.colorbar(im, ax=ax)
        st.pyplot(fig)


