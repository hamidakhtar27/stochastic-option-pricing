# 📈 Stochastic Option Pricing & Monte Carlo Simulation Framework

An industry-grade **quantitative finance project** implementing Monte Carlo–based European option pricing with variance reduction techniques, statistical confidence intervals, efficiency analysis, and sensitivity visualization.  
The project is deployed as an interactive Streamlit dashboard.

🔗 **Live Dashboard**  
https://stochastic-option-pricing-ejugmwdu2mtjpetx4l7cnj.streamlit.app/

---

## Overview

This project implements a **production-style option pricing engine** designed to reflect real-world quantitative workflows used in trading, risk management, and financial research.

Instead of focusing only on closed-form pricing formulas, the framework emphasizes:

- Statistical reliability of Monte Carlo estimators  
- Variance reduction and estimator efficiency  
- Benchmarking against analytical models  
- Clear visualization and interpretability  

The result is a practical, end-to-end quantitative system rather than a theoretical demonstration.

---

## Quantitative Methods Implemented

- Monte Carlo simulation for European call option pricing
- Variance reduction techniques:
  - Plain Monte Carlo
  - Antithetic Variates
  - Control Variates
- Black–Scholes analytical pricing benchmark
- Confidence intervals for Monte Carlo estimators
- Convergence and efficiency analysis
- Sensitivity analysis across volatility and maturity

---

## Dashboard Capabilities

### 1. Pricing & Comparison
- Monte Carlo option pricing
- Direct comparison with Black–Scholes price
- Distribution of Monte Carlo price estimates
- Confidence interval visualization

### 2. Efficiency Analysis
- Convergence behaviour across different simulation sizes
- Confidence interval width vs number of paths
- Performance comparison of variance reduction methods

### 3. Sensitivity Analysis
- Heatmap of option prices across:
  - Volatility
  - Time to maturity
- Intuitive visualization of parameter sensitivity

---

## Tech Stack

- **Python**
- **NumPy** — numerical computation
- **SciPy** — analytical pricing components
- **Pandas** — data handling
- **Matplotlib** — statistical visualization
- **Streamlit** — interactive dashboard and deployment
- **GitHub & Streamlit Cloud** — version control and hosting

---

## Project Structure

stochastic-option-pricing/
├── app.py # Streamlit entry point
├── requirements.txt
├── README.md
│
├── src/
│ ├── models/
│ │ └── black_scholes.py # Black–Scholes analytical pricing
│ ├── monte_carlo/
│ │ └── simulator.py # Monte Carlo & variance reduction methods
│ ├── analytics/
│ │ └── confidence_intervals.py
│ └── visualization/
│ └── dashboard.py # Streamlit dashboard
│
├── notebooks/ # Exploratory analysis & validation
└── tests/ # Unit tests (extendable)

---

## Author

**Mohd Hamid Akhtar Khan**  
B.Tech Computer Science  

Areas of Interest:
- Quantitative Finance
- Monte Carlo Simulation
- Statistical Modeling

GitHub: https://github.com/hamidakhtar27

---

## Future Work

- Greeks estimation using Monte Carlo methods
- Path-wise simulation and trajectory visualization
- Quasi–Monte Carlo techniques for variance reduction
- Extension to stochastic volatility models (e.g., Heston model)
- Performance optimization using Numba or C++

