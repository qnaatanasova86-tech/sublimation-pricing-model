"""Generate a synthetic dataset of sublimation orders for the pricing model.

The simulated costs are generated from known product- and quantity-dependent cost components, 
with a waste adjustment and random noise. The regression models approximate these relationships, 
allowing their predictive performance to be studied in a controlled setting.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 60

# product_type: (blank cost per unit, typical area cm2, typical qty range)
PRODUCTS = {
    "mug":        (2.50, 200, (1, 24)),
    "t-shirt":    (5.00, 600, (1, 15)),
    "mousepad":   (2.00, 450, (1, 20)),
    "phone_case": (3.00, 60,  (1, 12)),
    "invitation": (0.30, 300, (20, 150)),
}
INK_COST_PER_ML = 0.15
PAPER_COST_PER_SHEET = 0.05
PRESS_COST_PER_MIN = 0.12
DESIGN_COST_PER_MIN = 0.15

rows = []
for i in range(1, N + 1):
    p = rng.choice(list(PRODUCTS))
    blank, area, (qmin, qmax) = PRODUCTS[p]
    qty = int(rng.integers(qmin, qmax + 1))
    area_cm2 = round(area * rng.normal(1.0, 0.1), 1)
    ink_ml = round(area_cm2 * qty * 0.0025 * rng.normal(1.0, 0.1), 2)
    paper = int(np.ceil(area_cm2 * qty / 600 * rng.normal(1.0, 0.05)))
    press_min = round(qty * rng.uniform(1.5, 3.0) + 5, 1)
    design_min = round(rng.uniform(10, 90), 0)
    waste_pct = round(float(np.clip(rng.normal(5, 2.5), 0, 15)), 1)

    cost = (
        blank * qty * (1 + waste_pct / 100)
        + ink_ml * INK_COST_PER_ML
        + paper * PAPER_COST_PER_SHEET
        + press_min * PRESS_COST_PER_MIN
        + design_min * DESIGN_COST_PER_MIN
    )
    cost *= rng.normal(1.0, 0.04)  # unexplained noise
    rows.append([i, p, qty, area_cm2, ink_ml, paper, press_min,
                 design_min, waste_pct, round(cost, 2)])

df = pd.DataFrame(rows, columns=[
    "order_id", "product_type", "quantity", "area_cm2", "ink_ml",
    "paper_sheets", "press_time_min", "design_time_min", "waste_pct",
    "total_cost_eur"])

# Add a few missing values and one outlier, for data-cleaning practice
for col in ["ink_ml", "waste_pct", "design_time_min"]:
    df.loc[rng.choice(df.index, 2, replace=False), col] = np.nan
df.loc[rng.integers(0, N), "total_cost_eur"] *= 3

from pathlib import Path

output_path = Path("orders.csv")
df.to_csv(output_path, index=False)

print(f"Dataset saved to: {output_path.resolve()}")
print(df.head(), "\n", df.shape)
