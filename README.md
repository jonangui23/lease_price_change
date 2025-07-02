# State-Level Rent Price Sensitivity to Unemployment

## 📘 Overview

This project analyzes how rent prices in U.S. states respond to unemployment changes. By combining lease-level rental data(which can be changed to view other relationships) with quarterly unemployment rates, it uses a linear regression model with state-level changes to quantify and visualize **price sensitivity** across the country.

The resulting model allows us to determine which states have **more elastic** (sensitive) or **inelastic** (resilient) housing markets in response to labor market changes. A heatmap is generated to visually communicate these differences.

---

## 📊 Methodology

1. **Data Sources**
   - Lease data: Contains rental prices, availability, and location (by state, year, and quarter).
   - Unemployment data: Contains quarterly unemployment rates by U.S. state.

2. **Data Preparation**
   - Mean rental prices are aggregated by `state-year-quarter`.
   - Unemployment rates are merged in at the same granularity.
   - The log of rent price is used to stabilize variance and improve model fit.

3. **Feature Engineering**
   - **State dummy variables** are created to control for fixed effects.
   - **Interaction terms** are formed between each state dummy and the unemployment rate to allow for heterogeneous impacts.
   - Arizona (AZ) is used as the **baseline category** (its dummy is omitted).

4. **Model Estimation**
   - A linear regression (OLS) is fit with:
     - Dependent variable: log-transformed rent price.
     - Independent variables: unemployment rate × state dummy interactions.
   - The coefficient of `unemployment_rate` represents AZ.
   - Other coefficients represent the *difference* in unemployment sensitivity relative to AZ.

5. **Coefficient Adjustment**
   - All state interaction coefficients are adjusted by **adding AZ’s coefficient** to obtain the **total marginal effect** of unemployment on rent in each state.

6. **Geographic Visualization**
   - A shapefile of U.S. states is merged with the regression output.
   - A **heatmap** is generated using `GeoPandas` and `Matplotlib`, where color intensity reflects each state's price sensitivity to unemployment.

---

## 📂 File Structure

```bash
.
├── data/
│   ├── leases.csv
│   ├── unemployment.csv
│   └── cb_2018_us_state_5m.shp  # Shapefile for US states
├── analysis/
│   └── price_sensitivity_model.py
├── output/
│   └── rent_unemployment_heatmap.png
└── README.md

