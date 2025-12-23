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


# ==================================================
# Cached Monte Carlo runner (hashable inputs only)
# ==================================================
@st.cache_data(show_spinner=False)
def run_pricing(method, S0, K, r, sigma, T, n_paths, runs):
    pricing_funcs = {
        "Plain Monte Carlo": monte_carlo_european_call,
        "Antithetic Variates": monte_carlo_european_call_antithetic,
        "Control Variate": monte_carlo_european_call_control_variate,
    }

    func = pricing_funcs[method]

    return np.array([
        func(S0, K, r, sigma, T, n_paths, seed=i)
        for i in range(runs)
    ])


# ==================================================
# MAIN STREAMLIT APP
# ==================================================
def main():
    # --------------------------------------------------
    # Page config (MUST be first Streamlit call)
    # --------------------------------------------------
    st.set_page_config(
        page_title="Stochastic Option Pricing Dashboard",
        layout="wide"
    )

    st.title("📈 Stochastic Simulation & Option Pricing Framework")
    st.markdown(
        """
        Industry-grade quantitative dashboard for Monte Carlo option pricing,
        variance reduction techniques, statistical confidence intervals,
        efficiency benchmarking, and sensitivity analysis.
        """
    )

    # --------------------------------------------------
    # Sidebar controls
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Pricing
    # --------------------------------------------------
    price = pricing_funcs[method](S0, K, r, sigma, T, n_paths, seed=42)
    bs_price = european_call_price(S0, K, r, sigma, T)

    tab1, tab2, tab3 = st.tabs(
        ["📊 Pricing & Comparison", "📉 Efficiency", "🔥 Sensitivity"]
    )

    # ==================================================
    # TAB 1 — Pricing, Comparison & Distribution
    # ==================================================
    with tab1:
        st.subheader("Pricing Results")

        col1, col2 = st.columns(2)
        col1.metric(f"{method} Price", f"{price:.4f}")
        col2.metric("Black–Scholes Price", f"{bs_price:.4f}")

        st.markdown("### Method Comparison")

        rows = []
        for name in pricing_funcs.keys():
            start = time.perf_counter()
            samples = run_pricing(name, S0, K, r, sigma, T, n_paths, 15)
            elapsed = (time.perf_counter() - start) * 1000

            mean, lo, hi = confidence_interval(samples)
            rows.append({
                "Method": name,
                "Price": round(mean, 5),
                "CI Width": round(hi - lo, 6),
                "Abs Error vs BS": round(abs(mean - bs_price), 6),
                "Time (ms)": round(elapsed, 1),
            })

        st.dataframe(
            pd.DataFrame(rows).set_index("Method"),
            use_container_width=True
        )

        # --------- DISTRIBUTION PLOT (RESTORED PROPERLY) ---------
        st.markdown("### Monte Carlo Price Distribution")

        dist_samples = run_pricing(method, S0, K, r, sigma, T, n_paths, 30)
        mean, lo, hi = confidence_interval(dist_samples)

        fig, ax = plt.subplots()
        ax.hist(dist_samples, bins=20, alpha=0.7)
        ax.axvline(bs_price, linestyle="--", label="Black–Scholes")
        ax.axvline(lo, linestyle=":", label="95% CI Lower")
        ax.axvline(hi, linestyle=":", label="95% CI Upper")

        ax.set_xlabel("Option Price")
        ax.set_ylabel("Frequency")
        ax.set_title("Monte Carlo Estimator Distribution")
        ax.legend()

        st.pyplot(fig)

    # ==================================================
    # TAB 2 — Efficiency
    # ==================================================
    with tab2:
        st.subheader("Estimator Efficiency (CI Width vs Paths)")

        path_grid = [5_000, 10_000, 20_000, 50_000]
        fig, ax = plt.subplots()

        for name in pricing_funcs.keys():
            widths = []
            for n in path_grid:
                samples = run_pricing(name, S0, K, r, sigma, T, n, 10)
                _, lo, hi = confidence_interval(samples)
                widths.append(hi - lo)

            ax.plot(path_grid, widths, marker="o", label=name)

        ax.set_xscale("log")
        ax.set_xlabel("Number of Paths (log scale)")
        ax.set_ylabel("95% CI Width")
        ax.set_title("Monte Carlo Efficiency Comparison")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    # ==================================================
    # TAB 3 — Sensitivity
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
        im = ax.imshow(
            heatmap,
            origin="lower",
            aspect="auto",
            cmap="plasma"
        )
        fig.colorbar(im, ax=ax, label="Option Price")

        ax.set_xlabel("Volatility (σ)")
        ax.set_ylabel("Time to Maturity (T)")
        ax.set_title("Option Price Sensitivity (Control Variate)")

        st.pyplot(fig)

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    st.markdown("---")
    st.markdown(
        "Built by **Mohd Hamid Akhtar Khan**  \n"
        "Monte Carlo Simulation • Variance Reduction • Statistical Inference"
    )
