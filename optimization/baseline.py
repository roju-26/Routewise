import pandas as pd


# -----------------------------
# Load data
# -----------------------------
orders = pd.read_csv("data/orders.csv")
vehicles = pd.read_csv("data/vehicles.csv")


print("Orders loaded:", len(orders))
print("Vehicles loaded:", len(vehicles))


# -----------------------------
# Track remaining capacity
# -----------------------------
remaining_capacity = {}

for _, vehicle in vehicles.iterrows():
    remaining_capacity[vehicle["vehicle_id"]] = vehicle["capacity"]


# -----------------------------
# Assign orders to vehicles
# -----------------------------
assignments = []

vehicle_index = 0

for _, order in orders.iterrows():

    assigned = False

    # Try vehicles starting from current vehicle
    for i in range(len(vehicles)):

        index = (vehicle_index + i) % len(vehicles)

        vehicle = vehicles.iloc[index]
        vehicle_id = vehicle["vehicle_id"]

        if remaining_capacity[vehicle_id] >= order["weight"]:

            assignments.append({
                "order_id": order["order_id"],
                "vehicle_id": vehicle_id,
                "weight": order["weight"],
                "priority": order["priority"],
                "x": order["x"],
                "y": order["y"],
                "ready_time": order["ready_time"],
                "due_time": order["due_time"],
                "service_time": order["service_time"]
            })

            remaining_capacity[vehicle_id] -= order["weight"]

            vehicle_index = index

            assigned = True
            break

    if not assigned:
        print(
            f"WARNING: Order {order['order_id']} "
            f"could not be assigned because of capacity."
        )


# -----------------------------
# Create result DataFrame
# -----------------------------
assignments_df = pd.DataFrame(assignments)
# -----------------------------
# Calculate baseline routes
# -----------------------------

def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


# -----------------------------
# Time-window checking
# -----------------------------

def format_time(minutes):
    """Convert minutes from midnight to HH:MM."""
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"


total_late_deliveries = 0
total_on_time_deliveries = 0
total_distance = 0

print("\nBaseline Routes:")

for _, vehicle in vehicles.iterrows():

    vehicle_id = vehicle["vehicle_id"]

    # Get orders assigned to this vehicle
    vehicle_orders = assignments_df[
        assignments_df["vehicle_id"] == vehicle_id
    ]

    if vehicle_orders.empty:
        print(f"{vehicle_id}: No deliveries")
        continue

    current_x = vehicle["start_x"]
    current_y = vehicle["start_y"]

    route_distance = 0

    route = ["Depot"]

    for _, order in vehicle_orders.iterrows():

        distance = calculate_distance(
            current_x,
            current_y,
            order["x"],
            order["y"]
        )

        route_distance += distance

        route.append(order["order_id"])

        current_x = order["x"]
        current_y = order["y"]

    # Return to depot
    distance = calculate_distance(
        current_x,
        current_y,
        vehicle["start_x"],
        vehicle["start_y"]
    )

    route_distance += distance

    route.append("Depot")

    total_distance += route_distance

    print(
        f"{vehicle_id}: "
        f"{' -> '.join(route)} | "
        f"Distance = {route_distance:.2f}"
    )


print(f"\nTotal Baseline Distance: {total_distance:.2f}")


# -----------------------------
# Display results
# -----------------------------
print("\nBaseline Vehicle Assignments:")
print(assignments_df)


print("\nRemaining Vehicle Capacity:")

for vehicle_id, capacity in remaining_capacity.items():
    print(vehicle_id, ":", capacity, "kg")


print("\nAssigned orders:",
      len(assignments_df))

print("Unassigned orders:",
      len(orders) - len(assignments_df))
print("\n========== BASELINE SUMMARY ==========")
print(f"Total orders: {len(orders)}")
print(f"Assigned orders: {len(assignments_df)}")
print(f"Unassigned orders: {len(orders) - len(assignments_df)}")
print(f"Total distance: {total_distance:.2f}")
print(f"On-time deliveries: {total_on_time_deliveries}")
print(f"Late deliveries: {total_late_deliveries}")