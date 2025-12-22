# src/visualization/dashboard.py
def main():
    import streamlit as st
    
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
# Page config
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

st.markdown("<br>", unsafe_allow_html=True)

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
    [5_000, 10_000, 20_000, 50_000, 100_000],
    index=2
)

method = st.sidebar.radio(
    "Pricing Method",
    ["Plain Monte Carlo", "Antithetic Variates", "Control Variate"]
)

# ==================================================
# Pricing logic
# ==================================================
pricing_funcs = {
    "Plain Monte Carlo": monte_carlo_european_call,
    "Antithetic Variates": monte_carlo_european_call_antithetic,
    "Control Variate": monte_carlo_european_call_control_variate,
}

price = pricing_funcs[method](S0, K, r, sigma, T, n_paths, seed=42)
bs_price = european_call_price(S0, K, r, sigma, T)

# ==================================================
# Tabs
# ==================================================
tab1, tab2, tab3 = st.tabs(
    ["📊 Pricing & Comparison", "📉 Efficiency", "🔥 Sensitivity"]
)

# ==================================================
# TAB 1 — Pricing & Comparison
# ==================================================
with tab1:
    st.subheader("Pricing Results")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{method} Price", f"{price:.4f}")
    with col2:
        st.metric("Black–Scholes Price", f"{bs_price:.4f}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        f"""
        **Method Insight**
        - Plain MC converges at O(1/√N)
        - Variance reduction improves estimator efficiency
        - Confidence intervals quantify uncertainty

        **Current method:** {method}
        """
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("Method Comparison (Same Computational Budget)")

    rows = []
    for name, func in pricing_funcs.items():
        start = time.perf_counter()

        estimates = [
            func(S0, K, r, sigma, T, n_paths, seed=i)
            for i in range(20)
        ]

        elapsed = (time.perf_counter() - start) * 1000
        mean, lower, upper = confidence_interval(np.array(estimates))

        rows.append({
            "Method": name,
            "Price": round(mean, 5),
            "CI Width": round(upper - lower, 6),
            "Abs Error vs BS": round(abs(mean - bs_price), 6),
            "Time (ms)": round(elapsed, 1),
        })

    df = pd.DataFrame(rows)
    st.dataframe(df.set_index("Method"), use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("95% Confidence Interval (Selected Method)")

    samples = [
        pricing_funcs[method](S0, K, r, sigma, T, n_paths, seed=i)
        for i in range(30)
    ]

    mean, lower, upper = confidence_interval(np.array(samples))

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("95% CI Width", f"{upper - lower:.6f}")
    with col2:
        st.write(
            "This interval quantifies the statistical uncertainty of the "
            "Monte Carlo estimator under the selected method."
        )

    fig_ci, ax_ci = plt.subplots()
    ax_ci.hist(samples, bins=15, alpha=0.6)
    ax_ci.axvline(bs_price, linestyle="--", label="Black–Scholes")
    ax_ci.axvline(lower, linestyle=":", label="CI Lower")
    ax_ci.axvline(upper, linestyle=":", label="CI Upper")
    ax_ci.set_xlabel("Option Price")
    ax_ci.set_ylabel("Frequency")
    ax_ci.legend()
    fig_ci.tight_layout(pad=3.0)

    st.pyplot(fig_ci)

# ==================================================
# TAB 2 — Efficiency
# ==================================================
with tab2:
    st.subheader("Efficiency Analysis: CI Width vs Number of Paths")

    path_grid = [5_000, 10_000, 20_000, 50_000, 100_000]

    def ci_width(func):
        widths = []
        for n in path_grid:
            estimates = [
                func(S0, K, r, sigma, T, n, seed=i)
                for i in range(15)
            ]
            _, lo, hi = confidence_interval(np.array(estimates))
            widths.append(hi - lo)
        return widths

    fig_eff, ax_eff = plt.subplots()

    ax_eff.plot(path_grid, ci_width(monte_carlo_european_call), marker="o", label="Plain MC")
    ax_eff.plot(path_grid, ci_width(monte_carlo_european_call_antithetic), marker="o", label="Antithetic")
    ax_eff.plot(path_grid, ci_width(monte_carlo_european_call_control_variate), marker="o", label="Control Variate")

    ax_eff.set_xscale("log")
    ax_eff.set_xlabel("Number of Paths (log scale)")
    ax_eff.set_ylabel("95% CI Width")
    ax_eff.set_title("Estimator Efficiency Comparison")
    ax_eff.legend()
    ax_eff.grid(True)
    fig_eff.tight_layout(pad=3.0)

    st.pyplot(fig_eff)

# ==================================================
# TAB 3 — Sensitivity
# ==================================================
with tab3:
    st.subheader("Sensitivity Analysis: Volatility × Maturity Heatmap")

    vol_grid = np.linspace(0.1, 0.5, 8)
    T_grid = np.linspace(0.25, 2.0, 8)

    heatmap = np.zeros((len(T_grid), len(vol_grid)))

    for i, t in enumerate(T_grid):
        for j, vol in enumerate(vol_grid):
            heatmap[i, j] = monte_carlo_european_call_control_variate(
                S0, K, r, vol, t, n_paths=20_000, seed=42
            )

    fig_hm, ax_hm = plt.subplots()
    im = ax_hm.imshow(
        heatmap,
        origin="lower",
        aspect="auto",
        cmap="plasma",
        extent=[vol_grid[0], vol_grid[-1], T_grid[0], T_grid[-1]]
    )

    ax_hm.set_xlabel("Volatility (σ)")
    ax_hm.set_ylabel("Maturity (T)")
    ax_hm.set_title("Option Price Sensitivity (Control Variate)")
    fig_hm.colorbar(im, ax=ax_hm, label="Option Price")
    fig_hm.tight_layout(pad=3.0)

    st.pyplot(fig_hm)

# ==================================================
# Footer
# ==================================================
st.markdown(
    "<br><br><hr>",
    unsafe_allow_html=True
)

st.markdown(
    "Built by **Mohd Hamid Akhtar Khan**  \n"
    "Monte Carlo Simulation • Variance Reduction • Statistical Inference"
)

if __name__ == "__main__":
    main()
