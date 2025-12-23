# 📈 Stochastic Option Pricing & Monte Carlo Simulation Framework

An **industry-grade quantitative finance project** implementing Monte Carlo–based option pricing with variance reduction techniques, statistical confidence intervals, efficiency benchmarking, and sensitivity analysis — deployed as an interactive Streamlit dashboard.

🔗 **Live App**  
https://stochastic-option-pricing-ejugmwdu2mtjpetx4l7cnj.streamlit.app/

---

## 🔍 Project Overview

This project builds a **production-style option pricing engine** designed to mirror real-world quantitative workflows used in trading, risk, and research roles.

The dashboard enables users to:
- Price European call options using **Monte Carlo simulation**
- Apply **variance reduction techniques** (Antithetic Variates, Control Variates)
- Compare Monte Carlo estimates against the **Black–Scholes analytical solution**
- Quantify estimator uncertainty using **confidence intervals**
- Analyze convergence and estimator efficiency
- Visualize **sensitivity across volatility and maturity**

The emphasis is on **statistical reliability, performance, and interpretability**, not just formula implementation.

---

## 🧠 Quantitative Concepts Implemented

- Stochastic processes and log-normal asset dynamics
- Monte Carlo simulation for option pricing
- Variance reduction techniques:
  - Plain Monte Carlo
  - Antithetic Variates
  - Control Variates
- Confidence intervals for Monte Carlo estimators
- Convergence and efficiency analysis
- Sensitivity analysis across key model parameters
- Benchmarking against Black–Scholes model

---

## 🛠️ Tech Stack

- **Python**
- **NumPy** – numerical computation
- **SciPy** – analytical pricing components
- **Pandas** – data handling
- **Matplotlib** – statistical visualization
- **Streamlit** – interactive dashboard and deployment
- **GitHub + Streamlit Cloud** – version control and cloud hosting

---

## 🧩 Project Structure

stochastic-option-pricing/
│
├── app.py # Streamlit entry point
├── requirements.txt
├── README.md
│
├── src/
│ ├── models/
│ │ └── black_scholes.py # Black–Scholes analytical pricing
│ │
│ ├── monte_carlo/
│ │ └── simulator.py # Monte Carlo & variance reduction methods
│ │
│ ├── analytics/
│ │ └── confidence_intervals.py # Statistical confidence intervals
│ │
│ └── visualization/
│ └── dashboard.py # Streamlit dashboard
│
├── notebooks/ # Exploratory research & validation
└── tests/ # Unit tests (extendable)

---

## 📊 Dashboard Features

### 1️⃣ Pricing & Comparison
- Monte Carlo option pricing
- Comparison with Black–Scholes price
- Confidence interval estimation
- Distribution of Monte Carlo price estimates

### 2️⃣ Efficiency Analysis
- Convergence behaviour across simulation sizes
- CI width vs number of paths
- Performance comparison of variance reduction methods

### 3️⃣ Sensitivity Analysis
- Heatmap of option prices across:
  - Volatility
  - Time to maturity
- Intuitive visualization of parameter sensitivity

---

## 🚀 Run Locally

```bash
git clone https://github.com/hamidakhtar27/stochastic-option-pricing.git
cd stochastic-option-pricing

pip install -r requirements.txt
streamlit run app.py


🎯 Why This Project Matters

This project demonstrates:

Strong quantitative finance fundamentals

Statistical rigor beyond basic pricing

Clean, modular software design

Performance-aware Monte Carlo implementation

End-to-end deployment and reproducibility

👤 Author

Mohd Hamid Akhtar Khan
B.Tech Computer Science
Quantitative Finance • Monte Carlo Simulation • Statistical Modeling

GitHub: https://github.com/hamidakhtar27

🔮 Future Extensions

Greeks estimation via Monte Carlo

Path-wise simulation visualization

Quasi-Monte Carlo methods

Stochastic volatility models (Heston)

Performance optimization using Numba or C++


✅ **Save the file** (`Cmd + S`)

---

## ✅ PART 2 — STEP-BY-STEP: PUSH TO GITHUB

Make sure you are inside your repo folder:

```bash
cd stochastic-option-pricing

🔹 Step 1: Check file status
git status


You should see:

modified: README.md

🔹 Step 2: Stage the README
git add README.md

🔹 Step 3: Commit
git commit -m "Add final professional README"

🔹 Step 4: Sync with remote (IMPORTANT)
git pull --rebase origin main


If it completes cleanly, continue.

🔹 Step 5: Push to GitHub
git push origin main

✅ FINAL CHECK

Open your repo on GitHub

Refresh the page

You should see:

Clean README

Live app link

Proper formatting

🎯 RESULT

You now have:

✅ Industry-grade deployed project

✅ Professional GitHub presentation

✅ Resume-ready quant project

✅ MSc / Imperial-level credibility

When you’re ready, next I can:

Write resume bullets

Optimize this for UK quant interviews

Add Greeks / advanced features

Just say “next” 🚀

Uptill where is readme 

Good question — let me make this absolutely unambiguous.

📍 Where does the README end?

The README.md ends exactly here ⬇️

## 🔮 Future Extensions

- Greeks estimation via Monte Carlo
- Path-wise simulation visualization
- Quasi-Monte Carlo methods
- Stochastic volatility models (Heston)
- Performance optimization using Numba or C++


