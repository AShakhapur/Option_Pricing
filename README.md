# Option Pricing Project

## Overview

This project aims to provide users with a straightforward way to utilize various option pricing strategies using the asset of your choice. The goal was educational to further my understanding of these techniques.

## Project Goals

- Implement and compare different option pricing models.
- Provide a simple interface for users to input data and receive option pricing results.
- Educate users on the methodologies and logic behind option pricing strategies.

## Trading Methods

### Black-Scholes Model

The Black-Scholes model is currently implemented. It provides a closed-form solution for pricing European call and put options. This model assumes that the price of the underlying asset follows a geometric Brownian motion with constant volatility and interest rate.

**Current State:**
- Implemented and functional.
- Accepts user input for asset price, strike price, time to expiration, risk-free rate, and volatility.
- Outputs the calculated call and put option prices.

**Limitations:**
- Assumes constant volatility and interest rate.
- Only applicable for European options, which can only be exercised at expiration.

### Binomial Pricing Strategy

The Binomial Pricing Model constructs a binomial tree to represent possible future stock prices. By working backward through the tree, it calculates the option price. This model can handle various types of options and is flexible in terms of modeling different conditions.

**Current State:**
- Currently Functional.
- Further Testing required to ensure validity.

**Limitations:**
- Computationally intensive for a large number of steps.
- Less intuitive compared to the Black-Scholes model.

### Least Squares Monte Carlo (LSMC) Strategy

The Least Squares Monte Carlo method uses simulation to estimate the value of options. By simulating numerous paths of the underlying asset price and applying least squares regression, it can approximate the option's value, especially useful for American options where early exercise is possible.

**Current State:**
- In progress.
- Will provide a powerful approach for pricing options with complex features.

**Limitations:**
- Computationally intensive due to the need for many simulations.
- Requires careful implementation to ensure accuracy and efficiency.

### Implicit Bayesian Strategy

The Implicit Bayesian Strategy aims to use a Bayesian approach to determine option prices. This method will incorporate prior beliefs and observed data to update the probability distribution of the option prices.

**Current State:**
- Conceptual stage.
- Will involve Bayesian statistical methods to enhance option pricing accuracy.

**Limitations:**
- Requires further research and development.
- May be complex to implement and interpret.

## Project Structure

- **`get_data.rmd`**: R Markdown script for gathering and preprocessing data.
- **`pricing_models.py`**: Python script containing the implementation of various pricing models.
- **`README.md`**: Project overview and instructions.
- **`stock_df.csv`**: CSV file containing historical stock data.
- **`stock_identity.csv`**: CSV file containing stock metadata.
- **`testing.ipynb`**: Jupyter notebook for quick testing.
- **`data_funcs.r`**: R script with functions related to data handling.
- **`testing.py`**: Python script for testing the implementations.

## Usage Instructions

Currently, the code operates through console input. Users are prompted to input parameters such as asset price, strike price, time to expiration, risk-free rate, and volatility. The results are then displayed in the console. Future updates will include more sophisticated interfaces and expanded functionality.

To get started, run the `get_data.rmd` script and follow the on-screen prompts. Then run the `pricing_models.py` script and follow the on-screen prompts here as well.

## Additional Information

For further reading and references, please refer to the following resources:
- [Black-Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [Binomial Options Pricing Model](https://en.wikipedia.org/wiki/Binomial_options_pricing_model)
- [Least Squares Monte Carlo](https://en.wikipedia.org/wiki/Least_squares_Monte_Carlo)
