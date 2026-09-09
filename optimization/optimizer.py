import pandas as pd
import numpy as np

# Load delivery orders
orders = pd.read_csv("data/orders.csv")

# Load vehicles
vehicles = pd.read_csv("data/vehicles.csv")

print("Orders loaded:", len(orders))
print("Vehicles loaded:", len(vehicles))


# -----------------------------
# Create locations
# -----------------------------

locations = [(0, 0)]  # Depot

for _, order in orders.iterrows():
    locations.append((order["x"], order["y"]))


# -----------------------------
# Create distance matrix
# -----------------------------

num_locations = len(locations)

distance_matrix = np.zeros((num_locations, num_locations))

for i in range(num_locations):
    for j in range(num_locations):

        x1, y1 = locations[i]
        x2, y2 = locations[j]

        distance = np.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

        distance_matrix[i][j] = round(distance, 2)


# -----------------------------
# Create travel-time matrix
# -----------------------------

travel_time_matrix = distance_matrix * 2
travel_time_matrix = np.round(travel_time_matrix).astype(int)


print("Number of locations:", num_locations)
print("Distance matrix created.")
print("Travel-time matrix created.")
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# -----------------------------
# Create OR-Tools routing model
# -----------------------------

depot = 0

manager = pywrapcp.RoutingIndexManager(
    num_locations,
    len(vehicles),
    depot
)

routing = pywrapcp.RoutingModel(manager)

print("OR-Tools routing model created.")
# -----------------------------
# Distance callback
# -----------------------------

def distance_callback(from_index, to_index):
    """Return distance between two locations."""

    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)

    return int(distance_matrix[from_node][to_node] * 100)


transit_callback_index = routing.RegisterTransitCallback(
    distance_callback
)

routing.SetArcCostEvaluatorOfAllVehicles(
    transit_callback_index
)

print("Distance callback added.")
# -----------------------------
# Vehicle capacity constraint
# -----------------------------

def demand_callback(from_index):
    """Return the delivery weight at a location."""

    from_node = manager.IndexToNode(from_index)

    # Depot has zero demand
    if from_node == 0:
        return 0

    return int(orders.iloc[from_node - 1]["weight"])


demand_callback_index = routing.RegisterUnaryTransitCallback(
    demand_callback
)

vehicle_capacities = [
    int(vehicle["capacity"])
    for _, vehicle in vehicles.iterrows()
]

routing.AddDimensionWithVehicleCapacity(
    demand_callback_index,
    0,                      # No extra capacity allowed
    vehicle_capacities,     # Vehicle capacities
    True,                   # Start cumul at zero
    "Capacity"
)

print("Vehicle capacity constraint added.")
# -----------------------------
# Time formatting helper
# -----------------------------

def format_time(minutes):
    """Convert minutes from midnight to HH:MM."""
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"
# -----------------------------
# Time window constraint
# -----------------------------

def time_callback(from_index, to_index):
    """Return travel time between two locations."""

    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)

    return int(travel_time_matrix[from_node][to_node])


time_callback_index = routing.RegisterTransitCallback(
    time_callback
)

routing.AddDimension(
    time_callback_index,
    60,          # Waiting time allowed
    1440,        # Maximum route time: 24 hours
    False,       # Vehicle does not start at zero time
    "Time"
)

time_dimension = routing.GetDimensionOrDie("Time")


# -----------------------------
# Add delivery time windows
# -----------------------------

for order_index in range(1, num_locations):

    order = orders.iloc[order_index - 1]

    routing_index = manager.NodeToIndex(order_index)

    ready_time = int(order["ready_time"])
    due_time = int(order["due_time"])

    time_dimension.CumulVar(routing_index).SetRange(
        ready_time,
        due_time
    )


# Set vehicle start time
for vehicle_id in range(len(vehicles)):

    start_index = routing.Start(vehicle_id)

    time_dimension.CumulVar(start_index).SetRange(
        480,
        480
    )


print("Time-window constraint added.")


# -----------------------------
# Search parameters
# -----------------------------

search_parameters = pywrapcp.DefaultRoutingSearchParameters()

search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
)

search_parameters.time_limit.seconds = 10


# -----------------------------
# Solve the routing problem
# -----------------------------

print("\nSolving optimized routes...")

solution = routing.SolveWithParameters(
    search_parameters
)


# -----------------------------
# Display optimized routes
# -----------------------------

# -----------------------------
# Display optimized routes
# -----------------------------

if solution:

    print("\n========== OPTIMIZED ROUTES ==========")

    total_optimized_distance = 0
    route_results = []
    total_deliveries = 0
    total_on_time = 0
    total_late = 0

    for vehicle_id in range(len(vehicles)):

        index = routing.Start(vehicle_id)

        route = ["Depot"]
        route_distance = 0
        route_load = 0

        print(f"\nV{vehicle_id + 1:03d}:")

        while not routing.IsEnd(index):

            node_index = manager.IndexToNode(index)

            # Process delivery order
            if node_index != 0:

                order = orders.iloc[node_index - 1]

                order_id = order["order_id"]
                weight = int(order["weight"])
                ready_time = int(order["ready_time"])
                due_time = int(order["due_time"])
                service_time = int(order["service_time"])

                # Get scheduled arrival time
                delivery_time = solution.Value(
                    time_dimension.CumulVar(index)
                )

                route.append(order_id)

                route_load += weight
                total_deliveries += 1

                # Check time window
                if delivery_time <= due_time:
                    status = "ON TIME"
                    total_on_time += 1
                else:
                    status = "LATE"
                    total_late += 1

                print(
                    f"   {order_id} | "
                    f"Delivery: {format_time(delivery_time)} | "
                    f"Window: "
                    f"{format_time(ready_time)}-"
                    f"{format_time(due_time)} | "
                    f"{status}"
                )

            previous_index = index

            index = solution.Value(
                routing.NextVar(index)
            )

            # Calculate distance
            route_distance += routing.GetArcCostForVehicle(
                previous_index,
                index,
                vehicle_id
            ) / 100

            route.append("Depot")

        total_optimized_distance += route_distance

        route_results.append({
            "vehicle_id": f"V{vehicle_id + 1:03d}",
            "route": route,
            "load": route_load,
            "distance": route_distance
        })

        print(
            f"   Load: {route_load} kg"
        )

        print(
            f"   Distance: {route_distance:.2f}"
        )

        print(
            f"   Route: {' -> '.join(route)}"
        )


    # -----------------------------
    # Optimization summary
    # -----------------------------

    print("\n========== OPTIMIZATION SUMMARY ==========")

    print(
        f"Total orders: {len(orders)}"
    )

    print(
        f"Delivered orders: {total_deliveries}"
    )

    print(
        f"On-time deliveries: {total_on_time}"
    )

    print(
        f"Late deliveries: {total_late}"
    )

    print(
        f"Total Optimized Distance: "
        f"{total_optimized_distance:.2f}"
    )


else:

    print("\nNo feasible optimized solution found.")
    # ============================================================
# RETURN OPTIMIZATION RESULTS FOR DASHBOARD
# ============================================================

def get_optimization_results():

    if not solution:
        return {
            "routes": [],
            "total_distance": 0,
            "total_deliveries": 0,
            "on_time": 0,
            "late": 0
        }

    return {
        "routes": route_results,
        "total_distance": total_optimized_distance,
        "total_deliveries": total_deliveries,
        "on_time": total_on_time,
        "late": total_late
    }