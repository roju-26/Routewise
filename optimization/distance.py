import pandas as pd
import numpy as np


# -----------------------------
# Load orders
# -----------------------------
orders = pd.read_csv("data/orders.csv")


# -----------------------------
# Create locations
# -----------------------------
# Depot is location 0
locations = [(0, 0)]

# Add every order location
for _, order in orders.iterrows():
    locations.append((order["x"], order["y"]))


# -----------------------------
# Calculate distance matrix
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
# Calculate travel-time matrix
# -----------------------------
# Assumption:
# 1 distance unit = 2 minutes of travel
travel_time_matrix = distance_matrix * 2

travel_time_matrix = np.round(travel_time_matrix).astype(int)


# -----------------------------
# Display results
# -----------------------------
print("Number of locations:", num_locations)

print("\nDistance Matrix:")
print(distance_matrix)

print("\nTravel Time Matrix (minutes):")
print(travel_time_matrix)