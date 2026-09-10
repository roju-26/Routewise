import pandas as pd
import numpy as np
import os

# Make results reproducible
np.random.seed(42)

# -----------------------------
# Create data folder if needed
# -----------------------------
os.makedirs("data", exist_ok=True)

# -----------------------------
# Generate delivery orders
# -----------------------------
num_orders = 30

orders = []

for i in range(1, num_orders + 1):
    order = {
        "order_id": f"O{i:03d}",
        "x": np.random.randint(1, 21),
        "y": np.random.randint(1, 21),
        "weight": np.random.randint(1, 11),
        "priority": np.random.choice(["Low", "Medium", "High"]),
        "ready_time": np.random.randint(480, 600),
        "due_time": np.random.randint(660, 900),
        "service_time": np.random.randint(5, 15)
    }

    orders.append(order)

orders_df = pd.DataFrame(orders)

# -----------------------------
# Generate vehicles
# -----------------------------
vehicles = [
    {
        "vehicle_id": "V001",
        "capacity": 50,
        "start_x": 0,
        "start_y": 0
    },
    {
        "vehicle_id": "V002",
        "capacity": 60,
        "start_x": 0,
        "start_y": 0
    },
    {
        "vehicle_id": "V003",
        "capacity": 70,
        "start_x": 0,
        "start_y": 0
    },
    {
        "vehicle_id": "V004",
        "capacity": 80,
        "start_x": 0,
        "start_y": 0
    }
]

vehicles_df = pd.DataFrame(vehicles)

# -----------------------------
# Save CSV files
# -----------------------------
orders_df.to_csv("data/orders.csv", index=False)
vehicles_df.to_csv("data/vehicles.csv", index=False)

print("Synthetic data generated successfully!")
print()
print("Orders:")
print(orders_df.head())
print()
print("Vehicles:")
print(vehicles_df)