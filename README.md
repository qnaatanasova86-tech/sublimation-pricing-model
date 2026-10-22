# Pricing Model for Sublimation Print Orders

A mathematical project on the application of linear algebra and least squares to the pricing of sublimation print orders (mugs, t-shirts, mousepads, phone cases and invitations).

## What the project does

1. Builds a **linear regression model** that predicts the production cost of an order from its characteristics (quantity, product type, ink, paper, press time, design time, waste).
2. Derives the least squares solution in matrix form, $\hat\beta = (X^T X)^{-1} X^T y$, and compares OLS with Ridge regression in the presence of multicollinearity.
3. Improves the model with an interaction between quantity and product type.
4. Checks the model with residual diagnostics and cross-validation.
5. Turns the model into a **price calculator**: the selling price for a target profit margin $m$ is $P = \hat y / (1 - m)$.

The data are **simulated** (60 orders), because there were not enough structured records of real orders. The results therefore describe the simulation and not a real workshop.

## Files

| File | Description |
|---|---|
| `pricing_model.ipynb` | The main notebook: problem, mathematics, analysis, models, diagnostics, calculator, conclusions |
| `generate_data.py` | Script that generates the simulated dataset (fixed random seed) |
| `orders.csv` | The simulated dataset (with a few missing values and one outlier on purpose) |
| `orders_clean.csv` | The dataset after cleaning (produced by the notebook) |
| `requirements.txt` | Python packages needed to run the notebook |

## How to run
pip install -r requirements.txt
jupyter notebook pricing_model.ipynb


Then choose **Kernel → Restart & Run All**. The notebook reads `orders.csv` from the same folder. To regenerate the data, run `python generate_data.py` (it writes the file to `data/orders.csv`; copy it next to the notebook).

## Main results

- Without interactions, OLS reaches a test R² of 0.56 and Ridge 0.62; both have large errors.
- With the quantity × product interaction, the test R² is 0.99 (mean absolute error about 1.4 EUR).
- A simplified model that uses only information known before production (product, quantity, design time) is as accurate and is used for quoting a price in advance.
- The very high accuracy reflects the simulated data; real data would give lower accuracy.

## Limitations

The data are simulated, the sample is small (59 orders), the calculator should be used only inside the range of quantities seen in the data, and the estimated cost has an error of about 10%. See Section 10.2 of the notebook.

## Use of AI assistance

Parts of this project were prepared with the help of an AI assistant (Claude, by Anthropic). More details are in Section 11 of the notebook.
