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

def generate_data(num_orders=30, num_vehicles=4):

    orders = []

    for i in range(1, num_orders + 1):
        order = {
            "order_id": f"O{i:03d}",
            "x": np.random.randint(1, 21),
            "y": np.random.randint(1, 21),
            "weight": np.random.randint(1, 11),
            "priority": np.random.choice(
                ["Low", "Medium", "High"]
            ),
            "ready_time": np.random.randint(480, 600),
            "due_time": np.random.randint(660, 900),
            "service_time": np.random.randint(5, 15),

            "historical_late_rate": round(
                np.random.uniform(0.05, 0.40), 2
            )
        }

        orders.append(order)

    orders_df = pd.DataFrame(orders)

    # -----------------------------
    # Generate vehicles
    # -----------------------------

    vehicles = []

    capacities = [50, 60, 70, 80]

    for i in range(1, num_vehicles + 1):

        capacity = capacities[
            (i - 1) % len(capacities)
        ]

        vehicles.append({
            "vehicle_id": f"V{i:03d}",
            "capacity": capacity,
            "start_x": 0,
            "start_y": 0
        })

    vehicles_df = pd.DataFrame(vehicles)

    # -----------------------------
    # Save CSV files
    # -----------------------------

    orders_df.to_csv(
        "data/orders.csv",
        index=False
    )

    vehicles_df.to_csv(
        "data/vehicles.csv",
        index=False
    )

    return orders_df, vehicles_df


if __name__ == "__main__":

    orders_df, vehicles_df = generate_data()

    print("Synthetic data generated successfully!")
    print()
    print("Orders:")
    print(orders_df.head())
    print()
    print("Vehicles:")
    print(vehicles_df)