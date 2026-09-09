# -----------------------------
# Baseline vs Optimized
# -----------------------------

baseline_distance = 357.69

# Replace this with the value printed by optimizer.py
optimized_distance = 133.03

improvement = baseline_distance - optimized_distance

if baseline_distance > 0:
    improvement_percentage = (
        improvement / baseline_distance
    ) * 100
else:
    improvement_percentage = 0


print("========== ROUTE COMPARISON ==========")
print(f"Baseline Distance:   {baseline_distance:.2f}")
print(f"Optimized Distance:  {optimized_distance:.2f}")
print(f"Distance Saved:      {improvement:.2f}")
print(f"Improvement:         {improvement_percentage:.2f}%")