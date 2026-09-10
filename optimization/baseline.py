import pandas as pd
import math


def calculate_distance(x1, y1, x2, y2):
    """Calculate straight-line distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Load data
orders = pd.read_csv("data/orders.csv")
vehicles = pd.read_csv("data/vehicles.csv")

print("Orders loaded:", len(orders))
print("Vehicles loaded:", len(vehicles))

# Store baseline routes
routes = []

vehicle_index = 0

for _, order in orders.iterrows():

    vehicle = vehicles.iloc[vehicle_index]

    distance = calculate_distance(
        vehicle["start_x"],
        vehicle["start_y"],
        order["x"],
        order["y"]
    )

    routes.append({
        "vehicle_id": vehicle["vehicle_id"],
        "order_id": order["order_id"],
        "distance": distance,
        "weight": order["weight"]
    })

    vehicle_index += 1

    if vehicle_index >= len(vehicles):
        vehicle_index = 0


routes_df = pd.DataFrame(routes)

print("\nBaseline routes:")
print(routes_df)

print("\nTotal baseline distance:",
      round(routes_df["distance"].sum(), 2))

print("Total assigned weight:",
      routes_df["weight"].sum())