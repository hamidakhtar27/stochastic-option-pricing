# 📈 Stochastic Simulation & Option Pricing Framework

An **industry-grade quantitative finance project** implementing Monte Carlo option pricing, variance reduction techniques, statistical confidence analysis, and an interactive Streamlit dashboard.

🔗 **Live Dashboard**:  
https://stochastic-option-pricing-9ejr99bhhr9chguyngsnrr.streamlit.app/

---

## 🚀 Features

- **Black–Scholes analytical pricing**
- **Monte Carlo simulation** for European options
- **Variance reduction techniques**
  - Antithetic variates
  - Control variates
- **Statistical confidence intervals (95%)**
- **Estimator efficiency comparison**
- **Sensitivity analysis (volatility × maturity heatmaps)**
- **Interactive Streamlit dashboard**

---

## 🧠 Quantitative Concepts Demonstrated

- Stochastic differential equations (GBM)
- Risk-neutral valuation
- Monte Carlo convergence analysis
- Variance reduction efficiency
- Confidence interval estimation
- Bias–variance tradeoff

---

## 🛠️ Tech Stack

- **Python**
- NumPy, SciPy
- Matplotlib
- Pandas
- Streamlit
- PyTest (unit testing)

---

## 📊 Dashboard Preview

The dashboard allows real-time experimentation with:
- Initial price
- Strike
- Volatility
- Risk-free rate
- Time to maturity
- Monte Carlo paths
- Pricing methodology

---

## 📂 Project Structure

```text
stochastic-option-pricing/
│
├── src/
│   ├── models/          # Black-Scholes, GBM
│   ├── monte_carlo/     # Simulators
│   ├── analytics/       # CI, convergence, efficiency
│   └── visualization/  # Streamlit dashboard
│
├── tests/               # Unit tests
├── app.py               # Streamlit entry point
├── requirements.txt
└── README.md
